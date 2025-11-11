import json
import os
import time
from datetime import datetime
import random
from kafka import KafkaProducer

# Configuration Kafka
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'raw_data')

def create_producer():
    """Crée une instance du producteur Kafka"""
    return KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER],
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )

def generate_data():
    """Génère des données factices pour le test"""
    return {
        'timestamp': datetime.now().isoformat(),
        'value': random.uniform(0, 100),
        'type': random.choice(['type_A', 'type_B', 'type_C'])
    }

def main():
    producer = create_producer()
    print(f"Connexion au broker Kafka: {KAFKA_BROKER}")
    print(f"Envoi des données vers le topic: {KAFKA_TOPIC}")

    while True:
        try:
            # Génération et envoi des données
            data = generate_data()
            producer.send(KAFKA_TOPIC, value=data)
            print(f"Données envoyées: {data}")
            time.sleep(1)  # Envoi toutes les secondes
        except Exception as e:
            print(f"Erreur lors de l'envoi des données: {e}")
            break

    producer.close()

if __name__ == "__main__":
    main()