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

from core.database_utils import Account
from core.widgets import AttachedFilesMixin

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from core.create_account import CreateAccountForm


class EditAccountForm(CreateAccountForm, AttachedFilesMixin):
    def __init__(self, database, account):
        super().__init__(database)
        self.account = account
        # TODO: fill attached_paths with file names from account.attached_files;
        #  map file names to None (since they don't have any path)
        # load already attached files mapping them to None since they don't have any path
        self.attached_paths = ...
        self.load_account()
        # TODO: change Create button to Save

    def load_account(self):
        """
        Populates form fields with account data.
        """

        self.load_attached_files()
        # TODO: change title to `Edit [account name] account`
        # TODO: make account name cursive

    def validate_name(self):
        """
        Validates name field, displaying error tip if account name is invalid.

        Possible problems with account name:
        * name field is empty
        * name field contains name that is already taken; it's OK, however if account name
        hasn't changed throughout editing
        :return: True if name is valid.
        """

    def create_account(self) -> Account:
        """
        Creates account using form data.
        """
        account = super().create_account()
        # TODO: add already loaded attached files:
        """
        iterate over attached_paths keys:
            if key value is None:
                add attached file from self.account.attached_files to account.attached_files
        return account
        """

    def on_apply(self, _):
        """
        Saves changes done to account.
        """

        # TODO: remove old account from database and accounts list (remove ListBoxRow)
        super().on_apply()
