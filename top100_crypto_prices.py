# top100_crypto_prices.py
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

    response = requests.get(url, params=params)
    data = response.json()

    now = datetime.now().strftime('%Y-%m-%d')
    filename = f"prices_{now}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for idx, coin in enumerate(data, start=1):
            name = coin['name']
            symbol = coin['symbol'].upper()
            price = coin['current_price']
            f.write(f"{idx}. {name} ({symbol}): ${price}\n")

if __name__ == "__main__":
    fetch_top_100_cryptos()
