#!/usr/bin/env python3

import os

os.system("stubgen core -o stubs")
STUB_DIR = "stubs/core/"

for stub in os.listdir(STUB_DIR):
    if stub == "__init__.pyi":
        continue

    _in = open(f"{STUB_DIR}/{stub}", "r").readlines()
    out = open(f"{STUB_DIR}/{stub}", "w")

    for line in _in:
        if "def " not in line and ": Any" in line:
            continue

        out.write(line)
