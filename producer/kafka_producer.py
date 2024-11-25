from kafka import KafkaProducer
import time
import json

def create_producer():
    retries = 30
    while retries > 0:
        try:
            producer = KafkaProducer(
                bootstrap_servers=['kafka:9092'],
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            return producer
        except Exception as e:
            print(f"Tentative de connexion à Kafka... ({retries} essais restants)")
            retries -= 1
            time.sleep(1)
    raise Exception("Impossible de se connecter à Kafka")

def publish_messages():
    producer = create_producer()
    print("Producer successfully created!")
    messages = [
        "Les algorithmes de machine learning permettent de créer des modèles prédictifs.",
        "L'apprentissage supervisé utilise des données étiquetées pour l'entraînement.",
        "Le clustering est une technique d'apprentissage non supervisé.",
        "Les réseaux de neurones sont essentiels pour le deep learning.",
        "Les modèles de régression linéaire sont simples mais puissants."
    ]

    while True:
        for message in messages:
            producer.send('machine_learning', {'message': message})
            producer.flush()
            print(f"Message envoyé: {message}")
            time.sleep(2)

if __name__ == "__main__":
    publish_messages() 