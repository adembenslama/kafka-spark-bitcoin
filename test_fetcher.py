import requests
from datetime import datetime
import time

def get_bitcoin_price(api_key):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd,eur",
        "x_cg_demo_api_key": api_key
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return {
            "timestamp": datetime.now().isoformat(),
            "price_usd": data["bitcoin"]["usd"],
            "price_eur": data["bitcoin"]["eur"]
        }
    except Exception as e:
        print(f"Erreur lors de la récupération du prix: {e}")
        return None

def main():
    api_key = "CG-25b3ZFtxtcNuY2Z9NqnSzuHX"
    
    while True:
        price_data = get_bitcoin_price(api_key)
        if price_data:
            print(f"Prix Bitcoin: ${price_data['price_usd']} | €{price_data['price_eur']}")
            print(f"Timestamp: {price_data['timestamp']}")
        time.sleep(2)  # Attendre 2 secondes entre chaque requête

if __name__ == "__main__":
    main() 