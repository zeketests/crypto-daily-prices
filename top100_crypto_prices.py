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

    today_prices = {}
    changes = []
    new_entries = []
    removed_entries = []
    biggest_gainer = None
    biggest_loser = None

    # Save CSV
    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "name", "symbol", "price"])
        for idx, coin in enumerate(data, start=1):
            symbol = coin['symbol'].upper()
            price = coin['current_price']
            today_prices[symbol] = price
            writer.writerow([idx, coin['name'], symbol, price])

    # Compare with yesterday
    if os.path.exists(yesterday_csv):
        with open(yesterday_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            yesterday_prices = {row['symbol'].upper(): float(row['price']) for row in reader}

        for symbol, price in today_prices.items():
            if symbol in yesterday_prices:
                old_price = yesterday_prices[symbol]
                change = ((price - old_price) / old_price) * 100
                changes.append((symbol, change, old_price, price))
                if not biggest_gainer or change > biggest_gainer[1]:
                    biggest_gainer = (symbol, change)
                if not biggest_loser or change < biggest_loser[1]:
                    biggest_loser = (symbol, change)
            else:
                new_entries.append(symbol)

        removed_entries = list(set(yesterday_prices.keys()) - set(today_prices.keys()))

        with open(diff_filename, "w", encoding="utf-8") as f:
            f.write(f"📊 Differences between {yesterday_str} and {today_str}\n\n")
            for symbol, change, old, new in changes:
                if change > 5:
                    f.write(f"🔼 {symbol} ↑ {change:.2f}% (${old} → ${new})\n")
                elif change < -5:
                    f.write(f"🔽 {symbol} ↓ {change:.2f}% (${old} → ${new})\n")

            if new_entries:
                f.write("\n🆕 New in Top 100:\n")
                for s in new_entries:
                    f.write(f"+ {s}\n")

            if removed_entries:
                f.write("\n❌ Removed from Top 100:\n")
                for s in removed_entries:
                    f.write(f"- {s}\n")

        # Update README
        summary = f"""**Date:** {today_str}  
**Biggest gainer:** {biggest_gainer[0]} ↑ {biggest_gainer[1]:.2f}%  
**Biggest loser:** {biggest_loser[0]} ↓ {abs(biggest_loser[1]):.2f}%  
**New entries:** {', '.join(new_entries) if new_entries else 'None'}  
**Removed:** {', '.join(removed_entries) if removed_entries else 'None'}"""

        update_readme_summary(summary)

def update_readme_summary(summary_text):
    with open("README.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    start = "<!-- AUTO-UPDATE-START -->"
    end = "<!-- AUTO-UPDATE-END -->"

    new_lines = []
    inside = False
    for line in lines:
        if start in line:
            inside = True
            new_lines.append(line)
            new_lines.append(summary_text + "\n")
        elif end in line:
            inside = False
            new_lines.append(line)
        elif not inside:
            new_lines.append(line)

    with open("README.md", "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    fetch_top_100_cryptos()
