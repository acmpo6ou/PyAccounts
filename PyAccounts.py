#!/usr/bin/python3

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

import sys

import gi

from core.gtk_utils import IconDialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.load_css()

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


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="com.acmpo6ou.PyAccounts", **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self, title="PyAccounts")
            self.window.show_all()
        else:
            dialog = IconDialog(
                "PyAccounts is already running",
                "Only one application instance can run at the same time.",
                icon="dialog-warning",
            )
            dialog.show_all()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
