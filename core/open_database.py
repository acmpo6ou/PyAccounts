#!/usr/bin/python3

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


from core.database_utils import Database
from core.gtk_utils import GladeTemplate


class OpenDatabaseForm(GladeTemplate):
    def __init__(self, database: Database):
        super().__init__("open_database")
        self.vexpand = True
        self.database = database

        # TODO: change form title to `Open [database name] database`.
        # TODO: make database name cursive

    def on_open_database(self, _):
        """
        Tries to open database with password from password field,
        if there is an error decrypting the database – displays incorrect_password tip.
        Opens database window on success.
        """
        # TODO: destroy form on success

    def on_password_changed(self, _):
        """
        Hides incorrect_password tip.
        """

    def on_toggle_password_visibility(self, _):
        ...
