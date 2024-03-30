#!/usr/bin/env bash

cd ~/Documents/PyAccounts || exit
source venv/bin/activate
export GSETTINGS_SCHEMA_DIR=/opt/homebrew/share/glib-2.0/schemas/
GTK_THEME=Adwaita:dark XDG_DATA_DIRS=./share ./PyAccounts.py
