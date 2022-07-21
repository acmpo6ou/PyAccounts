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
import os
from typing import TYPE_CHECKING

from gi.repository import Gdk, Gtk, GdkPixbuf

from core.database_utils import Database
from core.gtk_utils import GladeTemplate, load_icon
from core.widgets import Window

if TYPE_CHECKING:
    from core.main_window import MainWindow

ACCOUNT_ICONS_DIR = "img/account_icons/"


class DatabaseWindow(Window):
    # <editor-fold>
    parent_widget: Gtk.Box
    menubar_toolbar: Gtk.Box
    menubar: Gtk.MenuBar
    toolbar: Gtk.Toolbar
    separator: Gtk.Paned
    form_box: Gtk.Box
    accounts_list: Gtk.ListBox
    status_bar: Gtk.Label
    # </editor-fold>

    # it's important to sort icon names by length (longer names first),
    # because this way we will have better matches
    account_icons = [
        icon.removesuffix(".svg")
        for icon in sorted(
            os.listdir(ACCOUNT_ICONS_DIR),
            key=lambda x: len(x),
            reverse=True
        )
    ]

    def __init__(self, database: Database, main_window: "MainWindow"):
        GladeTemplate.__init__(self, "database_window")
        Window.__init__(self)

        self.main_window = main_window
        self.database = database

        # Ctrl+S to save database
        self.shortcuts.connect(
            Gdk.keyval_from_name("s"),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE,
            self.on_save,
        )

        self.load_accounts()
        self.title = database.name

    def load_accounts(self):
        """
        Populates accounts_list with items.
        """

        # TODO: set sort_func for accounts_list to sort alphabetically
        # TODO: for each account get icon using load_account_icon(), label is account name
        # TODO: use add_list_item() to add accounts to accounts_list
        # see MainWindow's load_databases for more details

    def load_account_icon(self, accountname: str):
        """
        Returns account icon associated with given [accountname].
        """

        icon = load_icon("cs-user-accounts", 50)
        for icon_name in self.account_icons:
            if icon_name in accountname.lower():
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    f"{ACCOUNT_ICONS_DIR}/{icon_name}.svg", 50, 50, True
                )
                return Gtk.Image.new_from_pixbuf(pixbuf)
        return icon

    def on_save(self, *args):
        """
        Saves database to disk.
        On success displays success message in statusbar, on error – error message.
        """

    def do_delete_event(self, event):
        """
        Called when user tries to close the window, propagates event to on_quit.
        NOTE: DO NOT move this method to Window superclass, or else it won't work.
        """
        return self.on_quit(event)

    def on_quit(self, _) -> bool:
        """
        Checks if database is saved, if it is – quits, otherwise displays confirmation dialog.
        :returns: True to prevent quiting and False to allow it.
        """

        # TODO: show warning dialog "Are you sure you want to close the database?"
        #  "Any unsaved changes will be lost!"

        # TODO: offer 3 buttons: Cancel, Save and Ok
        #   if Cancel is picked – return
        #   if Save is picked, call database.save()
        #   at the end of the method call database.close() and self.destroy()

        # TODO: return True if user doesn't want to quit and False otherwise

    def on_create_account(self, _):
        """
        Displays create account form.
        """
        # TODO: use show_form()

    def on_edit_account(self, _):
        """
        Displays edit account form for selected account.
        """
        # TODO: show warning in statusbar if there is no account selected
        # TODO: use show_form()

    def on_delete_account(self, _):
        """
        Displays confirmation dialog asking user if he really wants to delete selected account.
        """

        # TODO: show warning in statusbar if there is no account selected
        #  "Please, select account you want to delete."
        # TODO: remove account from database.accounts, call accounts_list.delete(name)
