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

ACCOUNT_ICONS_DIR = "img/account_icons/"


class DatabaseWindow(Window):
    # TODO: use list comprehension, os.listdir(ACCOUNT_ICONS_DIR) and sorted(with custom function)
    # TODO: remove .svg from icon names
    # it's important to sort icon names by length (longer names first), because this way
    # we will have better matches
    account_icons = ...

    def __init__(self, database, main_window):
        GladeTemplate.__init__(self, "database_window")
        Window.__init__(self)

        self.main_window = main_window
        self.database = database
        self.load_accounts()
        # TODO: set title to database name

    def load_accounts(self):
        """
        Populates accounts_list with items.
        """

        # TODO: set sort_func for accounts_list to sort alphabetically
        # TODO: for each account create hbox with icon and label
        # TODO: get icon using load_account_icon(), label is account name
        # TODO: style label: xalign = 0, margin start = 5
        # TODO: add() hbox to accounts_list

    def load_account_icon(self, accountname):
        """
        Returns account icon associated with given [accountname].
        """

        # TODO: icon = default icon (cs-user-accounts)
        # TODO: see loadAccountIcon() of MyAccounts:
        #  https://github.com/acmpo6ou/MyAccounts/blob/master/app/src/main/java/com/acmpo6ou/myaccounts/account/accounts_list/AccountsAdapter.kt
        #  if icon found: icon = load_icon(name, size) (from gtk_utils)
        # TODO: return icon
        # TODO: see tests of loadAccountIcon()

    def on_save(self, _):
        """
        Saves database to disk.
        On success displays success message in statusbar, on error – error message.
        """

    def on_quit(self, _):
        """
        Checks if database is saved, if it is – quits, otherwise displays confirmation dialog.
        """

        # TODO: show warning dialog "Are you sure you want to close the database?"
        #  "Any unsaved changes will be lost!"

        # TODO: offer 3 buttons: Cancel, Save and Ok
        #   if Cancel is picked – return
        #   if Save is picked, call database.save()
        #   at the end of the method call database.close() and self.destroy()

    def on_create_account(self, _):
        """
        Displays create account form.
        """
        # TODO: use show_form()

    def on_edit_database(self, _):
        """
        Displays edit account form for selected account.
        """
        # TODO: show warning in statusbar if there is no account selected
        # TODO: call form.set_account()
        # TODO: use show_form()

    def on_delete_account(self, _):
        """
        Displays confirmation dialog asking user if he really want's to delete selected account.
        """

        # TODO: show warning in statusbar if there is no account selected
        #  "Please, select account you want to delete."
        # TODO: remove account from database.accounts, remove corresponding ListBoxRow from
        #  accounts_list
