#!/usr/bin/env bash
# Environment setup for Claude Code routines / GitHub Actions
set -e
python3 -m pip install --quiet playwright pillow requests
python3 -m playwright install --with-deps chromium
