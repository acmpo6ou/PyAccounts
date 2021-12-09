#!/usr/bin/env python3.9

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
Extends Gtk stubs generated by PyCharm to include our pythonic properties.
This way, we get autocompletion for them.
See _getattr and _setattr from gtk_utils module for more details.
"""

import os
import re


for module in ("Gtk", "Gdk", "Gio"):
    STUBS_DIR = f"stubs/{module}"

    for file in os.listdir(STUBS_DIR):
        _in = open(f"{STUBS_DIR}/{file}").read()
        out = open(f"{STUBS_DIR}/{file}", "a")

        gets = re.findall("get_[a-z_]*", _in)
        sets = re.findall("set_[a-z_]*", _in)

        props = set()
        for method in gets + sets:
            prop = method[4:]
            props.add(prop)

        for prop in props:
            out.write(f"    {prop} = ...\n")
