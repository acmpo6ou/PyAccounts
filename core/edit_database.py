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

from core.create_database import CreateDatabase
from core.database_utils import Database
from core.gtk_utils import delete_list_item, add_list_item
from core.widgets import ErrorDialog

if typing.TYPE_CHECKING:
    from core.main_window import MainWindow

EDIT_DB_TITLE = "Edit <i>{}</i> database"
ERROR_EDITING_DB = "Error editing database!"


class EditDatabase(CreateDatabase):
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

    APPLY_BUTTON_TEXT = "_Save"

    @property
    def items(self):
        dbs = [database.name for database in self.main_window.databases]
        # it's OK if database name hasn't changed throughout editing
        dbs.remove(self.database.name)
        return dbs

    def __init__(self, database: Database, main_window: "MainWindow"):
        super().__init__(main_window)
        self.database = database
        self.title.markup = EDIT_DB_TITLE.format(database.name)

        self.name.text = database.name
        self.password.text = database.password
        self.repeat_password.text = database.password

    def on_apply(self, _=None):
        """
        Applies changes to database using form data.
        """

        try:
            db = self.database.save(
                self.name.text,
                self.password.text,
                self.database.accounts,
            )
        except Exception as err:
            logging.error(traceback.format_exc())
            ErrorDialog(ERROR_EDITING_DB, err).run()
            return

        self.main_window.databases.remove(self.database)
        self.main_window.databases.append(db)
        self.main_window.databases.sort(key=lambda db: db.name)

        delete_list_item(self.main_window.db_list, self.database.name)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/icon.svg", 50, 50, True)
        add_list_item(self.main_window.db_list, pixbuf, db.name)

        self.destroy()
        win = self.main_window.windows[self.database.name]
        del self.main_window.windows[self.database.name]
        self.main_window.windows[db.name] = win

        # TODO: preserve the * in the title if it was there
        win.title = db.name
        win.database.name = db.name
        win.database.password = db.password
