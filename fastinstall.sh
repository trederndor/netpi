#!/bin/bash

set -e

# Directory di destinazione
TARGET_DIR="$HOME/netpi"

echo "[*] Creazione della cartella $TARGET_DIR..."
mkdir -p "$TARGET_DIR"

# Se esiste già una cartella .git dentro, rimuove tutto per evitare conflitti
if [ -d "$TARGET_DIR/.git" ]; then
    echo "[*] Cartella già esistente con repo git. Pulizia in corso..."
    rm -rf "$TARGET_DIR"
    mkdir -p "$TARGET_DIR"
fi

echo "[*] Clonazione del repository..."
git clone https://github.com/trederndor/netpi.git "$TARGET_DIR"

# Vai nella directory
cd "$TARGET_DIR"

# Rende eseguibile lo script di installazione se non lo è
chmod +x install.sh

echo "[*] Esecuzione di install.sh..."
./install.sh
