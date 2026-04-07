#!/bin/bash
set -e

SRC="$(dirname "$0")/translated/ExampleLanguage"
DEST="/mnt/c/Program Files (x86)/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ExampleLanguage"

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
