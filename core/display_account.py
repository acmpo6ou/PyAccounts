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
import base64
import logging
import traceback
from pathlib import Path
from typing import TYPE_CHECKING

from gi.repository import Gtk, Gdk

from core.database_utils import Account
from core.gtk_utils import GladeTemplate, abc_list_sort, item_name
from core.widgets import AttachedFilesMixin, ErrorDialog

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

ERROR_SAVING_FILE = "Error saving the file!"
SUCCESS_SAVING_FILE = "File saved successfully!"
SUCCESS_PASSWORD_COPY = "Password and email/username are successfully copied!"
SUCCESS_NOTES_COPY = "Notes are successfully copied!"


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
        Copies e-mail/username to clipboard and password to safe clipboard.
        """

        account = self.account
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        to_copy = account.email if account.copy_email else account.username

        clipboard.set_text(to_copy, -1)
        self.database_window.main_window.safe_clipboard = account.password
        self.database_window.statusbar.success(SUCCESS_PASSWORD_COPY)

    def on_copy_notes(self, _=None):
        """
        Copies notes to safe clipboard.
        """
        self.database_window.main_window.safe_clipboard = self.account.notes
        self.database_window.statusbar.success(SUCCESS_NOTES_COPY)

    def save_attached_file(self, path: str, content: str):
        """
        Saves given attached file handling all errors.

        :param path: where to save the file.
        :param content: file content to save.
        """

        try:
            data = content.encode()
            content = base64.b64decode(data)
            Path(path).write_bytes(content)
            self.database_window.statusbar.success(SUCCESS_SAVING_FILE)
        except Exception as err:
            logging.error(traceback.format_exc())
            ErrorDialog(ERROR_SAVING_FILE, err).run()

    def on_save_file(self, _, row: Gtk.ListBoxRow):
        """
        Displays file dialog to save selected attached file.
        :param row: row containing name of attached file.
        """

        dialog = Gtk.FileChooserDialog(
            title="Save attached file",
            action=Gtk.FileChooserAction.SAVE,
        )
        filename = item_name(row)
        dialog.current_name = filename

        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button(Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT)

        response = dialog.run()
        dialog.hide()

        if response == Gtk.ResponseType.ACCEPT:
            self.save_attached_file(
                dialog.filename,
                self.account.attached_files[filename],
            )
