# STALKER6900 STALK Bot 🔍

This version of the EARN6900X bot uses token data filtered from **Stalk.fun**, giving you sniper-level alerts on tokens that already passed basic rug filters and volume thresholds.

## Features

- Pulls data from Stalk.fun's frontend (scrape or mirror)
- Applies winrate + stalk_score algorithm
- Only alerts tokens with:
  - ✅ Good momentum (buys > sells)
  - ✅ Decentralized holder base
  - ✅ Locked liquidity
  - ✅ Spike in volume / hype

## Setup

1. Set your Telegram bot token and chat ID:
   Create a `.env` file:
   ```
   BOT_TOKEN=your_telegram_bot_token
   CHAT_ID=your_chat_id
   ```
2. Run with:
   ```bash
   pip install python-telegram-bot requests
   python earn6900x_stalk.py
   ```

## Requirements

- Python 3.8+
- python-telegram-bot==13.15
- requests
