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
from gi.repository import Gtk

from core.gtk_utils import GladeTemplate

gi.require_version("Gtk", "3.0")

NOTES_PLACEHOLDER = "Text is hidden, use eye button to toggle its visibility."


class DisplayAccount(GladeTemplate):
    def __init__(self):
        super().__init__("display_account")
        # TODO: set sort_func for attached_files list to sort it alphabetically

    def set_account(self, account):
        """
        Populates form fields with account data.
        """
        self.account = account
        # TODO: use format() or f-strings, to make text appear beautifully
        # TODO: set password label's text to dots (use '●' * 24)
        # TODO: set notes text to NOTES_PLACEHOLDER
        self.load_attached_files()

    def load_attached_files(self):
        """
        Populates attached_files list with attached files.
        """

        """
        iterate attached_files dict keys:
            create label with key text
            add it to attached_files list box
        """

    def on_toggle_pass(self, button: Gtk.ToggleButton):
        """
        Toggles password visibility.
        :param button: used to decide whether to show or hide the password.
        """
        # TODO: if button.active is True – set password label to account password (formatting it
        #  appropriately with format())
        # TODO: else – set password label to dots

    def on_toggle_notes(self, button: Gtk.ToggleButton):
        """
        Toggles notes visibility.
        :param button: used to decide whether to show or hide the notes.
        """
        # TODO: if button.active is True – set notes label to account notes
        #  else – set notes label to NOTES_PLACEHOLDER

    def on_copy(self, _):
        """
        Copies e-mail to clipboard and password to safe clipboard.
        """
        # TODO: copy password to password field of MainWindow.
        # TODO: remove password after 1 minute
