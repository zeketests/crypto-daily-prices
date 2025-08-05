import os
import requests
from datetime import datetime, timedelta
import csv

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

    today = datetime.now()
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = (today - timedelta(days=1)).strftime('%Y-%m-%d')

    folder = f"data/{today.year}/{today.month:02}"
    os.makedirs(folder, exist_ok=True)

    csv_filename = os.path.join(folder, f"prices_{today_str}.csv")
    diff_filename = os.path.join(folder, f"diff_{today_str}.txt")
    yesterday_csv = os.path.join(folder, f"prices_{yesterday_str}.csv")

    # Save today's data as CSV
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "name", "symbol", "price"])
        for idx, coin in enumerate(data, start=1):
            writer.writerow([idx, coin['name'], coin['symbol'].upper(), coin['current_price']])

    # Prepare dict for today
    today_prices = {coin['symbol'].upper(): coin['current_price'] for coin in data}

    # Compare with yesterday if file exists
    if os.path.exists(yesterday_csv):
        with open(yesterday_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            yesterday_prices = {row['symbol'].upper(): float(row['price']) for row in reader}

        with open(diff_filename, "w", encoding="utf-8") as f:
            f.write(f"📊 Differences between {yesterday_str} and {today_str}\n\n")
            
            # Check price changes
            for symbol, price in today_prices.items():
                if symbol in yesterday_prices:
                    old_price = yesterday_prices[symbol]
                    change = ((price - old_price) / old_price) * 100
                    if change > 5:
                        f.write(f"🔼 {symbol} ↑ {change:.2f}% (${old_price} → ${price})\n")
                    elif change < -5:
                        f.write(f"🔽 {symbol} ↓ {change:.2f}% (${old_price} → ${price})\n")

            # Check new entries
            new_symbols = set(today_prices.keys()) - set(yesterday_prices.keys())
            if new_symbols:
                f.write("\n🆕 New in Top 100:\n")
                for s in new_symbols:
                    f.write(f"+ {s}\n")

            # Check removed entries
            removed_symbols = set(yesterday_prices.keys()) - set(today_prices.keys())
            if removed_symbols:
                f.write("\n❌ Removed from Top 100:\n")
                for s in removed_symbols:
                    f.write(f"- {s}\n")

if __name__ == "__main__":
    fetch_top_100_cryptos()
