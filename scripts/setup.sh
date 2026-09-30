#!/usr/bin/env bash
# Environment setup for Claude Code routines / GitHub Actions
set -e
python3 -m pip install --quiet playwright pillow requests
python3 -m playwright install chromium
# System libraries only if Chromium can't start yet. Not via --with-deps unconditionally:
# apt-get update fails on cloud images whose extra PPAs are blocked by the network allowlist.
if ! python3 -c "from playwright.sync_api import sync_playwright as p; pw=p().start(); pw.chromium.launch().close(); pw.stop()" 2>/dev/null; then
  echo "Chromium can't launch yet, installing system dependencies"
  python3 -m playwright install-deps chromium
fi
echo "setup ok: Chromium launches"
