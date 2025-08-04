# ai_volume_analyzer.py – IA autonome LNRC avec alertes Telegram
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_ADDRESS = os.getenv("CONTRACT_ADDRESS")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BSC_API_KEY = os.getenv("BSC_API_KEY")  # clé BscScan perso (gratuite)

DEXSCREENER_URL = f"https://api.dexscreener.com/latest/dex/pairs/bsc/{TOKEN_ADDRESS}"
BURN_ADDRESS = "0x000000000000000000000000000000000000dEaD"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[⚠️] Erreur Telegram : {e}")

def check_metrics():
    try:
        # 🔥 Lire burn via BscScan
        burn_url = f"https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={TOKEN_ADDRESS}&address={BURN_ADDRESS}&apikey={BSC_API_KEY}"
        burn_res = requests.get(burn_url).json()
        burn_amount = int(burn_res["result"]) / 1e18

        # 📊 Lire volume et prix via DexScreener
        dex = requests.get(DEXSCREENER_URL).json()
        volume_usd = float(dex["pair"]["volume"]["h24"])
        price_usd = float(dex["pair"]["priceUsd"])

        print(f"[IA] 🔥 Burn: {burn_amount:.2f} | Volume 24h: {volume_usd}$ | Prix: {price_usd}$")

        # 🚨 Conditions critiques
        if volume_usd < 500 or price_usd < 0.00001:
            send_telegram(f"⚠️ *Alerte LNRC IA* \n🔥 Burn: `{burn_amount:.2f}`\n📉 Volume faible: `{volume_usd}$`\n💸 Prix: `{price_usd}$`")

    except Exception as e:
        print(f"[ERREUR IA] {e}")
        send_telegram(f"❌ *Erreur IA LNRC* : `{e}`")

# 🔁 Boucle toutes les 15 minutes
if __name__ == "__main__":
    while True:
        check_metrics()
        time.sleep(900)  # 15 minutes
