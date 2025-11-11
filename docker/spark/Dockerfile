# Stage de build
FROM eclipse-temurin:11-jdk-focal

# Install Python and dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip wget && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

# Install Spark
ENV SPARK_VERSION=3.4.0
ENV HADOOP_VERSION=3

RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /usr/local/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Set environment variables
ENV SPARK_HOME=/usr/local/spark \
    JAVA_HOME=/opt/java/openjdk \
    PATH="${SPARK_HOME}/bin:${JAVA_HOME}/bin:$PATH"

# Fix Spark script to use correct Java path
RUN sed -i 's|/usr/local/openjdk-11/bin/java|/opt/java/openjdk/bin/java|g' ${SPARK_HOME}/bin/spark-class

# Install Python dependencies
COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

WORKDIR /app

# Le script de streaming sera monté via un volume
CMD ["spark-submit", \
    "--master", "local[*]", \
    "--conf", "spark.jars.ivy=/tmp/.ivy", \
    "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.postgresql:postgresql:42.2.23", \
    "consumer/streaming_job.py"]