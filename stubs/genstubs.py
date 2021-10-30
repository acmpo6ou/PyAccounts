#!/usr/bin/env python3

import os
import re
import xml.etree.ElementTree as ET

os.system("stubgen core -o stubs")

STUB_DIR = "stubs/core/"
SKIP = ("__init__.pyi", "gtk_utils.pyi", "database_utils.pyi", "widgets.pyi")

for stub in os.listdir(STUB_DIR):
    if stub in SKIP:
        continue

    _in = open(f"{STUB_DIR}/{stub}", "r").readlines()
    out = open(f"{STUB_DIR}/{stub}", "w")

    out.write("from gi.repository import Gtk\n")
    injected = False
    for line in _in:
        out.write(line)

        if "class " in line and not injected:
            injected = True
            # fmt: off
            glade_filepath = f"ui/{stub[:-3]}glade" \
                .replace("ui/create_", "ui/create_edit_") \
                .replace("ui/edit_", "ui/create_edit_")

            parent_widget_id = glade_filepath \
                .replace("ui/", "") \
                .replace(".glade", "")
            # fmt: on

            glade_file = open(glade_filepath, "r").read()
            root = ET.parse(glade_filepath).getroot()

            ids = re.findall('id="([a-z_]*)"', glade_file)
            for _id in ids:
                widget = root.findall(f".//*[@id='{_id}']")[0]
                classname = widget.attrib["class"].replace("Gtk", "Gtk.")

                if _id == parent_widget_id:
                    out.write(f"    parent_widget: {classname}\n")
                    continue

                out.write(f"    {_id}: {classname}\n")
