import os
import requests
from datetime import datetime

def fetch_top_100_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1
    }

    response = requests.get(url, params=params, timeout=30)
    data = response.json()

    today = datetime.now().strftime('%Y-%m-%d')
    folder = f"data/{today[:4]}/{today[5:7]}"
    os.makedirs(folder, exist_ok=True)

    filename = os.path.join(folder, f"prices_{today}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        for idx, coin in enumerate(data, start=1):
            f.write(f"{idx}. {coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']}\n")

if __name__ == "__main__":
    fetch_top_100_cryptos()
