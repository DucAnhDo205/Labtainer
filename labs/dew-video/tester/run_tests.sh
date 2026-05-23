#!/bin/bash
set -e

VIDEO="${1:-watermarked.dwv}"
LEN="${2:-18}"
KEY="${3:-4242}"

echo "[1] Extracting original"
python dew_extract.py --in "$VIDEO" --length "$LEN" --key "$KEY"

echo "[2] Applying mild compression-like quantization"
python attack.py --in "$VIDEO" --out attacked.dwv --step 4

echo "[3] Extracting attacked video"
python dew_extract.py --in attacked.dwv --length "$LEN" --key "$KEY"

echo "[done]"
