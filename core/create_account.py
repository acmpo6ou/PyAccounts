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
from __future__ import annotations

import logging
import traceback
import typing
from pathlib import Path

from gi.repository import Gdk, Gtk

from core.database_utils import Account, Database
from core.gtk_utils import get_mime_icon, add_list_item, abc_list_sort, item_name
from core.widgets import CreateForm, DateChooserDialog, WarningDialog, ErrorDialog

if typing.TYPE_CHECKING:
    from core.database_window import DatabaseWindow

DROP_ID = 808
CONFIRM_ATTACH_EXISTING_FILE = "File <b>{}</b> is already attached, replace?"
SELECT_FILES_TO_DETACH = "Please select some files to detach."
CONFIRM_FILES_DETACH = "Detach selected files?"
ERROR_READING_FILE = "Error reading file <b>{}</b>."


class CreateAccount(CreateForm):
    # <editor-fold>
    add: Gtk.Image
    remove: Gtk.Image
    parent_widget: Gtk.Box
    title: Gtk.Label
    apply: Gtk.Button
    username: Gtk.Entry
    email: Gtk.Entry
    copy_email: Gtk.RadioButton
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

    @property
    def items(self):
        return list(self.database.accounts)

    def __init__(self, database: Database, database_window: "DatabaseWindow"):
        super().__init__("create_edit_account")
        self.database = database
        self.database_window = database_window
        self.attached_paths = {}

        # allow dropping files onto attached_files list to attach them
        self.attached_files.drag_dest_set(
            Gtk.DestDefaults.ALL,
            [Gtk.TargetEntry.new("text/uri-list", Gtk.TargetFlags.OTHER_APP, DROP_ID)],
            Gdk.DragAction.COPY,
        )
        self.attached_files.sort_func = abc_list_sort

        # load completion for email and username fields
        usernames = [account.username for account in self.database.accounts.values()]
        emails = [account.email for account in self.database.accounts.values()]
        self.load_completion(self.username, usernames)
        self.load_completion(self.email, emails)

    @staticmethod
    def load_completion(field: Gtk.Entry, items: list[str]):
        """
        Loads completion for [field] using completion strings from [items].
        """

        model = Gtk.ListStore(str)
        for entry in items:
            model.append([entry])

        completion = Gtk.EntryCompletion()
        completion.model = model
        completion.set_text_column(0)  # it's important to use set_text_column!
        field.completion = completion

    @staticmethod
    def on_hover_date_icon(icon: Gtk.Image):
        """
        Changes cursor style to `pointer` when hovering over date icon.
        :param icon: the date icon.
        """
        icon.window.cursor = Gdk.Cursor(Gdk.CursorType.HAND1)

    def on_choose_date(self, *args):
        """
        Displays a dialog to choose the birthdate.
        """

        dialog = DateChooserDialog(self.birth_date.text)
        if dialog.run() == Gtk.ResponseType.OK:
            date = dialog.calendar.date
            date_str = f"{date.day:02d}.{date.month + 1:02d}.{date.year}"
            self.birth_date.text = date_str

    def attach_file(self, path: str):
        """
        Adds item to attached_files list with file mime icon and file name.

        Saves path to attached_paths.
        If the file with such name already exists – displays confirmation dialog.
        :param path: path to file to attach.
        """

        name = Path(path).name
        if name in self.attached_paths:
            # if file name is already in attached_paths but its path is same
            # as [path] don't show a confirmation dialog.
            # Because when dropping multiple files onto attached_files list,
            # the dropping event is generated twice for some reason
            # and attached_file() will also be called twice
            if self.attached_paths[name] == path:
                return

            msg = CONFIRM_ATTACH_EXISTING_FILE.format(name)
            if WarningDialog(msg).run() == Gtk.ResponseType.YES:
                self.attached_paths[name] = path
            return

        self.attached_paths[name] = path
        icon = get_mime_icon(path)
        add_list_item(self.attached_files, icon.pixbuf, name, path)

    def on_attach_file(self, _):
        """
        Displays attach file dialog.
        """

        dialog = Gtk.FileChooserDialog(
            title="Attach file",
            action=Gtk.FileChooserAction.OPEN,
        )
        dialog.select_multiple = True

        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button("Open", Gtk.ResponseType.ACCEPT)
        response = dialog.run()
        dialog.hide()

        if response == Gtk.ResponseType.ACCEPT:
            for path in dialog.filenames:
                self.attach_file(path)

    def on_detach_file(self, _=None):
        """
        Displays confirmation dialog to ask user if he really wants to detach selected file,
        detaches the file on user confirmation.
        """

        rows = self.attached_files.selected_rows
        if not rows:
            self.database_window.statusbar.warning(SELECT_FILES_TO_DETACH)

        response = WarningDialog(CONFIRM_FILES_DETACH).run()
        if response == Gtk.ResponseType.NO:
            return

        filenames = [item_name(row) for row in rows]
        for name in filenames:
            del self.attached_paths[name]
        for row in rows:
            row.destroy()

    def on_drop_files(self, _, context, x, y, data: Gtk.SelectionData, info, time):
        """
        Called when files are dropped onto attached files list, attaches dropped files.
        :param data: contains paths to dropped files.
        """

        paths = data.get_uris()
        for path in paths:
            path = path.removeprefix("file://")
            if Path(path).is_file():
                self.attach_file(path)

    def get_attached_files(self) -> dict[str, bytes]:
        """
        Loads content of selected attached files handling errors.
        :return: dict mapping file names to file content.
        """

        attached_files = {}
        for filename, path in self.attached_paths.items():
            if not path:  # skip files that are already attached
                continue

            try:
                with open(path, "rb") as file:
                    data = file.read()
                    attached_files[filename] = data
            except Exception as err:
                logging.error(traceback.format_exc())
                ErrorDialog(ERROR_READING_FILE.format(filename), err).run()
        return attached_files

    def create_account(self) -> Account:
        """
        Creates account using form data.
        """

        # TODO: get data from all fields
        # TODO: call get_attached_files() to get proper dict (file name -> file content in bytes)

    def on_apply(self, _=None):
        """
        Creates account and adds it to accounts list.
        """

        # TODO: create Account instance using create_account and add it to the database,
        #  update accounts list
        # TODO: destroy form on success
