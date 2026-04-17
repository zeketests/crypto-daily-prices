# 🪙 Crypto Weekly Prices

Automatically fetches the top 100 crypto prices weekly from CoinGecko, stores them in `.csv`, and tracks changes over time.

## 📅 Latest Update
<!-- AUTO-UPDATE-START -->
**Date:** 2026-04-10  
**Biggest gainer:** ZEC ↑ 20.06%  
**Biggest loser:** TAO ↓ 17.12%  
**New entries:** DASH, SIREN  
**Removed:** CAKE, TUSD
<!-- AUTO-UPDATE-END -->

## 📁 Folder structure

Files are saved under `data/YYYY/MM/` and include:
- `prices_YYYY-MM-DD.csv`
- `diff_YYYY-MM-DD.txt` (if previous day's data exists)

## ⚙️ How it works

- Weekly GitHub Actions job runs at 12:00 UTC
- `.csv` with top 100 cryptos saved in `/data/`
- Differences from previous week are tracked
- README is auto-updated with latest summary

---

Powered by automation. No hands needed!
