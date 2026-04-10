#!/bin/bash
set -e

TYPE="${1:-minor}"
COMMENT="${2:-}"

if [[ "$TYPE" != "major" && "$TYPE" != "minor" && "$TYPE" != "patch" ]]; then
    echo "Errore: tipo release deve essere major, minor o patch (default: minor)"
    exit 1
fi

# Recupera l'ultimo tag, default a 0.0.0 se nessuno
LAST_TAG=$(git tag --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | head -n1)
if [[ -z "$LAST_TAG" ]]; then
    LAST_TAG="v0.0.0"
    echo "Nessun tag trovato, parto da $LAST_TAG"
else
    echo "Ultimo tag: $LAST_TAG"
fi

# Estrae major, minor, patch
VERSION="${LAST_TAG#v}"
MAJOR=$(echo "$VERSION" | cut -d. -f1)
MINOR=$(echo "$VERSION" | cut -d. -f2)
PATCH=$(echo "$VERSION" | cut -d. -f3)

# Incrementa la versione corretta
case "$TYPE" in
    major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
    minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
    patch) PATCH=$((PATCH + 1)) ;;
esac

NEW_TAG="v${MAJOR}.${MINOR}.${PATCH}"
echo "Nuovo tag: $NEW_TAG"

# Recupera l'ultimo commit su main
MAIN_COMMIT=$(git rev-parse origin/main)
echo "Commit: $MAIN_COMMIT"

# Crea il tag sull'ultimo commit di main (con o senza messaggio)
if [[ -n "$COMMENT" ]]; then
    git tag -a "$NEW_TAG" "$MAIN_COMMIT" -m "$COMMENT"
else
    git tag -a "$NEW_TAG" "$MAIN_COMMIT" -m "$NEW_TAG"
fi

git push origin "$NEW_TAG"
echo "Tag $NEW_TAG pushato su GitHub. La release verrà creata automaticamente dalla pipeline."