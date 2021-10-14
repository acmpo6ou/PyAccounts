#!/usr/bin/env python3

from gi.repository import Gtk, Gdk
from core.gtk_utils import GladeTemplate


class MainWindow(Gtk.ApplicationWindow, GladeTemplate):
    def __init__(self, *args, **kwargs):
        super(Gtk.ApplicationWindow, self).__init__(*args, **kwargs)
        GladeTemplate.__init__(self, "main_window")
        self.load_css()
        self.set_default_size(1280, 720)

    @staticmethod
    def load_css():
        """
        Loads styles from global.css.
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("ui/global.css")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )

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

    def on_create_database(self, _):
        """
        Displays create database form.
        """

    def on_edit_database(self, _):
        """
        Displays edit database form for selected database.
        """
        # TODO: show warning in statusbar if there is no database selected

    def delete_database(self, name):
        """
        Deletes given database from disk and database list handling all errors.
        :param name: name of the database to delete.
        """
        # TODO: show success message in statusbar if database is deleted successfully
        # TODO: show error message if there is an error

    def on_delete_database(self, _):
        """
        Displays confirmation dialog asking user if he really want's to delete selected database.
        """
        # TODO: show warning in statusbar if there is no database selected
