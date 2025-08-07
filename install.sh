#!/bin/bash
set -e
echo "=== 🛠 INSTALLAZIONE DIPENDENZE SPEEDTEST MONITOR ==="
# === Controlla Python 3 ===
if command -v python3 &> /dev/null; then
    echo "✅ Python3 già installato"
else
    echo "⚠️ Python3 non trovato. Installazione in corso..."
    sudo apt update
    sudo apt install -y python3
fi
# === Controlla pip ===
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 già installato"
else
    echo "⚠️ pip3 non trovato. Installazione in corso..."
    sudo apt install -y python3-pip
fi
# === Controlla virtualenv (opzionale ma utile) ===
#if ! python3 -m pip show virtualenv &> /dev/null; then
#    echo "➕ Installazione virtualenv"
#    python3 -m pip install --break-system-packages virtualenv
#fi
# === Crea venv (opzionale) ===
#if [ ! -d "venv" ]; then
#    echo "🌀 Creo ambiente virtuale Python..."
#    python3 -m virtualenv venv
#fi
# === Attiva virtualenv ===
#source venv/bin/activate
# === Installa dipendenze dal file requirements.txt ===
echo "📦 Installazione dipendenze da requirements.txt"
pip install --break-system-packages --upgrade pip
pip install --break-system-packages -r requirements.txt
echo "✅ Tutto installato. Puoi ora avviare lo script Python!"
