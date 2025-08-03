import time
import traceback
from web3 import Web3
from telegram import Bot

# ✅ Chargement sécurisé des variables d’environnement
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
RPC_URL = os.getenv("RPC_URL")

bot = Bot(token=BOT_TOKEN)
web3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=[])

# ✅ Logique principale d’IA de surveillance
def start_monitoring():
    while True:
        try:
            # 🔎 Exemple de vérification d’activité du contrat
            latest_block = web3.eth.block_number
            print(f"[AI Monitor] Bloc actuel : {latest_block}")
            
            # 🔔 Simule une alerte
            bot.send_message(chat_id=CHAT_ID, text=f"[AI MONITOR] Bloc actuel : {latest_block}")
            
            # ⏱️ Pause de 60s entre chaque check
            time.sleep(60)
        
        except Exception as inner_error:
            error_details = traceback.format_exc()
            print(f"[AI ERROR] Erreur pendant la surveillance :\n{error_details}")
            bot.send_message(chat_id=CHAT_ID, text=f"[ALERTE] Une erreur est survenue dans AI_MONITOR 🤖\n{inner_error}")
            time.sleep(30)  # évite la boucle d’erreur infinie

# ✅ Protection globale anti-crash
if __name__ == "__main__":
    try:
        print("[AI MONITOR] Démarrage de la surveillance sécurisée LNRC 🛡️")
        start_monitoring()
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"[FATAL ERROR] Impossible de démarrer AI_MONITOR:\n{error_trace}")
        bot.send_message(chat_id=CHAT_ID, text=f"🚨 [FATAL] AI_MONITOR a crashé dès le lancement\n{e}")
