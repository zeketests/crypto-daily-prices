import pytest
import csv
import os


def make_mock_coins(count=100, price_multiplier=1.0):
    """Generate mock coin data matching the CoinGecko API structure."""
    coins = []
    base_prices = [45000.0, 3000.0, 1.0, 400.0, 150.0, 300.0, 0.5, 12.0, 80.0, 25.0]
    for i in range(count):
        coins.append({
            "symbol": f"coin{i}",
            "name": f"Coin {i}",
            "current_price": round(base_prices[i % len(base_prices)] * price_multiplier, 2),
        })
    return coins


@pytest.fixture
def mock_coins():
    return make_mock_coins(100)


@pytest.fixture
def setup_dirs(tmp_path, monkeypatch):
    """Change cwd to tmp_path and create a README.md with update markers."""
    monkeypatch.chdir(tmp_path)
    readme = tmp_path / "README.md"
    readme.write_text(
        "# Crypto Daily Prices\n\n"
        "<!-- AUTO-UPDATE-START -->\n"
        "<!-- AUTO-UPDATE-END -->\n"
    )
    return tmp_path


@pytest.fixture
def setup_dirs_with_yesterday(setup_dirs, mock_coins):
    """Adds a yesterday CSV so the diff + README update code path is exercised."""
    from datetime import datetime, timedelta

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    folder = setup_dirs / f"data/{today.year}/{today.month:02}"
    folder.mkdir(parents=True, exist_ok=True)

    yesterday_csv = folder / f"prices_{yesterday.strftime('%Y-%m-%d')}.csv"
    with open(yesterday_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "name", "symbol", "price"])
        for idx, coin in enumerate(mock_coins, start=1):
            writer.writerow([idx, coin["name"], coin["symbol"].upper(), coin["current_price"]])

    return setup_dirs
