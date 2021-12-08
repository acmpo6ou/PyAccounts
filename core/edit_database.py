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
from gi.repository import Gtk

from core.create_database import CreateDatabase
from core.database_utils import Database
from core.widgets import ValidateDbNameMixin


class EditDatabase(ValidateDbNameMixin, CreateDatabase):
    # <editor-fold>
    parent_widget: Gtk.Box
    title: Gtk.Label
    name: Gtk.Entry
    password: Gtk.Entry
    repeat_password: Gtk.Entry
    apply: Gtk.Button
    name_error: Gtk.Label
    password_error: Gtk.Label
    passwords_diff_error: Gtk.Label
    # </editor-fold>

    def __init__(self, database: Database):
        super().__init__()
        self.database = database
        # TODO: change title text to `Edit [database name] database`
        # TODO: make database name cursive
        # TODO: change apply's button text to Save
        # TODO: populate form fields with data from database.

    def on_apply(self, _):
        """
        Applies changes to database using form data.
        """
        # TODO: save database, update list of databases
        # TODO: show success/error message
        # TODO: destroy form on success
