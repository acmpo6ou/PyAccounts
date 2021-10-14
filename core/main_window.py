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

    def on_import_database(self, _):
        """
        Displays import database dialog.
        """

    def on_export_database(self, _):
        """
        Displays export database dialog.
        """

    def on_quit(self, _):
        """
        Checks if all databases are closed, if they are – quits, if they aren't – displays
        confirmation dialog.
        """
