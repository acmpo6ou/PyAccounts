#!/bin/bash

cd /usr/share/pyaccounts/PyAccounts
source ../bin/activate
python3.9 PyAccounts.py "$@" 2>/tmp/`date +'%d-%m-%Y_%H:%M:%S'`-PyAccounts.log
