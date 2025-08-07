#!/usr/bin/env bash
set -euo pipefail

TARGET="$HOME/netpi"
REPO_RAW="https://raw.githubusercontent.com/trederndor/netpi/main"
INSTALLER="installer.sh"

echo "▶ Creazione cartella di destinazione: $TARGET"
rm -rf "$TARGET"
mkdir -p "$TARGET"

echo "▶ Scarico il progetto e lo script di installazione"
cd "$TARGET"
curl -sSL "$REPO_RAW/$INSTALLER" -o install.sh
curl -sSL "$REPO_RAW/other_files.zip" -o source.zip  # se hai più file, oppure usa git clone

echo "▶ Rendo eseguibile l’installer"
chmod +x install.sh

echo "▶ Eseguo lo script di setup"
./install.sh

echo "✅ Installazione completata in $TARGET"
