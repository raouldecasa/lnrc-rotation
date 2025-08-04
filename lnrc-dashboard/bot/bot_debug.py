import os
import time
from web3 import Web3
import requests
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
WALLETS = [os.getenv(f"WALLET_{i}") for i in range(1, 5)]
PKS = [os.getenv(f"PK_{i}") for i in range(1, 5)]

# Initialisation Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Erreur Telegram : {response.text}")
        else:
            print("✅ Message Telegram envoyé.")
    except Exception as e:
        print(f"Erreur d'envoi Telegram : {e}")

def check_debug():
    send_telegram("🟢 LNRC Bot Debug lancé avec succès.")

    # Test de connexion Web3
    if web3.is_connected():
        send_telegram("✅ Web3 connecté avec succès.")
    else:
        send_telegram("❌ Échec de la connexion Web3.")
        return

    # Vérifie le contrat
    if not web3.is_address(CONTRACT_ADDRESS):
        send_telegram("⚠️ Adresse du contrat invalide.")
        return

    # Vérifie les wallets
    for i, wallet in enumerate(WALLETS, 1):
        if not web3.is_address(wallet):
            send_telegram(f"⚠️ WALLET_{i} invalide : {wallet}")
        else:
            balance = web3.eth.get_balance(wallet)
            balance_eth = web3.from_wei(balance, 'ether')
            send_telegram(f"💰 WALLET_{i} balance : {balance_eth:.5f} BNB")

    # Vérifie les clés privées
    for i, pk in enumerate(PKS, 1):
        if not pk or len(pk) < 64:
            send_telegram(f"⚠️ Clé privée PK_{i} manquante ou invalide.")

    send_telegram("🔍 Fin des vérifications LNRC bot_debug ✅")

if __name__ == "__main__":
    check_debug()
