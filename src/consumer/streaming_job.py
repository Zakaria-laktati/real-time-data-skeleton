from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import avg, col, from_json, to_timestamp, window
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import os
import time

# Configuration
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:29092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'raw_data')
CHECKPOINT_LOCATION = os.getenv('SPARK_CHECKPOINT_LOCATION', '/tmp/checkpoint')

# Configuration PostgreSQL
POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin123')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'realtime_data')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'postgres')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_URL = f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Schéma des données
schema = StructType([
    StructField("timestamp", StringType(), True),
    StructField("value", DoubleType(), True),
    StructField("type", StringType(), True)
])

def create_spark_session():
    """Crée une session Spark avec les configurations nécessaires"""
    return SparkSession.builder \
        .appName("RealTimeDataProcessing") \
        .config("spark.sql.streaming.checkpointLocation", CHECKPOINT_LOCATION) \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.postgresql:postgresql:42.2.23") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true") \
        .getOrCreate()

def write_to_postgres(df, epoch_id):
    """Écrit le DataFrame dans PostgreSQL"""
    last_exception = None
    for attempt in range(1, 6):
        try:
            df.write \
                .format("jdbc") \
                .option("url", POSTGRES_URL) \
                .option("dbtable", "processed_data") \
                .option("user", POSTGRES_USER) \
                .option("password", POSTGRES_PASSWORD) \
                .option("driver", "org.postgresql.Driver") \
                .mode("append") \
                .save()
            return
        except Exception as exc:  # pragma: no cover - best effort resilience
            last_exception = exc
            wait_seconds = min(5 * attempt, 30)
            print(f"PostgreSQL indisponible (tentative {attempt}/5). Nouvel essai dans {wait_seconds}s : {exc}")
            time.sleep(wait_seconds)

    if last_exception is not None:
        raise last_exception

def parse_kafka_records(df: DataFrame) -> DataFrame:
    """Convertit les messages Kafka en colonnes exploitable par Spark."""
    parsed_df = df.select(
        from_json(col("value").cast("string"), schema).alias("parsed_data")
    ).select(
        to_timestamp(col("parsed_data.timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSSSSS").alias("event_timestamp"),
        col("parsed_data.value").alias("value"),
        col("parsed_data.type").alias("type")
    )
    return parsed_df.dropna(subset=["event_timestamp"])


def aggregate_events(df: DataFrame, window_duration: str = "5 minutes") -> DataFrame:
    """Agrège les événements par fenêtre temporelle et type."""
    working_df = df
    if working_df.isStreaming:
        working_df = working_df.withWatermark("event_timestamp", window_duration)

    return working_df.groupBy(
        window("event_timestamp", window_duration),
        "type"
    ).agg(
        avg("value").alias("avg_value")
    ).select(
        col("window.start").alias("timestamp"),
        col("type"),
        col("avg_value").alias("value")
    )


def process_stream(spark):
    """Configure et exécute le job de streaming"""
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BROKER) \
        .option("subscribe", KAFKA_TOPIC) \
        .option("startingOffsets", "latest") \
        .load()

    parsed_df = parse_kafka_records(df)
    processed_df = aggregate_events(parsed_df)

    # Écriture dans PostgreSQL
    query = processed_df \
        .writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("update") \
        .start()

    query.awaitTermination()

def main():
    spark = create_spark_session()
    process_stream(spark)

if __name__ == "__main__":
    main()