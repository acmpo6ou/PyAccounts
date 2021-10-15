#!/usr/bin/python3

#  Copyright (c) 2022. Bohdan Kolvakh
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

import gi

gi.require_version("Gtk", "3.0")
from core.gtk_utils import GladeTemplate


class GenPassDialog(GladeTemplate):
    """
    A dialog to generate password.
    """

    def __init__(self, pass1, pass2):
        super().__init__("generate_password")
        self.pass1 = pass1
        self.pass2 = pass2

    def on_cancel(self, _):
        self.parent_widget.hide()

    def on_generate(self, _):
        """
        Generates password and fills pass1 and pass2 password fields with it.
        """
        # TODO: regenerate password if it happens not to contain at least one of the specified
        #  by user characters
