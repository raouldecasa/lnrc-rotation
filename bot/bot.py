import os
import time
import random
from dotenv import load_dotenv
from web3 import Web3
import telebot

# Chargement des variables d'environnement
load_dotenv()

print("📦 Chargement des variables...")

RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

WALLETS = [
    os.getenv("WALLET_1"),
    os.getenv("WALLET_2"),
    os.getenv("WALLET_3"),
    os.getenv("WALLET_4"),
]

PKS = [
    os.getenv("PK_1"),
    os.getenv("PK_2"),
    os.getenv("PK_3"),
    os.getenv("PK_4"),
]

MARKETING_WALLET = "0x55EbBd2dDCf4D4FB0bbbE91615E8bF6668D6f89a"

if not all([RPC_URL, CONTRACT_ADDRESS, BOT_TOKEN, CHAT_ID] + WALLETS + PKS):
    print("❌ Une ou plusieurs variables d'environnement sont manquantes.")
    exit()

w3 = Web3(Web3.HTTPProvider(RPC_URL))
bot = telebot.TeleBot(BOT_TOKEN)

# Interface du token LNRC (ERC20 compatible)
ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]

token_contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)

def send_telegram(msg):
    try:
        bot.send_message(CHAT_ID, msg)
    except Exception as e:
        print("Telegram Error:", e)

def rotate_tokens():
    print("🔁 Rotation LNRC initialisée.")
    while True:
        try:
            for i in range(4):
                sender = Web3.to_checksum_address(WALLETS[i])
                receiver = Web3.to_checksum_address(WALLETS[(i + 1) % 4])
                private_key = PKS[i]

                # Détermine le montant à transférer (exemple : 100_000 tokens * 10**18)
                balance = token_contract.functions.balanceOf(sender).call()
                if balance == 0:
                    print(f"❌ Wallet {i+1} n'a aucun token.")
                    continue

                amount = int(balance * 0.97)  # On garde 3% pour burn + marketing
                burn_amount = int(balance * 0.02)
                marketing_amount = int(balance * 0.01)

                nonce = w3.eth.get_transaction_count(sender)
                gas_price = w3.eth.gas_price

                # 1. Transfert principal (97 %)
                tx = token_contract.functions.transfer(receiver, amount).build_transaction({
                    'chainId': 97,
                    'gas': 100000,
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
                signed_tx = w3.eth.account.sign_transaction(tx, private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

                # 2. Burn (vers 0x000...dead)
                nonce += 1
                burn_tx = token_contract.functions.transfer(
                    "0x000000000000000000000000000000000000dEaD", burn_amount
                ).build_transaction({
                    'chainId': 97,
                    'gas': 100000,
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
                signed_burn_tx = w3.eth.account.sign_transaction(burn_tx, private_key)
                burn_tx_hash = w3.eth.send_raw_transaction(signed_burn_tx.rawTransaction)

                # 3. Marketing
                nonce += 1
                marketing_tx = token_contract.functions.transfer(
                    MARKETING_WALLET, marketing_amount
                ).build_transaction({
                    'chainId': 97,
                    'gas': 100000,
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
                signed_marketing_tx = w3.eth.account.sign_transaction(marketing_tx, private_key)
                marketing_tx_hash = w3.eth.send_raw_transaction(signed_marketing_tx.rawTransaction)

                # Logs
                msg = (
                    f"🔁 Rotation {i+1}/4 effectuée\n"
                    f"👛 De : {sender[:6]}...{sender[-4:]}\n"
                    f"📥 Vers : {receiver[:6]}...{receiver[-4:]}\n"
                    f"💸 Montant : {w3.from_wei(amount, 'ether')} LNRC\n"
                    f"🔥 Burn : {w3.from_wei(burn_amount, 'ether')} LNRC\n"
                    f"💼 Marketing : {w3.from_wei(marketing_amount, 'ether')} LNRC\n"
                    f"🔗 Tx hash : {w3.to_hex(tx_hash)}"
                )
                print(msg)
                send_telegram(msg)

            print("✅ Rotation complète. Pause 20 minutes ⏳\n")
            time.sleep(20 * 60)

        except Exception as e:
            print("❌ Erreur rotation :", e)
            send_telegram(f"❌ Erreur bot rotation : {e}")
            time.sleep(60)

# Lancement
if __name__ == "__main__":
    print("🚀 Bot LNRC démarré ✅")
    rotate_tokens()
