@echo off
taskkill /F /IM python.exe /T
taskkill /F /IM node.exe /T
echo [LNRC] Tous les services sont stoppés.
pause
