#!/bin/bash
set -e

echo "=== 🛠 INSTALLAZIONE DIPENDENZE SPEEDTEST MONITOR ==="

# Installa curl se non presente
if ! command -v curl &> /dev/null; then
    echo "⚠️ curl non trovato. Installazione in corso..."
    sudo apt-get update
    sudo apt-get install -y curl
else
    echo "✅ curl già installato"
fi

# Installa speedtest-cli ufficiale (Ookla)
if ! command -v speedtest &> /dev/null; then
    echo "⚡ Installazione speedtest-cli (Ookla)..."
    curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
    sudo apt-get install -y speedtest
    echo "✅ speedtest installato"
    # Accetta la licenza per non bloccare successivi speedtest

else
    echo "✅ speedtest-cli già installato"
fi

# Controlla Python 3
if command -v python3 &> /dev/null; then
    echo "✅ Python3 già installato"
else
    echo "⚠️ Python3 non trovato. Installazione in corso..."
    sudo apt update
    sudo apt install -y python3
fi

# Controlla pip
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 già installato"
else
    echo "⚠️ pip3 non trovato. Installazione in corso..."
    sudo apt install -y python3-pip
fi

# Installa dipendenze Python
echo "📦 Installazione dipendenze da requirements.txt"
pip install --break-system-packages --upgrade pip
pip install --break-system-packages -r requirements.txt
echo "✅ Tutto installato. Puoi ora avviare lo script Python!"
echo "Eseguire uno speedtest per accettare i termini di licenza e iniziare ad utilizzare il servizio"
