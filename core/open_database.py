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

from gi.repository import Gtk, GLib

from core.database_utils import Database
from core.database_window import DatabaseWindow
from core.gtk_utils import GladeTemplate

if typing.TYPE_CHECKING:
    from core.main_window import MainWindow

OPEN_DB_TITLE = "Open <i>{}</i> database"


class OpenDatabase(GladeTemplate):
    # <editor-fold>
    parent_widget: Gtk.Box
    title: Gtk.Label
    open_button: Gtk.Button
    incorrect_password: Gtk.Label
    password: Gtk.Entry

    # </editor-fold>

    def __init__(self, database: Database, main_window: "MainWindow"):
        super().__init__("open_database")
        self.vexpand = True
        self.database = database
        self.main_window = main_window

        self.title.markup = OPEN_DB_TITLE.format(database.name)
        # wait for password field to get mapped and make it focused
        GLib.timeout_add(100, lambda: self.password.grab_focus())

    def on_open_database(self, _=None):
        """
        Tries to open database with password from password field,
        if there is an error decrypting the database – displays incorrect_password tip.
        Opens database window on success.
        """

        self.database.open(self.password.text)
        self.destroy()
        DatabaseWindow(self.database, self.main_window).present()

    def on_password_changed(self, _):
        """
        Hides incorrect_password tip.
        """

    def on_icon_press(self, _, icon_pos, __):
        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            self.toggle_password_visibility()
        else:
            self.clear_password()

    def toggle_password_visibility(self):
        self.password.visibility = not self.password.visibility

    def clear_password(self):
        self.password.text = ""
