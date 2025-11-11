import datetime as dt
import sys

import pytest

from src.consumer.streaming_job import aggregate_events, parse_kafka_records


pytestmark = pytest.mark.skipif(
    sys.version_info >= (3, 12),
    reason="PySpark 3.4 n'est pas compatible avec Python >= 3.12 pour les tests locaux.",
)


def test_parse_kafka_records_extracts_expected_fields(spark):
    payload = [{"value": '{"timestamp": "2025-11-10T16:00:00.000000", "value": 12.5, "type": "type_A"}'}]
    raw_df = spark.createDataFrame(payload)

    parsed_df = parse_kafka_records(raw_df)
    result = parsed_df.collect()[0]

    assert result.type == "type_A"
    assert result.value == 12.5
    assert result.event_timestamp == dt.datetime(2025, 11, 10, 16, 0)


def test_aggregate_events_computes_window_average(spark):
    payload = [
        {"value": '{"timestamp": "2025-11-10T16:00:00.000000", "value": 10.0, "type": "type_A"}'},
        {"value": '{"timestamp": "2025-11-10T16:02:00.000000", "value": 30.0, "type": "type_A"}'},
        {"value": '{"timestamp": "2025-11-10T16:03:00.000000", "value": 20.0, "type": "type_B"}'},
    ]
    raw_df = spark.createDataFrame(payload)

    parsed_df = parse_kafka_records(raw_df)
    aggregated_df = aggregate_events(parsed_df, window_duration="5 minutes")

    results = {(row.type, round(row.value, 2)) for row in aggregated_df.collect()}
    expected = {("type_A", 20.0), ("type_B", 20.0)}

    assert results == expected
