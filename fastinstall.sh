#!/usr/bin/env bash
set -euo pipefail

START_DIR="$(pwd)"
TARGET="$HOME/netpi"
REPO_RAW="https://raw.githubusercontent.com/trederndor/netpi/main"
INSTALLER="installer.sh"

echo "▶ Creazione cartella di destinazione: $TARGET"
rm -rf "$TARGET"
mkdir -p "$TARGET"

echo "▶ Scarico il progetto e lo script di installazione"
cd "$TARGET"
curl -sSL "$REPO_RAW/$INSTALLER" -o "$INSTALLER"
curl -sSL "$REPO_RAW/other_files.zip" -o source.zip  # se serve

echo "▶ Rendo eseguibile l’installer"
chmod +x "$INSTALLER"

echo "▶ Eseguo lo script di setup"
./"$INSTALLER"

echo "✅ Installazione completata in $TARGET"
cd "$START_DIR"
