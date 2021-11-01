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

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")

from gi.repository import Gdk, Gtk
from core.widgets import CreateForm


DROP_ID = 808


class CreateAccountForm(CreateForm):
    def __init__(self, database):
        super().__init__("create_edit_account")
        self.database = database
        self.attached_paths = {}

        # allow dropping files onto attached_files list to attach them
        self.attached_files.drag_dest_set(
            Gtk.DestDefaults.ALL,
            [Gtk.TargetEntry.new("text/uri-list", Gtk.TargetFlags.OTHER_APP, DROP_ID)],
            Gdk.DragAction.COPY,
        )

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

    def attach_file(self, path):
        """
        Adds item to attached_files list with file mime icon and file name.

        Saves path to attached_paths.
        :param path: path to file to attach.
        """

        # TODO: add path to attached_paths dict, file name is the key and path is the value
        # TODO: add item with file name to attached_files list box
        # TODO: add file mime icon to item using get_mime_icon() from gtk_utils

    def on_attach_file(self, _):
        """
        Displays attach file dialog.
        """

        # see FileChooserDialog and FileChooser docs for more details
        # TODO: set dialog title to "Attach file"
        # TODO: allow all files
        # TODO: use Gtk.FileChooserAction.OPEN
        # TODO: add 2 buttons: Cancel and Open (do we even need to add them?)
        # TODO: attach the file only if response is Gtk.ResponseType.ACCEPT
        # TODO: set select_multiple to True (to allow selection of multiple files)

        # TODO: use dialog.filenames to get list of selected file paths
        # TODO: iterate over selected paths and call attach_file() for each of them

    def on_detach_file(self, _):
        """
        Displays confirmation dialog to ask user if he really wants to detach selected file,
        detaches the file on user confirmation.
        """

        # TODO: show warning if there is no file selected in attached_files list
        # TODO: get selected item from attached_files and extract file name from it
        # TODO: create WarningDialog asking "Detach [file name]?"
        # TODO: if response is Gtk.ResponseType.ACCEPT:
        #  remove the file from attached_paths
        #  remove corresponding item from attached_files list (by iterating through children and
        #  removing child with appropriate file name, break from the loop after removed child)

    def on_drop_files(self, _, context, x, y, data, info, time):
        """
        Called when files are dropped onto attached files list, attaches dropped files.
        :param data: contains paths to dropped files.
        """

        # TODO: use data.get_uris() to get a list of file paths
        # TODO: remove `file://` at the beginning of each path
        # TODO: call attach_file for each path

    def get_attached_files(self):
        """
        Loads content of selected attached files handling errors.
        :return: dict mapping file names to file content.
        """

        # TODO: create empty attached_files dict
        # TODO: iterate through attached_paths:
        #  if path is None – skip it, because EditAccountForm may add old attached files as items
        #  with None path
        #  for each path try to read file content; save the content to attached_files dict
        #  on error display ErrorDialog "Failed to read file [file name]"

    def create_account(self) -> Account:
        """
        Creates account using form data.
        """

        # TODO: get data from all fields
        # TODO: call get_attached_files() to get proper dict (file name -> file content in bytes)

    def on_apply(self, _):
        """
        Creates account, adds it to accounts list.
        """

        # TODO: create Account instance using create_account and add it to the database,
        #  update accounts list
        self.destroy()
