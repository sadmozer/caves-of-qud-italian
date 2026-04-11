#!/bin/bash
set -e

SRC="$(dirname "$0")/../ItalianLanguage"
DEST="/mnt/c/Users/%USERPROFILE%/AppData/LocalLow/Freehold Games/CavesOfQud/Mods"

if [[ ! -d "$SRC" ]]; then
    echo "Errore: cartella sorgente non trovata: $SRC"
    exit 1
fi

if [[ ! -d "$DEST" ]]; then
    echo "Errore: cartella di destinazione non trovata: $DEST"
    echo "Assicurati che Caves of Qud sia installato in Steam."
    exit 1
fi

echo "Copia file da:"
echo "  $SRC"
echo "verso:"
echo "  $DEST"
echo ""

cp -v "$SRC"/* "$DEST"/

echo ""
echo "Installazione completata."