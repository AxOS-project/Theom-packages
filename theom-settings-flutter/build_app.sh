#!/bin/bash

set -e

# Build
flutter build linux --release

# Copy
cp -r ./build/linux/x64/release/bundle/ ./bundle