#  Copyright (c) 2021-2022. Bohdan Kolvakh
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
import typing

from gi.repository import Gtk

from core.create_account import CreateAccount
from core.database_utils import Account, Database
from core.gtk_utils import delete_list_item
from core.widgets import AttachedFilesMixin

if typing.TYPE_CHECKING:
    from core.database_window import DatabaseWindow

EDIT_ACCOUNT_TITLE = "Edit <i>{}</i> account"


class EditAccount(CreateAccount, AttachedFilesMixin):
    # <editor-fold>
    add: Gtk.Image
    remove: Gtk.Image
    parent_widget: Gtk.Box
    title: Gtk.Label
    apply: Gtk.Button
    username: Gtk.Entry
    email: Gtk.Entry
    copy_email: Gtk.RadioButton
    copy_username: Gtk.RadioButton
    birth_box: Gtk.EventBox
    birth_date: Gtk.Label
    notes: Gtk.TextView
    attached_files: Gtk.ListBox
    accname: Gtk.Label
    name: Gtk.Entry
    name_error: Gtk.Label
    password: Gtk.Entry
    password_error: Gtk.Label
    repeat_password: Gtk.Entry
    passwords_diff_error: Gtk.Label
    # </editor-fold>

    APPLY_BUTTON_TEXT = "_Save"

    @property
    def items(self):
        accounts = list(self.database.accounts.keys())
        # it's OK if account name hasn't changed throughout editing
        accounts.remove(self.account.accountname)
        return accounts

    def __init__(self, database: Database, account: Account, database_window: "DatabaseWindow"):
        super().__init__(database, database_window)
        self.account = account
        # load already attached files mapping them to None since they don't have any path
        self.attached_paths = {file: None for file in account.attached_files}
        self.load_account()

    def load_account(self):
        """
        Populates form fields with account data.
        """

        self.title.markup = EDIT_ACCOUNT_TITLE.format(self.account.accountname)
        self.name.text = self.account.accountname
        self.email.text = self.account.email
        self.username.text = self.account.username
        copy = self.copy_email if self.account.copy_email else self.copy_username
        copy.active = True
        self.password.text = self.account.password
        self.repeat_password.text = self.account.password
        self.birth_date.text = self.account.birthdate
        self.notes.buffer.text = self.account.notes
        self.load_attached_files(self.account.attached_files)

    def create_account(self) -> Account:
        """
        Creates account using form data.
        """

        account = super().create_account()
        for filename, path in self.attached_paths.items():
            if path is None:
                content = self.account.attached_files[filename]
                account.attached_files[filename] = content
        return account

    def on_apply(self, _=None):
        """
        Saves changes done to account.
        """

        delete_list_item(
            self.database_window.accounts_list,
            self.account.accountname,
        )
        super().on_apply()
