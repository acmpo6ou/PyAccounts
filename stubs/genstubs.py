#!/usr/bin/env python3

import os
import re
import xml.etree.ElementTree as ET

# os.system("stubgen core -o stubs")

STUB_DIR = "stubs/core/"
SKIP = ("__init__.pyi", "gtk_utils.pyi", "database_utils.pyi", "widgets.pyi")

for stub in os.listdir(STUB_DIR):
    if stub in SKIP:
        continue

    _in = open(f"{STUB_DIR}/{stub}", "r").readlines()
    # out = open(f"{STUB_DIR}/{stub}", "w")

    injected = False
    # print(stub)
    for line in _in:
        # out.write(line)

        if "class " in line and not injected:
            injected = True
            glade_file = f"ui/{stub[:-3]}glade"

            regex = re.search('id="(*)"')

            # root = ET.parse(glade_file).getroot()
            # print(root)
    break
