#!/bin/bash
set -e

VIDEO="${1:-watermarked.dwv}"
LEN="${2:-17}"
KEY="${3:-7301}"

echo "[1] Extracting original"
ORIGINAL="$(python dew_extract.py --in "$VIDEO" --length "$LEN" --key "$KEY")"
echo "$ORIGINAL"
if [ "$ORIGINAL" = "DEW-EVIDENCE-2026" ]; then
    echo "VERIFY_ORIGINAL=Y"
else
    echo "VERIFY_ORIGINAL=N"
fi

echo "[2] Applying mild compression-like quantization"
python attack.py --in "$VIDEO" --out attacked.dwv --step 4

echo "[3] Extracting attacked video"
ATTACKED="$(python dew_extract.py --in attacked.dwv --length "$LEN" --key "$KEY")"
echo "$ATTACKED"
if [ "$ATTACKED" = "DEW-EVIDENCE-2026" ]; then
    echo "VERIFY_ATTACKED=Y"
else
    echo "VERIFY_ATTACKED=N"
fi

echo "[done]"
