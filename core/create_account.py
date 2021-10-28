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
gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Gdk, Gtk
from core.widgets import CreateForm


class CreateAccountForm(CreateForm):
    def __init__(self, database):
        super().__init__("create_edit_account")
        self.database = database

        # load completion for email and username fields
        # TODO: get emails and usernames from self.database (use list comprehensions)
        usernames = ...
        emails = ...
        self.load_completion(self.username, usernames)
        self.load_completion(self.email, emails)

    def load_completion(self, field, items):
        """
        Loads completion for [field] using completion strings from [items].
        """

        # TODO: here's a sample code on how to use Gtk.EntryCompletion:
        # model = Gtk.ListStore(str)
        # for entry in mylist:
        #     model.append((entry,))
        # completion = Gtk.EntryCompletion()
        # completion.model = model
        # completion.set_text_column(0)  # it's important to use set_text_column!
        # field.completion = completion

    @staticmethod
    def on_hover_date_icon(icon):
        """
        Changes cursor style to `pointer` when hovering over date icon.
        :param icon: the date icon.
        """
        icon.window.cursor = Gdk.Cursor(Gdk.CursorType.HAND1)
        # TODO: possibly test this method

    def on_choose_date(self, *args):
        """
        Displays a dialog to choose the birth date.
        """

        # TODO: run DateChooserDialog dialog
        # TODO: if response is OK – use date_chooser.date to get picked date
        # TODO: convert the date to string of format "dd.mm.yyyy"
        # TODO: set birth_date label to this date
