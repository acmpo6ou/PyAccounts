#!/usr/bin/env python3

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

from core.widgets import Window

gi.require_version("Gtk", "3.0")
from core.gtk_utils import GladeTemplate


class DatabaseWindow(Window):
    def __init__(self, database, main_window):
        GladeTemplate.__init__(self, "database_window")
        Window.__init__(self)

        self.main_window = main_window
        self.database = database
        # TODO: set title to database name

    def on_save(self, _):
        """
        Saves database to disk.
        On success displays success message in statusbar, on error – error message.
        """

    def on_quit(self, _):
        """
        Checks if database is saved, if it is – quits, otherwise displays confirmation dialog.
        """

    def on_create_account(self, _):
        """
        Displays create account form.
        """

    def on_edit_database(self, _):
        """
        Displays edit account form for selected account.
        """
        # TODO: show warning in statusbar if there is no account selected
        # TODO: call form.set_account()

    def on_delete_account(self, _):
        """
        Displays confirmation dialog asking user if he really want's to delete selected account.
        """
        # TODO: show warning in statusbar if there is no account selected
