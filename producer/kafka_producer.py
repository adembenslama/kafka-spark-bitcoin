from kafka import KafkaProducer
import time
import json
import requests
from datetime import datetime

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

def get_bitcoin_price(api_key):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd,eur",
        "x_cg_demo_api_key": api_key
    }
    try:
        response = requests.get(url, params=params)
        print(f"API Response Status: {response.status_code}")
        if response.status_code != 200:
            print(f"API Error: {response.text}")
            return None
        data = response.json()
        return {
            "timestamp": datetime.now().isoformat(),
            "price_usd": data["bitcoin"]["usd"],
            "price_eur": data["bitcoin"]["eur"]
        }
    except Exception as e:
        print(f"Erreur lors de la récupération du prix: {e}")
        return None

def publish_messages():
    producer = create_producer()
    print("Producer successfully created!")
    api_key = "CG-25b3ZFtxtcNuY2Z9NqnSzuHX"

    while True:
        price_data = get_bitcoin_price(api_key)
        if price_data:
            try:
                producer.send('machine_learning', price_data)
                producer.flush()
                print(f"Prix Bitcoin envoyé: ${price_data['price_usd']} | €{price_data['price_eur']}")
                print("Message successfully sent to Kafka")
            except Exception as e:
                print(f"Erreur lors de l'envoi du message à Kafka: {e}")
        time.sleep(2)

if __name__ == "__main__":
    publish_messages() 