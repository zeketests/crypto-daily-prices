import csv
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import patch

import allure
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.conftest import make_mock_coins
from top100_crypto_prices import fetch_top_100_cryptos, update_readme_summary


def _today_csv_path(base):
    today = datetime.now()
    return base / f"data/{today.year}/{today.month:02}/prices_{today.strftime('%Y-%m-%d')}.csv"


def _today_diff_path(base):
    today = datetime.now()
    return base / f"data/{today.year}/{today.month:02}/diff_{today.strftime('%Y-%m-%d')}.txt"


# ---------------------------------------------------------------------------
# CSV generation
# ---------------------------------------------------------------------------

@allure.feature("CSV Generation")
class TestCSVGeneration:

    @allure.story("File Creation")
    @allure.title("CSV file is created after fetching prices")
    def test_csv_file_is_created(self, setup_dirs, mock_coins):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        assert _today_csv_path(setup_dirs).exists()

    @allure.story("File Format")
    @allure.title("CSV file has the expected headers: rank, name, symbol, price")
    def test_csv_has_correct_headers(self, setup_dirs, mock_coins):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        with open(_today_csv_path(setup_dirs), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ["rank", "name", "symbol", "price"]

    @allure.story("File Content")
    @allure.title("CSV file contains exactly 100 rows")
    def test_csv_contains_100_rows(self, setup_dirs, mock_coins):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        with open(_today_csv_path(setup_dirs), encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 100

    @allure.story("File Content")
    @allure.title("CSV rows have sequential rank values starting at 1")
    def test_csv_ranks_are_sequential(self, setup_dirs, mock_coins):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        with open(_today_csv_path(setup_dirs), encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        ranks = [int(r["rank"]) for r in rows]
        assert ranks == list(range(1, 101))

    @allure.story("File Content")
    @allure.title("CSV prices match the API response values")
    def test_csv_prices_match_api_data(self, setup_dirs, mock_coins):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        with open(_today_csv_path(setup_dirs), encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        for row, coin in zip(rows, mock_coins):
            assert float(row["price"]) == coin["current_price"]
            assert row["symbol"] == coin["symbol"].upper()


# ---------------------------------------------------------------------------
# Diff generation
# ---------------------------------------------------------------------------

@allure.feature("Diff Generation")
class TestDiffGeneration:

    @allure.story("No Previous Data")
    @allure.title("No diff file is created when there is no previous day CSV")
    def test_no_diff_without_previous_data(self, setup_dirs, mock_coins):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        assert not _today_diff_path(setup_dirs).exists()

    @allure.story("With Previous Data")
    @allure.title("Diff file is created when previous day CSV exists")
    def test_diff_created_with_previous_data(self, setup_dirs_with_yesterday, mock_coins):
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        assert _today_diff_path(setup_dirs_with_yesterday).exists()

    @allure.story("With Previous Data")
    @allure.title("Diff file contains the correct date range header")
    def test_diff_contains_date_header(self, setup_dirs_with_yesterday, mock_coins):
        today = datetime.now()
        yesterday = today - timedelta(days=1)

        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        content = _today_diff_path(setup_dirs_with_yesterday).read_text(encoding="utf-8")
        assert yesterday.strftime("%Y-%m-%d") in content
        assert today.strftime("%Y-%m-%d") in content

    @allure.story("Price Changes")
    @allure.title("Diff file reports coins with gains greater than 5%")
    def test_diff_reports_significant_gainers(self, setup_dirs, mock_coins):
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        folder = setup_dirs / f"data/{today.year}/{today.month:02}"
        folder.mkdir(parents=True, exist_ok=True)

        # Yesterday prices are ~10% lower
        yesterday_coins = make_mock_coins(100, price_multiplier=0.88)
        yesterday_csv = folder / f"prices_{yesterday.strftime('%Y-%m-%d')}.csv"
        with open(yesterday_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["rank", "name", "symbol", "price"])
            for idx, coin in enumerate(yesterday_coins, start=1):
                writer.writerow([idx, coin["name"], coin["symbol"].upper(), coin["current_price"]])

        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        content = _today_diff_path(setup_dirs).read_text(encoding="utf-8")
        assert "🔼" in content

    @allure.story("Price Changes")
    @allure.title("Diff file reports coins with losses greater than 5%")
    def test_diff_reports_significant_losers(self, setup_dirs, mock_coins):
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        folder = setup_dirs / f"data/{today.year}/{today.month:02}"
        folder.mkdir(parents=True, exist_ok=True)

        # Yesterday prices are ~10% higher
        yesterday_coins = make_mock_coins(100, price_multiplier=1.12)
        yesterday_csv = folder / f"prices_{yesterday.strftime('%Y-%m-%d')}.csv"
        with open(yesterday_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["rank", "name", "symbol", "price"])
            for idx, coin in enumerate(yesterday_coins, start=1):
                writer.writerow([idx, coin["name"], coin["symbol"].upper(), coin["current_price"]])

        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        content = _today_diff_path(setup_dirs).read_text(encoding="utf-8")
        assert "🔽" in content

    @allure.story("New / Removed Entries")
    @allure.title("Diff file lists coins that are new in the top 100")
    def test_diff_lists_new_entries(self, setup_dirs, mock_coins):
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        folder = setup_dirs / f"data/{today.year}/{today.month:02}"
        folder.mkdir(parents=True, exist_ok=True)

        # Yesterday has different last coin
        yesterday_data = make_mock_coins(100)
        yesterday_data[-1]["symbol"] = "oldcoin"
        yesterday_csv = folder / f"prices_{yesterday.strftime('%Y-%m-%d')}.csv"
        with open(yesterday_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["rank", "name", "symbol", "price"])
            for idx, coin in enumerate(yesterday_data, start=1):
                writer.writerow([idx, coin["name"], coin["symbol"].upper(), coin["current_price"]])

        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        content = _today_diff_path(setup_dirs).read_text(encoding="utf-8")
        assert "🆕 New in Top 100" in content
        assert "COIN99" in content

    @allure.story("New / Removed Entries")
    @allure.title("Diff file lists coins removed from the top 100")
    def test_diff_lists_removed_entries(self, setup_dirs, mock_coins):
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        folder = setup_dirs / f"data/{today.year}/{today.month:02}"
        folder.mkdir(parents=True, exist_ok=True)

        # Yesterday has an extra coin (OLDCOIN) not present today
        yesterday_data = make_mock_coins(100)
        yesterday_data[-1]["symbol"] = "oldcoin"
        yesterday_csv = folder / f"prices_{yesterday.strftime('%Y-%m-%d')}.csv"
        with open(yesterday_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["rank", "name", "symbol", "price"])
            for idx, coin in enumerate(yesterday_data, start=1):
                writer.writerow([idx, coin["name"], coin["symbol"].upper(), coin["current_price"]])

        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = mock_coins
            fetch_top_100_cryptos()

        content = _today_diff_path(setup_dirs).read_text(encoding="utf-8")
        assert "❌ Removed from Top 100" in content
        assert "OLDCOIN" in content


# ---------------------------------------------------------------------------
# README update
# ---------------------------------------------------------------------------

@allure.feature("README Updater")
class TestReadmeUpdate:

    @allure.story("Marker Replacement")
    @allure.title("Summary text is inserted between AUTO-UPDATE markers")
    def test_summary_inserted_between_markers(self, setup_dirs):
        summary = "**Date:** 2026-04-08\n**Biggest gainer:** BTC ↑ 10.00%"

        with allure.step("Call update_readme_summary with a sample summary"):
            update_readme_summary(summary)

        content = (setup_dirs / "README.md").read_text(encoding="utf-8")
        assert summary in content

    @allure.story("Marker Replacement")
    @allure.title("Content outside the AUTO-UPDATE markers is preserved")
    def test_content_outside_markers_is_preserved(self, setup_dirs):
        update_readme_summary("Any summary")

        content = (setup_dirs / "README.md").read_text(encoding="utf-8")
        assert "# Crypto Daily Prices" in content

    @allure.story("Marker Replacement")
    @allure.title("AUTO-UPDATE markers are preserved in the README")
    def test_markers_are_preserved(self, setup_dirs):
        update_readme_summary("Any summary")

        content = (setup_dirs / "README.md").read_text(encoding="utf-8")
        assert "<!-- AUTO-UPDATE-START -->" in content
        assert "<!-- AUTO-UPDATE-END -->" in content

    @allure.story("Marker Replacement")
    @allure.title("Previous summary is replaced on subsequent updates")
    def test_previous_summary_is_replaced(self, setup_dirs):
        update_readme_summary("First summary")
        update_readme_summary("Second summary")

        content = (setup_dirs / "README.md").read_text(encoding="utf-8")
        assert "First summary" not in content
        assert "Second summary" in content
