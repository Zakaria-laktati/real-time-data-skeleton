#!/bin/sh

# Attente que Kafka soit prêt
echo "Attente de Kafka..."
sleep 10

# Paramètres dynamiques
BOOTSTRAP_SERVER="${KAFKA_BROKER:-kafka:29092}"
TOPIC_NAME="${KAFKA_TOPIC:-raw_data}"

# Création du topic
echo "Création du topic ${TOPIC_NAME}..."
kafka-topics --create \
    --if-not-exists \
    --bootstrap-server "${BOOTSTRAP_SERVER}" \
    --partitions 1 \
    --replication-factor 1 \
    --topic "${TOPIC_NAME}"

# Vérification
echo "Topics créés :"
kafka-topics --list --bootstrap-server "${BOOTSTRAP_SERVER}"