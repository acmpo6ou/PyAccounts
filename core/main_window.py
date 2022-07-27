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
import glob
import logging
import os
import shutil
import traceback
from pathlib import Path

from gi.repository import Gtk, Gdk, GdkPixbuf

import core
from core.create_database import CreateDatabase
from core.database_utils import Database
from core.database_window import DatabaseWindow
from core.edit_database import EditDatabase
from core.gtk_utils import GladeTemplate, abc_list_sort, delete_list_item, add_list_item, item_name
from core.open_database import OpenDatabase
from core.rename_database import RenameDatabase
from core.settings import Config
from core.widgets import Window, WarningDialog, ErrorDialog, IconDialog

IMPORT_DATABASE_TITLE = "Import database"
SUCCESS_DB_IMPORT = "Database imported successfully!"
WARNING_DB_EXISTS = "The database you are trying to import already exists!"
WARNING_DB_CORRUPTED = (
    "The database you are trying to import is probably corrupted.\n"
    "It's file size should be no smaller than 116 bytes."
)
ERROR_DB_IMPORT = "Error importing database!"

EXPORT_DATABASE_TITLE = "Export database"
SELECT_DB_TO_EXPORT = "Please select a database to export."
SUCCESS_DB_EXPORT = "Database exported successfully!"
ERROR_DB_EXPORT = "Error exporting database!"

SELECT_DB_TO_EDIT = "Please select a database to edit."
SELECT_DB_TO_DELETE = "Please select a database to delete."
CONFIRM_QUIT = "Are you sure you want to quit?"

CONFIRM_DB_DELETION = "Delete <b>{}</b> database?"
SUCCESS_DB_DELETED = "Database deleted successfully!"
ERROR_DB_DELETION = "Error deleting the database!"


class MainWindow(Gtk.ApplicationWindow, Window):
    # <editor-fold>
    parent_widget: Gtk.Box
    menubar_toolbar: Gtk.Box
    menubar: Gtk.MenuBar
    toolbar: Gtk.Toolbar
    separator: Gtk.Paned
    form_box: Gtk.Box
    db_list: Gtk.ListBox
    status_bar: Gtk.Label

    # </editor-fold>

    def __init__(self, *args, **kwargs):
        Gtk.ApplicationWindow.__init__(self, *args, **kwargs)
        GladeTemplate.__init__(self, "main_window")
        Window.__init__(self)

        # we will copy password or notes here, because it's safer than using a regular clipboard
        self._safe_clipboard = ""

        self.main_window = self
        self.windows: dict[str, DatabaseWindow] = {}

        self.config = Config()
        self.load_css()

        self.get_databases()
        # self.databases = [Database("main")]
        self.load_databases()
        self.select_main_database()

        # Ctrl+I to import database
        self.shortcuts.connect(
            Gdk.keyval_from_name("i"),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE,
            self.on_import_database,
        )

        # Ctrl+E to export database
        self.shortcuts.connect(
            Gdk.keyval_from_name("e"),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE,
            self.on_export_database,
        )

    @property
    def safe_clipboard(self) -> str:
        """
        Returns content from safe clipboard, then automatically clears the clipboard.
        This is done for safety.
        """

    @safe_clipboard.setter
    def safe_clipboard(self, value: str):
        """
        Puts `value` into safe clipboard and starts one minute timer to auto clear the clipboard.
        This is done for safety.
        """

        # TODO: use GObject.timeout_add() to add callback to clear safe clipboard
        # TODO: use it correctly! without overwriting the timer when copying again

    @staticmethod
    def load_css():
        """
        Loads styles from global.css
        """
        # TODO: substitute font from settings.json
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("ui/global.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )

    def get_databases(self):
        """
        Builds a sorted list of databases residing in SRC_DIR folder.
        """

        dbs = []
        for file in glob.glob(f"{core.SRC_DIR}/*.dba"):
            name = Path(file).stem
            dbs.append(Database(name))
        dbs.sort()
        self.databases = dbs

    def load_databases(self):
        """
        Populates db_list with items.
        """

        self.db_list.sort_func = abc_list_sort
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/icon.svg", 50, 50, True)

        for db in self.databases:
            add_list_item(self.db_list, pixbuf, db.name)

    def select_main_database(self):
        """
        If there is a database called `main` auto selects it
        (but only if the appropriate feature is turned on).
        """

        if not self.config.main_db:
            return

        for row in self.db_list.children:
            if item_name(row) == "main":
                self.db_list.select_row(row)
                break

    def on_database_selected(self, _, row: Gtk.ListBoxRow):
        """
        If selected database is closed – displays open database form.
        :param row: row containing selected database name.
        """

        if not row:
            return

        index = self.db_list.children.index(row)
        selected_db = self.databases[index]

        if not selected_db.opened:
            form = OpenDatabase(selected_db, self)
            self.show_form(form)

    def import_database(self, path: str):
        """
        Imports given database handling all errors.
        :param path: path to database file we're trying to import.
        """

        if f"{Path(path).stem}.dba" in os.listdir(core.SRC_DIR):
            IconDialog("Warning!", WARNING_DB_EXISTS, "dialog-warning").run()
            return

        if os.path.getsize(path) < 116:
            IconDialog("Warning!", WARNING_DB_CORRUPTED, "dialog-warning").run()
            return

        try:
            shutil.copy(path, core.SRC_DIR)
        except Exception as err:
            logging.error(traceback.format_exc())
            ErrorDialog(ERROR_DB_IMPORT, err).run()
            return

        db = Database(Path(path).stem)
        self.databases.append(db)
        self.databases.sort()

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/icon.svg", 50, 50, True)
        add_list_item(self.db_list, pixbuf, db.name)
        self.db_list.show_all()

        self.statusbar.success(SUCCESS_DB_IMPORT)

    def on_import_database(self, *args):
        """
        Displays import database dialog.
        """

        dialog = Gtk.FileChooserDialog(IMPORT_DATABASE_TITLE)

        dba_filter = Gtk.FileFilter()
        dba_filter.name = "Account database (*.dba)"
        dba_filter.add_mime_type("application/account-database")
        dialog.add_filter(dba_filter)

        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button("Import", Gtk.ResponseType.ACCEPT)

        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.ACCEPT:
            self.import_database(dialog.filename)

    def export_database(self, database: Database, path: str):
        """
        Exports given database handling all errors.
        :param path: where to export the database.
        """

        try:
            shutil.copy(database.dba_file, path)
        except Exception as err:
            logging.error(traceback.format_exc())
            ErrorDialog(ERROR_DB_EXPORT, err).run()
            return
        self.statusbar.success(SUCCESS_DB_EXPORT)

    def on_export_database(self, *args):
        """
        Displays export database dialog.
        """

        dialog = Gtk.FileChooserDialog(
            title=EXPORT_DATABASE_TITLE,
            action=Gtk.FileChooserAction.SAVE,
        )
        self.dialog = dialog

        row = self.db_list.selected_row
        if not row:
            self.statusbar.warning(SELECT_DB_TO_EXPORT)
            return

        # set default file name of the export dialog to <db_name>.dba
        index = self.db_list.children.index(row)
        selected_db = self.databases[index]
        dialog.current_name = selected_db.dba_file.name

        dba_filter = Gtk.FileFilter()
        dba_filter.name = "Account database (*.dba)"
        dba_filter.add_mime_type("application/account-database")
        dialog.add_filter(dba_filter)

        dialog.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        dialog.add_button("Export", Gtk.ResponseType.ACCEPT)

        response = dialog.run()
        dialog.hide()
        if response == Gtk.ResponseType.ACCEPT:
            self.export_database(selected_db, dialog.filename)

    def do_delete_event(self, _):
        """
        Checks if all databases are closed, if they are – quits, if any of them aren't –
        displays confirmation dialog.
        :returns: True to prevent quiting and False to allow it.
        """

        if any(database.opened for database in self.databases):
            response = WarningDialog(CONFIRM_QUIT).run()
            if response == Gtk.ResponseType.NO:
                return True
        return False

    def on_quit(self, _):
        self.application.quit()

    def on_create_database(self, _):
        """
        Displays create database form.
        """

        form = CreateDatabase(self)
        self.show_form(form)

    def on_edit_database(self, _):
        """
        If selected database is opened – displays edit database form,
        otherwise – rename database form.
        """

        # show warning in statusbar if there is no database selected
        row = self.db_list.selected_row
        if not row:
            self.statusbar.warning(SELECT_DB_TO_EDIT)
            return

        index = self.db_list.children.index(row)
        selected_db = self.databases[index]

        if selected_db.opened:
            form = EditDatabase(selected_db, self)
        else:
            form = RenameDatabase(selected_db, self)
        self.show_form(form)

    def delete_database(self, database: Database):
        """
        Deletes given database from disk and database list, handling all errors.
        """

        try:
            database.dba_file.unlink()
        except Exception as err:
            logging.error(traceback.format_exc())
            ErrorDialog(ERROR_DB_DELETION, err).run()
            return

        self.databases.remove(database)
        delete_list_item(self.db_list, database.name)

        self.form_box.foreach(lambda form: self.form_box.remove(form))
        self.statusbar.success(SUCCESS_DB_DELETED)

    def on_delete_database(self, _):
        """
        Displays confirmation dialog asking user if he really want's to delete
        selected database.
        """

        # show warning in statusbar if there is no database selected
        row = self.db_list.selected_row
        if not row:
            self.statusbar.warning(SELECT_DB_TO_DELETE)
            return

        index = self.db_list.children.index(row)
        selected_db = self.databases[index]

        message = CONFIRM_DB_DELETION.format(selected_db.name)
        response = WarningDialog(message).run()

        if response == Gtk.ResponseType.YES:
            self.delete_database(selected_db)
