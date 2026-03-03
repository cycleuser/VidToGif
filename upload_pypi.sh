#!/usr/bin/env bash
# Upload vidtogif to PyPI
# Prerequisites: pip install build twine

set -e

echo "=== Cleaning old build artifacts ==="
rm -rf dist/ build/ vidtogif.egg-info/

echo "=== Building package ==="
python -m build

echo "=== Uploading to PyPI ==="
python -m twine upload dist/*

echo "=== Done! Package uploaded to PyPI ==="
