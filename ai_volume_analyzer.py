import os
import json
import logging
from datetime import datetime, timezone, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from web3 import Web3

# Charge .env.local si présent (usage local), sinon .env (Render)
if os.path.exists(".env.local"):
    load_dotenv(".env.local")
else:
    load_dotenv()

# ---------- Config ----------
RPC_URL = os.getenv("RPC_URL", "").strip()
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "").strip()
CONTRACT_ABI_PATH = os.getenv("CONTRACT_ABI", "").strip()  # ex: ai/abi/lnrc_testnet_abi.json

TOKEN_DECIMALS = int(os.getenv("TOKEN_DECIMALS", "18"))
TOKEN_TAX_RATE = float(os.getenv("TOKEN_TAX_RATE", "3"))  # 2% burn + 1% marketing => 3
TOKEN_GROSS_UP = os.getenv("TOKEN_GROSS_UP", "1").lower() in ("1", "true", "yes")

# Optionnel (si tu veux suivre des adresses précises)
BURN_WALLET = os.getenv("BURN_WALLET", "").strip()          # ex: 0x0000...dead
MARKETING_WALLET = os.getenv("MARKETING_WALLET", "").strip()

POLL_MINUTES = int(os.getenv("POLL_MINUTES", "10"))  # Fréquence d’analyse

# ---------- Logs ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def human_amount(raw):
    return raw / (10 ** TOKEN_DECIMALS)

def load_contract(w3: Web3):
    if not RPC_URL or not CONTRACT_ADDRESS or not CONTRACT_ABI_PATH:
        raise RuntimeError("Config manquante: RPC_URL / CONTRACT_ADDRESS / CONTRACT_ABI")

    with open(CONTRACT_ABI_PATH, "r", encoding="utf-8") as f:
        abi = json.load(f)

    address = Web3.to_checksum_address(CONTRACT_ADDRESS)
    return w3.eth.contract(address=address, abi=abi)

def analyze_contract():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        logging.error("Impossible de se connecter au RPC.")
        return

    contract = load_contract(w3)

    # --- totalSupply
    try:
        total_supply = contract.functions.totalSupply().call()
        logging.info(f"Total supply: {human_amount(total_supply):,.4f}")
    except Exception as e:
        logging.exception("Erreur lecture totalSupply: %s", e)

    # --- soldes optionnels
    try:
        if BURN_WALLET:
            burn_bal = contract.functions.balanceOf(Web3.to_checksum_address(BURN_WALLET)).call()
            logging.info(f"Burn wallet balance: {human_amount(burn_bal):,.4f}")

        if MARKETING_WALLET:
            mkt_bal = contract.functions.balanceOf(Web3.to_checksum_address(MARKETING_WALLET)).call()
            logging.info(f"Marketing wallet balance: {human_amount(mkt_bal):,.4f}")
    except Exception as e:
        logging.exception("Erreur lecture balances: %s", e)

    # --- activité sur les N derniers blocs (Transfers)
    try:
        current_block = w3.eth.block_number
        lookback_blocks = 500  # tu peux adapter
        from_block = max(current_block - lookback_blocks, 1)

        topic_transfer = w3.keccak(text="Transfer(address,address,uint256)").hex()
        logs = w3.eth.get_logs({
            "fromBlock": from_block,
            "toBlock": current_block,
            "address": Web3.to_checksum_address(CONTRACT_ADDRESS),
            "topics": [topic_transfer]
        })
        logging.info(f"Transfers (≈{lookback_blocks} blocs): {len(logs)} événements")
    except Exception as e:
        logging.exception("Erreur lecture logs Transfer: %s", e)

    # --- rappel params
    logging.info(f"Params fiscaux: TAX={TOKEN_TAX_RATE}% | gross_up={TOKEN_GROSS_UP}")

def main():
    logging.info("🧠 IA LNRC — monitoring démarré")
    analyze_contract()  # 1ère exécution immédiate

    scheduler = BlockingScheduler(timezone=timezone.utc)
    scheduler.add_job(analyze_contract, "interval", minutes=POLL_MINUTES, next_run_time=datetime.now(timezone.utc) + timedelta(minutes=POLL_MINUTES))
    scheduler.start()

if __name__ == "__main__":
    main()
