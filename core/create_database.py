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
import logging
import traceback
import typing

from gi.repository import Gtk, GdkPixbuf

from core.database_utils import Database
from core.database_window import DatabaseWindow
from core.gtk_utils import add_list_item
from core.widgets import CreateForm, FilterDbNameMixin, ErrorDialog

if typing.TYPE_CHECKING:
    from core.main_window import MainWindow


ERROR_DB_CREATION = "Error creating database!"


class CreateDatabase(CreateForm, FilterDbNameMixin):
    # <editor-fold>
    parent_widget: Gtk.Box
    title: Gtk.Label
    name: Gtk.Entry
    password: Gtk.Entry
    repeat_password: Gtk.Entry
    apply: Gtk.Button
    name_error: Gtk.Label
    password_error: Gtk.Label
    passwords_diff_error: Gtk.Label
    # </editor-fold>

    @property
    def items(self):
        return [database.name for database in self.main_window.databases]

    def __init__(self, main_window: "MainWindow"):
        super().__init__("create_edit_database")
        self.main_window = main_window
        self.password.text = main_window.safe_clipboard
        self.repeat_password.text = main_window.safe_clipboard

    def on_apply(self, _=None):
        """
        Creates database using form data and handling all errors.
        """

        database = Database(self.name.text, self.password.text)
        try:
            database.create()
        except Exception as err:
            logging.error(traceback.format_exc())
            ErrorDialog(ERROR_DB_CREATION, err).run()
            return

        self.main_window.databases.append(database)
        self.main_window.databases.sort(key=lambda db: db.name)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/icon.svg", 50, 50, True)
        add_list_item(self.main_window.db_list, pixbuf, database.name)

        self.destroy()
        win = DatabaseWindow(database, self.main_window)
        self.main_window.windows[database.name] = win
        win.present()
