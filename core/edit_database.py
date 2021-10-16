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

from core.create_database import CreateDatabaseForm
from core.database_utils import Database

gi.require_version("Gtk", "3.0")


class EditDatabaseForm(CreateDatabaseForm):
    def __init__(self):
        super().__init__(self)
        self.database = None
        # TODO: change apply's button text to Save

    def set_database(self, database: Database):
        """
        Populates form fields with data from database.
        """

    def on_apply_enabled(self, _):
        """
        Enables or disables apply button depending on whether there are errors in the form
        (i.e. no password entered, passwords do not match, etc...).
        Hides/shows error tips.
        """
        # TODO: allow database name be unchanged

    def on_apply(self, _):
        """
        Applies changes to database using form data.
        """
        # TODO: save database, update `databases` list, update list of databases (widget)
        # TODO: show success/error message
