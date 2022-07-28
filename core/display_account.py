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
from typing import TYPE_CHECKING

from gi.repository import Gtk, Gdk

from core.database_utils import Account
from core.gtk_utils import GladeTemplate, abc_list_sort
from core.widgets import AttachedFilesMixin

if TYPE_CHECKING:
    from core.database_window import DatabaseWindow

ACCOUNT_NAME = "👤 Account name: {}"
USERNAME = "✏️ Username: {}"
EMAIL = "✉️ E-mail: {}"
TO_COPY = "📋️ To copy: {}"
PASSWORD = "🔒️ Password: {}"
BIRTH_DATE = "📅 Date of birth: {}"
NOTES_PLACEHOLDER = "Text is hidden, use eye button to toggle its visibility."
DOTS = '●' * 24


class DisplayAccount(GladeTemplate, AttachedFilesMixin):
    # <editor-fold>
    copy_notes: Gtk.Image
    visibility: Gtk.Image
    visibility_notes: Gtk.Image
    parent_widget: Gtk.Box
    accountname: Gtk.Label
    username: Gtk.Label
    email: Gtk.Label
    to_copy: Gtk.Label
    password: Gtk.Label
    birth_date: Gtk.Label
    notes: Gtk.TextView
    attached_files: Gtk.ListBox
    # </editor-fold>

    def __init__(self, account: Account, database_window: "DatabaseWindow"):
        super().__init__("display_account")
        self.database_window = database_window
        self.account = account

        self.accountname.text = ACCOUNT_NAME.format(account.accountname)
        self.email.text = EMAIL.format(account.email)
        self.username.text = USERNAME.format(account.username)
        to_copy = "email" if account.copy_email else "username"
        self.to_copy.text = TO_COPY.format(to_copy)
        self.password.text = PASSWORD.format(DOTS)
        self.birth_date.text = BIRTH_DATE.format(account.birthdate)
        self.notes.buffer.text = NOTES_PLACEHOLDER

        self.attached_files.sort_func = abc_list_sort
        self.load_attached_files(account.attached_files)

        # Ctrl+C to copy password
        database_window.shortcuts.connect(
            Gdk.keyval_from_name("c"),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE,
            self.on_copy,
        )

    def on_toggle_pass(self, button: Gtk.ToggleButton):
        """
        Toggles password visibility.
        :param button: used to decide whether to show or hide the password.
        """

        password = self.account.password if button.active else DOTS
        self.password.text = PASSWORD.format(password)

    def on_toggle_notes(self, button: Gtk.ToggleButton):
        """
        Toggles notes visibility.
        :param button: used to decide whether to show or hide the notes.
        """

        notes = self.account.notes if button.active else NOTES_PLACEHOLDER
        self.notes.buffer.text = notes

    def on_copy(self, *args):
        """
        Copies e-mail to clipboard and password to safe clipboard.
        """
        # TODO: copy password to safe_clipboard property of MainWindow.

    def on_copy_notes(self, _):
        """
        Copies notes to safe clipboard.
        """
        # TODO: copy notes to safe_clipboard property of MainWindow.

    def save_attached_file(self, path: str, content: bytes):
        """
        Saves given attached file handling all errors.

        :param path: where to save the file.
        :param content: file content to save.
        """
        # TODO: open file for writing, write content to file
        # TODO: Show error/success message.

    def on_save_file(self, row: Gtk.ListBoxRow):
        """
        Displays file dialog to save selected attached file.
        :param row: row containing name of attached file.
        """

        # see FileChooserDialog docs for more details
        # TODO: set dialog title to "Save attached file"
        # TODO: set default name to attached file name (use current_name property)
        # TODO: use Gtk.FileChooserAction.SAVE
        # TODO: add 2 buttons: Cancel and Save
        # TODO: save the file only if response is Gtk.ResponseType.ACCEPT
        # TODO: use `filename` property of dialog to access selected file path
        # TODO: call save_attached_file
