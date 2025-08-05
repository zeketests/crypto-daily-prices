# 🪙 Crypto Daily Prices

This repo automatically fetches the top 100 cryptocurrencies from CoinGecko every day and saves their prices in `.csv` format.

It also generates a daily diff file showing:

- 🔼 Price increases > 5%
- 🔽 Price drops > 5%
- 🆕 New entries in the Top 100
- ❌ Removed coins

All data is stored in the `data/YYYY/MM/` folder.

Automation is handled via GitHub Actions. No manual work needed.
