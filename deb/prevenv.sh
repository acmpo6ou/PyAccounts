#!/bin/bash

if [ ! -d "deb/pyaccounts" ]; then
  python3.10 -m venv deb/pyaccounts
  source deb/pyaccounts/bin/activate
  pip install -U pip
  pip install -U setuptools
  pip install -U wheel
fi

source deb/pyaccounts/bin/activate
pip install -r requirements.txt

# remove .pyc, .pyo and .exe files and __pycache__ directories
find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
find . \( -name "*.exe" \) -type f -delete

# fix some venv paths to make the venv portable
REPSTR="$HOME/Documents/PyAccounts/deb/pyaccounts/"
grep -rl "$REPSTR" deb/pyaccounts | xargs sed -i "s;$REPSTR;/usr/share/pyaccounts/;g"

# remove dangling links
rm deb/pyaccounts/bin/python deb/pyaccounts/bin/python3
