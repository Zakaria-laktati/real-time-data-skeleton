# Real-Time Data Pipeline Skeleton

Ce projet propose un squelette prêt à l’emploi pour construire un pipeline de données en temps réel avec Kafka, Spark, PostgreSQL et une API Flask.

## Architecture

```
Producteur -> Kafka -> Spark Structured Streaming -> PostgreSQL <- Flask API
```

## Technologies

- Apache Kafka : ingestion évènementielle
- Apache Spark Structured Streaming : calcul temps réel
- PostgreSQL : persistance relationnelle
- Flask : exposition REST
- Docker Compose : orchestration locale

## Structure

```
.
├── checkpoint/                    # stockage des états Spark (monté en volume)
├── docker/                        # Dockerfiles (Spark, API, producer)
├── scripts/                       # scripts auxiliaires (init Kafka...)
├── src/
│   ├── api/                       # endpoints Flask
│   ├── consumer/                  # job Spark
│   ├── producer/                  # producteur Kafka
│   └── utils/                     # utilitaires partagés
├── tests/
│   ├── integration/               # tests d’intégration (docker compose)
│   └── unit/                      # tests unitaires Spark
├── .env.example                   # modèle d’environnement
├── docker-compose.yml             # orchestration des services
├── requirements.txt               # dépendances applicatives
├── requirements-dev.txt           # dépendances de test
└── README.md
```

## Mise en route

1. Copier `.env.example` vers `.env` et ajuster les valeurs si besoin.
2. Construire les images : `docker compose build`
3. Lancer le pipeline : `docker compose up -d`
4. Vérifier l’API : `curl http://localhost:5000/health`

## Services

- Kafka (`9092`) et Zookeeper (`2181`)
- Spark monitoring (`4040`, `8080`)
- PostgreSQL (`5432`) et pgAdmin (`5050`)
- API Flask (`5000` par défaut)

## Tests

- Installer les dépendances : `pip install -r requirements.txt -r requirements-dev.txt`
- Tests unitaires : `pytest tests/unit`
- Tests d’intégration (docker requis) : `RUN_INTEGRATION_TESTS=1 pytest tests/integration`
- Les tests d’intégration sont optionnels par défaut et valident la configuration Docker.

## Bonnes pratiques

- Utiliser les fonctions `parse_kafka_records` et `aggregate_events` pour étendre les transformations Spark.
- Adapter les schémas, topics et tables en fonction de votre cas d’usage.
- Ajouter la télémétrie (logs structurés, métriques) selon vos critères de production.

## Publication GitHub

- Initialiser le dépôt : `git init && git add . && git commit -m "Initial skeleton"`
- Créer un repository vide sur GitHub puis lier l’origine : `git remote add origin https://github.com/<user>/<repo>.git`
- Pousser la branche principale : `git push -u origin main`

## Soutenir le projet

Si ce squelette vous est utile, vous pouvez soutenir son évolution en contribuant, en partageant le repository ou via un pourboire sur la plateforme de votre choix. Merci !
