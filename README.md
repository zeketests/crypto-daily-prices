# 🪙 Crypto Daily Prices

Automatically fetches the top 100 crypto prices daily from CoinGecko, stores them in `.csv`, and tracks changes over time.

## 📅 Latest Update
<!-- AUTO-UPDATE-START -->
**Date:** 2026-02-04  
**Biggest gainer:** WLFI ↑ 5.61%  
**Biggest loser:** HYPE ↓ 9.92%  
**New entries:** USTB, NIGHT, FIL, NEXO, RENDER, ARB, VET, JAAA, MORPHO, USDY, XDC, OUSG, EUTBL, BONK, BDX, JUP, USDAI, USD0, SEI, JTRSY, STX, DASH, CAKE  
**Removed:** LBTC, USDT0, SUSDE, RSETH, RETH, BSC-USD, WBNB, SYRUPUSDC, USDC.E, CBBTC, WETH, WBETH, WEETH, STETH, WSTETH, JLP, WBTC, BNSOL, FBTC, JITOSOL
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