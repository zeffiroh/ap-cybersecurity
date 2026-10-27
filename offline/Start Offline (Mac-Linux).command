#!/bin/sh
# Double-click (Mac) or run (Linux) to use the whole course offline on this computer.
cd "$(dirname "$0")" || exit 1
exec python3 serve.py
