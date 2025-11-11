# Real-Time Data Pipeline Skeleton (template)

This repository provides a reusable starting point for building end-to-end real-time data pipelines with Apache Kafka, Apache Spark Structured Streaming, PostgreSQL, and a Flask REST API. A 🇫🇷 French version of this guide is available in [`README.fr.md`](README.fr.md).

## Architecture

```
Producer -> Kafka -> Spark Structured Streaming -> PostgreSQL <- Flask API
```

## Technologies

- Apache Kafka for event ingestion
- Apache Spark Structured Streaming for real-time processing
- PostgreSQL for durable storage
- Flask for REST exposure
- Docker Compose for local orchestration

## Project Structure

```
.
├── checkpoint/                    # Spark checkpoints (mounted volume)
├── docker/                        # Dockerfiles (Spark, API, producer)
├── scripts/                       # helper scripts (Kafka init, …)
├── src/
│   ├── api/                       # Flask endpoints
│   ├── consumer/                  # Spark job
│   ├── producer/                  # Kafka producer
│   └── utils/                     # shared helpers
├── tests/
│   ├── integration/               # Docker Compose smoke tests
│   └── unit/                      # Spark unit tests
├── .env.example                   # environment template
├── docker-compose.yml             # service orchestration
├── requirements.txt               # runtime dependencies
├── requirements-dev.txt           # test dependencies
└── README.md
```

## Getting Started

1. Copy `.env.example` to `.env` and tweak the values if necessary.
2. Build the images: `docker compose build`
3. Launch the stack: `docker compose up -d`
4. Check the API: `curl http://localhost:5000/health`

## Services

- Kafka (`9092`) and Zookeeper (`2181`)
- Spark monitoring UI (`4040`, `8080`)
- PostgreSQL (`5432`) and pgAdmin (`5050`)
- Flask API (`5000` by default)

## Testing

- Install the dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
- Unit tests: `pytest tests/unit` (skipped on Python ≥ 3.12 because PySpark 3.4 lacks support)
- Integration smoke test (requires Docker): `RUN_INTEGRATION_TESTS=1 pytest tests/integration`
- Integration tests are disabled by default and only validate the Compose configuration.

## Best Practices

- Extend the Spark logic through `parse_kafka_records` and `aggregate_events` in `src/consumer/streaming_job.py`.
- Adjust Kafka topics, schemas, and PostgreSQL tables to match your use case.
- Add observability (structured logging, metrics, tracing) before promoting to production.

## Publishing to GitHub

- Initialize Git: `git init && git add . && git commit -m "Initial skeleton"`
- Create an empty repository on GitHub and link it: `git remote add origin https://github.com/<user>/<repo>.git`
- Push the main branch: `git push -u origin main`

## Support
If you find this project helpful, consider supporting the developer by [buying them a coffee](https://www.buymeacoffee.com/zakarialaktati)!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-yellow.svg)](https://www.buymeacoffee.com/zakarialaktati)
