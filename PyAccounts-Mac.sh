#!/usr/bin/env bash

cd ~/Developer/PyAccounts || exit
source venv/bin/activate
export GSETTINGS_SCHEMA_DIR=/opt/homebrew/share/glib-2.0/schemas/
GTK_THEME=Adwaita:dark XDG_DATA_DIRS=./share ./PyAccounts.py
