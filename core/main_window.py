#!/usr/bin/env python3

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
from core.widgets import StatusBar

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from core.gtk_utils import GladeTemplate


class MainWindow(Gtk.ApplicationWindow, GladeTemplate):
    def __init__(self, *args, **kwargs):
        super(Gtk.ApplicationWindow, self).__init__(*args, **kwargs)
        GladeTemplate.__init__(self, "main_window")

        self.load_css()
        self.load_settings()

        self.set_default_size(1280, 720)
        self.set_icon_from_file("img/icon.svg")

        self.statusbar = StatusBar(self.statusbar)

    @staticmethod
    def load_css():
        """
        Loads styles from global.css
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("ui/global.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )

    def load_settings(self):
        """
        Loads settings on app startup.
        """
        # TODO: load separator position

    def on_separator_moved(self, separator, _):
        """
        Saves separator position to settings.json
        """

    def on_database_selected(self, db_list, row):
        """
        If database closed – display open database form.
        :param row: row containing selected database name.
        """

    def import_database(self, path):
        """
        Imports given database handling all errors.
        :param path: path to database file we're trying to import.
        """
        # TODO: show success and error messages
        # TODO: validate database file size, whether database already exists

    def on_import_database(self, _):
        """
        Displays import database dialog.
        """
        # TODO: allow only .dba files

    def export_database(self, name):
        """
        Exports given database handling all errors.
        :param name: name of the database we're trying to export.
        """
        # TODO: show success and error messages

    def on_export_database(self, _):
        """
        Displays export database dialog.
        """

    def on_quit(self, _):
        """
        Checks if all databases are closed, if they are – quits, if they aren't – displays
        confirmation dialog.
        """

    def on_preferences(self, _):
        """
        Displays preferences dialog.
        """

    def on_about(self, _):
        """
        Displays about dialog.
        """
        # TODO: set dialog version to current app version

    def on_create_database(self, _):
        """
        Displays create database form.
        """

    def on_edit_database(self, _):
        """
        Displays edit database form for selected database.
        """
        # TODO: show warning in statusbar if there is no database selected
        #  or if database is closed
        # TODO: call form.database = name

    def delete_database(self, name):
        """
        Deletes given database from disk and database list handling all errors.
        :param name: name of the database to delete.
        """
        # TODO: show success message in statusbar if database is deleted successfully
        # TODO: show error message if there is an error
        # TODO: deselect any database

    def on_delete_database(self, _):
        """
        Displays confirmation dialog asking user if he really want's to delete selected database.
        """
        # TODO: show warning in statusbar if there is no database selected
