#!/bin/bash
set -e

# Assicura di eseguire come root (per installare git)
if [ "$EUID" -ne 0 ]; then
  echo "⚠️ Lo script necessita dei permessi di root. Ri-eseguo con sudo..."
  exec sudo bash "$0" "$@"
fi

# Installa git se non c'è
if ! command -v git &> /dev/null; then
  echo "⚠️ git non trovato. Installazione in corso..."
  apt-get update
  apt-get install -y git
else
  echo "✅ git già installato"
fi

TARGET_DIR="/root/netpi"
echo "[*] Creazione della cartella $TARGET_DIR..."
mkdir -p "$TARGET_DIR"

echo "[*] Clonazione del repository..."
git clone https://github.com/trederndor/netpi.git "$TARGET_DIR"

cd "$TARGET_DIR"

chmod +x install.sh
echo "[*] Esecuzione di install.sh..."
./install.sh
