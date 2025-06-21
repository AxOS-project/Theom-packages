#!/bin/bash

set -e

if [ $1 = "--fresh" ]; then
    flutter clean
fi

# Build
flutter build linux --release

# Copy
cp -r ./build/linux/x64/release/bundle/ ./