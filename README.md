# 🪙 Crypto Daily Prices

Automatically fetches the top 100 crypto prices daily from CoinGecko, stores them in `.csv`, and tracks changes over time.

## 📅 Latest Update
<!-- AUTO-UPDATE-START -->
**Date:** 2025-08-11  
**Biggest gainer:** ENA ↑ 5.75%  
**Biggest loser:** HASH ↓ 7.00%  
**New entries:** LDO  
**Removed:** EZETH
<!-- AUTO-UPDATE-END -->

## 📁 Folder structure

Files are saved under `data/YYYY/MM/` and include:
- `prices_YYYY-MM-DD.csv`
- `diff_YYYY-MM-DD.txt` (if previous day's data exists)

## ⚙️ How it works

- Daily GitHub Actions job runs at 12:00 UTC
- `.csv` with top 100 cryptos saved in `/data/`
- Differences from previous day are tracked
- README is auto-updated with latest summary

---

Powered by automation. No hands needed!