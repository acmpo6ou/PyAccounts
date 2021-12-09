#!/usr/bin/env python3.9

#  Copyright (c) 2021. Bohdan Kolvakh
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

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gio

import sys
from signal import signal, SIGUSR1

# noinspection PyUnresolvedReferences
import core.gtk_utils
from core.main_window import MainWindow
from core.widgets import IconDialog


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="com.acmpo6ou.PyAccounts",
            flags=Gio.ApplicationFlags.HANDLES_OPEN,
            **kwargs
        )
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self, title="PyAccounts")
            self.window.show_all()

            self.fix_src_dir()
            self.fix_settings()

            if not self.check_paste_shortcut():
                self.create_paste_shortcut()

            signal(SIGUSR1, self.on_paste)

            # TODO: set process name to `PyAccounts` using setproctitle;
            #  see StackOverflow: https://stackoverflow.com/a/18992161
        else:
            # TODO: possibly test this dialog
            dialog = IconDialog(
                "PyAccounts is already running",
                "Only one application instance can run at a time.",
                icon="dialog-warning",
            )
            dialog.show_all()

    def do_open(self, files: list[Gio.File], *args):
        """
        Imports .dba files given in [files] list.
        """
        if not self.window:
            self.do_activate()

        # TODO: iterate over files, use file.path to get absolute file path
        # TODO: skip non .dba files
        # TODO: call self.window.import_database for each path

    def fix_src_dir(self):
        """
        Creates the SRC_DIR folder if it's absent.
        """

    def fix_settings(self):
        """
        Creates empty settings.json if it's absent.
        """

    def check_paste_shortcut(self):
        """
        Returns boolean value indicating whether there is a system shortcut to paste password.
        """

    def create_paste_shortcut(self):
        """
        Creates system shortcut to paste password.
        """

    def on_paste(self, *args):
        """
        Called when system shortcut (usually Super+V) to paste password from safe clipboard is
        pressed. Sends key press events to X server to simulate password typing.
        """
        # TODO: use keyboard module to paste password from window.safe_clipboard


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
