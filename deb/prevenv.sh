#!/bin/bash

if [ ! -d "deb/pyaccounts" ]; then
  python3 -m venv deb/pyaccounts
  source deb/pyaccounts/bin/activate
  pip install -U pip
  pip install -U setuptools
  pip install -U wheel
fi

source deb/pyaccounts/bin/activate
pip install -r requirements.txt

find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
find . \( -name "*.exe" \) -type f -delete

REPSTR="$HOME/Documents/PyAccounts/deb/pyaccounts/"
grep -rl "$REPSTR" deb/pyaccounts | xargs sed -i "s;$REPSTR;/usr/share/pyaccounts/;g"
