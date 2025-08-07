#!/usr/bin/env bash
set -euo pipefail

TARGET="$HOME/netpi"
REPO_URL="https://github.com/trederndor/netpi.git"
INSTALLER="install.sh"  # <-- cambia qui se il file si chiama diversamente!

echo "▶ Creazione cartella di destinazione: $TARGET"
rm -rf "$TARGET"
git clone "$REPO_URL" "$TARGET"

cd "$TARGET"

if [[ ! -f "$INSTALLER" ]]; then
    echo "❌ Errore: $INSTALLER non trovato. Verifica che esista nel repository."
    echo "🧩 Contenuto della cartella:"
    ls -la
    exit 1
fi

echo "▶ Rendo eseguibile lo script di installazione"
chmod +x "$INSTALLER"

echo "▶ Avvio dell’installer..."
bash "$INSTALLER"

echo "✅ Installazione completata in $TARGET"
