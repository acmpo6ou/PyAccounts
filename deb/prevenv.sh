#!/bin/bash

if [ ! -d "deb/pyaccounts" ]; then
  python3 -m venv deb/pyaccounts
  source deb/pyaccounts/bin/activate
  pip install -U pip setuptools
fi

source deb/pyaccounts/bin/activate
pip install -r requirements.txt
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
find . \( -name "*.exe" \) -type f -delete
