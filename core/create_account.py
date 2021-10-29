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

from gi.repository import Gdk
from core.widgets import CreateForm


class CreateAccountForm(CreateForm):
    def __init__(self, database):
        super().__init__("create_edit_account")
        self.database = database
        self.attached_paths = {}

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

    def on_attach_file(self, _):
        """
        Displays attach file dialog.
        Saves all selected files to attached_paths.
        Adds item to attached_files list with mime icon of file and file name.
        """

        # see FileChooserDialog and FileChooser docs for more details
        # TODO: set dialog title to "Attach file"
        # TODO: allow all files
        # TODO: use Gtk.FileChooserAction.OPEN
        # TODO: add 2 buttons: Cancel and Open (do we even need to add them?)
        # TODO: attach the file only if response is Gtk.ResponseType.ACCEPT
        # TODO: set select_multiple to True (to allow selection of multiple files)

        # TODO: use dialog.filenames to get list of selected file paths
        # TODO: iterate over selected paths and add them to attached_paths dict, file name is the
        #  key and path is the value
        # TODO: add item with file name to attached_files list box
        # TODO: add file mime icon to item using get_mime_icon() from gtk_utils

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

    def on_apply(self, _):
        """
        Creates account from form data.
        """

        # TODO: get data from all fields
        # TODO: call load_attached_files() to get proper dict (file name -> file content in bytes)
        # TODO: create Account instance and add it to the database
        # TODO: clear form with clear()
