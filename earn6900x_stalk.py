import os
import requests
import time
from datetime import datetime
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# === Simulated Stalk.fun Fetch ===
def fetch_stalk_tokens():
    url = "https://stalk.fun/api/tokens"  # Placeholder: replace with real endpoint if available
    try:
        res = requests.get(url).json()
        return [t for t in res if (datetime.utcnow().timestamp() - t['launch_timestamp']) < 900]
    except:
        return []

# === Scoring ===
def predict_winrate(token):
    buys = token.get('buy_count', 0)
    sells = token.get('sell_count', 0)
    holders = token.get('holder_count', 0)
    lp_locked = token.get('is_lp_locked', False)

    buy_pressure = buys / (sells + 1)
    hold_rate = holders / (buys + sells + 1)
    lp_trust = 1 if lp_locked else 0.6
    time_decay = (datetime.utcnow().timestamp() - token['launch_timestamp']) / 600

    winrate = (buy_pressure * hold_rate * lp_trust) / (time_decay + 1)
    return round(min(winrate * 100, 100), 2)

def stalk_score(token):
    buys = token['buy_count']
    sells = token['sell_count']
    holders = token['holder_count']
    volume = token.get('volume_5m', 1000)
    lp_locked = token.get('is_lp_locked', False)
    age_minutes = (datetime.utcnow().timestamp() - token['launch_timestamp']) / 60
    whale_risk = token.get('top_wallet_percent', 0.2)

    buy_pressure = buys / (sells + 1)
    holder_ratio = holders / (buys + sells + 1)
    lp_bonus = 1.2 if lp_locked else 0.6
    whale_penalty = 0.5 if whale_risk > 0.3 else 1.0

    score = (buy_pressure * holder_ratio * lp_bonus * whale_penalty * volume) / (age_minutes + 1)
    return round(min(score, 1000), 2)

def send_alert(token, winrate, stalkscore, cap):
    msg = f"""
🚨 *EARN6900X STALK SIGNAL* 🚨

Name: *{token['name']}*
Market Cap: ${int(cap):,}
Winrate: *{winrate}%*
StalkScore: *{stalkscore}*

[View on Pump.fun](https://pump.fun/{token['id']})
"""
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")

def main():
    while True:
        tokens = fetch_stalk_tokens()
        for token in tokens:
            winrate = predict_winrate(token)
            score = stalk_score(token)
            cap = token.get('market_cap', 0)
            if winrate > 75 and score > 150 and cap < 1000000:
                send_alert(token, winrate, score, cap)
        time.sleep(60)

if __name__ == "__main__":
    main()
