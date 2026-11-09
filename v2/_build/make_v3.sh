#!/bin/sh
# Builds v2 (plain) and v3 (glass) from the same source.
set -e
cd "$(dirname "$0")/../.."
python3 v2/_build/build.py
mkdir -p v3/assets
rm -rf v3/assets && mkdir -p v3 && cp -r v2/assets v3/assets
cp v2/_build/glass.css v3/assets/glass.css
PD_OUT="$(pwd)/v3" python3 v2/_build/build.py
