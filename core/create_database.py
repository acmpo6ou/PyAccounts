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

from core.widgets import CreateForm, FilterDbNameMixin

if typing.TYPE_CHECKING:
    from core.main_window import MainWindow


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

    def on_apply(self, _):
        """
        Creates database using form data and handling all errors
        """

        # TODO: create database, add it to databases list, update list of databases,
        #  open database window
        # TODO: on error show error dialog
        # TODO: destroy form on success
