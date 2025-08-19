# 🦁 Le Noble Roi Chat (LNRC) - Rotation & Monitoring

Ce projet regroupe plusieurs services automatisés autour du **token LNRC** sur la Binance Smart Chain (BSC).  
Il inclut un bot de rotation des wallets, une IA de monitoring et un bot Telegram.  

---

## 📂 Structure du projet

lnrc-rotation/
│
├── ai/                        # IA de monitoring LNRC
│   ├── ai_volume_analyzer.py   # Analyse du burn, volume, prix LNRC
│   ├── requirements.txt        # Dépendances Python
│
├── rotation-js/                # Bot de rotation (Node.js)
│   ├── bsc_rotation_bot.js     # Script principal
│   ├── package.json            # Dépendances Node.js
│   ├── .env.example            # Exemple de configuration
│   ├── README.md               # Documentation rotation bot
│
├── bot/                        # Bot Telegram LNRC (optionnel)
│   ├── bot.py
│   ├── requirements.txt
│
├── render.yaml                 # Configuration Render pour déploiement
└── README.md                   # Ce fichier (documentation globale)

---

## 🚀 Services inclus

### 🔹 1. IA Monitoring (Python)
- Analyse le **burn, le volume et le prix LNRC**.
- Déclenche des alertes (Telegram/logs).
- S’exécute automatiquement avec un scheduler.

### 🔹 2. Bot Rotation (Node.js)
- Effectue **~20 transactions/jour** entre 4 wallets.
- Applique les taxes du smart contract (2% burn, 1% marketing).
- Génère du volume de manière réaliste avec des montants aléatoires.

### 🔹 3. Bot Telegram (optionnel)
- Commandes `/balance`, `/wallets`, `/price`, `/burn`, `/stats`.
- Connexion directe au smart contract LNRC.
- Notifications en temps réel.

---

## ⚙️ Déploiement sur Render

1. Pousser le repo sur GitHub :
```bash
git add .
git commit -m "Initial LNRC rotation project"
git push origin main
