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

# noinspection PyUnresolvedReferences
import core.gtk_utils
from core.main_window import MainWindow
from core.widgets import IconDialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="com.acmpo6ou.PyAccounts", **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self, title="PyAccounts")
            self.window.show_all()

            self.fix_src_dir()
            self.check_paste_shortcut()
            # TODO: set process name to `PyAccounts` using setproctitle;
            #  see StackOverflow: https://stackoverflow.com/a/18992161
        else:
            dialog = IconDialog(
                "PyAccounts is already running",
                "Only one application instance can run at a time.",
                icon="dialog-warning",
            )
            dialog.show_all()

    def fix_src_dir(self):
        """
        Creates the SRC_DIR folder if it's absent.
        """
        # TODO: also call fix_settings

    def fix_settings(self):
        """
        Creates empty settings.json if it's absent.
        """

    def check_paste_shortcut(self):
        """
        Checks if there is a system shortcut to paste password, if there isn't creates it.
        """

    def create_paste_shortcut(self):
        """
        Creates system shortcut to paste password.
        """


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
