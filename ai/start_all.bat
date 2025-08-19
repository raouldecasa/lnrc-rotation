@echo off
setlocal

REM -- Vérifier les dossiers et fichiers --
if not exist "ai\ai_volume_analyzer.py" (
    echo [ERREUR] Fichier ai\ai_volume_analyzer.py introuvable.
    pause
    exit /b 1
)
if not exist "rotation-js\bsc_rotation_bot.js" (
    echo [ERREUR] Fichier rotation-js\bsc_rotation_bot.js introuvable.
    pause
    exit /b 1
)

REM -- Lancer l'IA Monitoring (log automatique) --
echo ==== [LNRC] IA Monitoring... ====
cd ai
start cmd /k "python ai_volume_analyzer.py > ..\logs\ia.log 2>&1"
cd ..

REM -- Lancer le Bot Rotation (log automatique) --
echo ==== [LNRC] Bot Rotation... ====
cd rotation-js
start cmd /k "node bsc_rotation_bot.js > ..\logs\rotation.log 2>&1"
cd ..

echo ==== Tout est lancé ! Les logs sont dans le dossier /logs ====
pause
