#!/usr/bin/env bash

cd ~/Documents/PyAccounts || exit
source venv/bin/activate
GTK_THEME=Adwaita:dark XDG_DATA_DIRS=./share ./PyAccounts.py
