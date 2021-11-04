#!/usr/bin/env python3

#  Copyright (c) 2021. Bohdan Kolvakh
#  This file is part of PyAccounts.
#
#  PyAccounts is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyAccounts is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PyAccounts.  If not, see <https://www.gnu.org/licenses/>.

"""
Generates type stubs for `core` package.

Generates stubs using mypy, then adds stubs extracted from glade ui files.
This way, all classes that derive from GladeTemplate will have proper autocomplete.
"""

import os
import re
import sys

# noinspection StandardLibraryXml
from xml.etree import ElementTree

result = os.system("stubgen core -o stubs")
if result:
    print("Please install mypy")
    sys.exit()

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
            root = ElementTree.parse(glade_filepath).getroot()

            ids = re.findall('id="([a-z_]*)"', glade_file)
            for _id in ids:
                widget = root.findall(f".//*[@id='{_id}']")[0]
                classname = widget.attrib["class"].replace("Gtk", "Gtk.")

                if _id == parent_widget_id:
                    out.write(f"    parent_widget: {classname}\n")
                    continue

                out.write(f"    {_id}: {classname}\n")
