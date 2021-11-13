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

from core.widgets import CreateForm


class CreateDatabase(CreateForm):
    def __init__(self):
        super().__init__("create_edit_database")

    def on_filter_name(self, name):
        """
        Removes unallowed characters from database name.

        Shows a warning explaining the user that he's trying to enter unallowed characters.
        :param name: name field containing database name.
        """

    def on_apply(self, _):
        """
        Creates database using form data and handling all errors
        """

        # TODO: create database, add it to databases list, update list of databases,
        #  open database window
        # TODO: on error show error dialog
        # TODO: destroy form on success
