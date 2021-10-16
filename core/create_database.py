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


class CreateDatabaseForm(GladeTemplate):
    def __init__(self):
        super().__init__("create_edit_database")
        self.vexpand = True

    def on_validate_name(self, name):
        """
        Auto removes unallowed characters from database name.
        Shows a warning explaining the user that he's trying to enter unallowed characters.
        :param name: name field containing database name.
        """

    def on_apply_enabled(self, _):
        """
        Enables or disables apply button depending on whether there are errors in the form
        (i.e. no password entered, passwords do not match, etc...)
        """

    def on_pass_toggle(self, _, __, ___):
        """
        Toggles password visibility of both password fields.
        """

    def on_generate_password(self, _):
        """
        Display dialog to generate password.
        """

    def on_apply(self, _):
        """
        Creates database from form's data
        """
        # TODO: create database, add it to databases list, update list of databases,
        #  open database window
