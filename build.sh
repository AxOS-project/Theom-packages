#!/bin/bash

set -e

OUTDIR="./out"
mkdir -p "$OUTDIR"

GREEN='\033[0;32m'
NC='\033[0m' # No Color

FILE=$1

if [ "$1" == "" ]; then
    echo "Invalid use of build.sh"
    exit 1
fi

if [ -f "${FILE}/PKGBUILD" ]; then
    echo -e "${GREEN}==> Building package in $FILE${NC}"
    pushd "$FILE" > /dev/null
    [ -d "$(pwd)/src/lib/__pycache__/" ] && rm -r "$(pwd)/src/lib/__pycache__/"
    makepkg -fs --noconfirm --nodeps
    rm -r pkg/
    mv ./*.pkg.tar.zst "../$OUTDIR/"
    popd > /dev/null
fi

echo -e "${GREEN}$FILE built and moved to $OUTDIR${NC}"
notify-send "$FILE built" "$FILE have been built and moved to $OUTDIR" -a "Theom packages"