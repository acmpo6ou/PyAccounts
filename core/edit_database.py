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

from core.create_database import CreateDatabaseForm
from core.database_utils import Database


class EditDatabaseForm(CreateDatabaseForm):
    def __init__(self, database: Database):
        super().__init__()
        self.database = database
        # TODO: change title text to `Edit [database name] database`
        # TODO: change apply's button text to Save
        # TODO: populate form fields with data from database.

    def validate_name(self):
        """
        Validates name field, displaying error tip if database name is invalid.

        Possible problems with database name:
        * name field is empty
        * name field contains name that is already taken; it's OK, however if database name
        hasn't changed throughout editing
        :return: True if name is valid.
        """

    def on_apply(self, _):
        """
        Applies changes to database using form data.
        """
        # TODO: save database, update list of databases
        # TODO: show success/error message
        # TODO: destroy form on success
