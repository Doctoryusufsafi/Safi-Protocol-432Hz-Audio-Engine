#!/bin/bash
echo "SAFI PROTOCOL DSP ENGINE v5.0 - Omerta Music Research"
echo "64-bit Linear Phase Offline Mastering"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
python3 -c "import numpy,scipy" 2>/dev/null || python3 -m pip install numpy scipy
export PYTHONIOENCODING=utf-8
python3 safi_app_v5.py
