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

from gi.repository import Gtk

from core.database_utils import Database
from core.gtk_utils import GladeTemplate
from core.widgets import FilterDbNameMixin, ValidateNameMixin

if typing.TYPE_CHECKING:
    from core.main_window import MainWindow


class RenameDatabase(GladeTemplate, FilterDbNameMixin, ValidateNameMixin):
    # <editor-fold>
    parent_widget: Gtk.Box
    title: Gtk.Label
    name: Gtk.Entry
    name_error: Gtk.Label
    apply: Gtk.Button

    # </editor-fold>

    @property
    def items(self):
        dbs = [database.name for database in self.main_window.databases]
        # it's OK if database name hasn't changed throughout editing
        dbs.remove(self.database.name)
        return dbs

    def __init__(self, database: Database, main_window: "MainWindow"):
        super().__init__("rename_database")
        self.database = database
        self.main_window = main_window
        # TODO: change title text to `Rename [database name] database`
        # TODO: make database name cursive
        # TODO: populate name field with database name

    def on_apply_enabled(self, _):
        """
        Enables or disables apply button depending on whether database name entered to the name
        field is valid.
        """
        self.validate_name()

    def on_apply(self, _):
        """
        Renames database using the name from name field.
        """

        # TODO: call database.rename() handling errors
        # TODO: update database list and destroy self on success
        # TODO: use ListBox.delete(name)
