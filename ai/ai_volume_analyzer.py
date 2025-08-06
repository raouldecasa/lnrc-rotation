import os
import time
import logging
import requests
from dotenv import load_dotenv
from web3 import Web3
from apscheduler.schedulers.blocking import BlockingScheduler

# Chargement des variables d'environnement
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = Web3.to_checksum_address(os.getenv("CONTRACT_ADDRESS"))

# Connexion Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Charger l'ABI du contrat
with open("bot/abi.json") as f:
    abi = f.read()

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

# Fonction pour envoyer un message Telegram
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            logging.info("✅ Alerte envoyée à Telegram.")
        else:
            logging.warning(f"⚠️ Erreur Telegram: {response.text}")
    except Exception as e:
        logging.error(f"❌ Erreur d'envoi Telegram : {e}")

# Analyseur IA simplifié
def analyze_contract():
    try:
        total_supply = contract.functions.totalSupply().call()
        burn_address = "0x000000000000000000000000000000000000dEaD"
        burn_balance = contract.functions.balanceOf(burn_address).call()
        burn_percentage = (burn_balance / total_supply) * 100

        logging.info(f"📊 Total Supply : {total_supply / 1e18:.2f} LNRC")
        logging.info(f"🔥 Tokens Burn : {burn_balance / 1e18:.2f} LNRC ({burn_percentage:.2f}%)")

        if burn_percentage > 30:
            send_telegram_alert(f"🔥 Le burn LNRC dépasse {burn_percentage:.2f}% !")
        else:
            logging.info("ℹ️ Le burn LNRC est sous contrôle.")
    except Exception as e:
        logging.error(f"❌ Erreur analyse IA : {e}")

# Planification
scheduler = BlockingScheduler()
scheduler.add_job(analyze_contract, "interval", minutes=5)

if __name__ == "__main__":
    logging.info("🤖 IA de surveillance LNRC activée.")
    analyze_contract()
    scheduler.start()
