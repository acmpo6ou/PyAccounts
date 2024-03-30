#!/usr/bin/env python3

#  Copyright (c) 2021-2023. Bohdan Kolvakh
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

import time
import platform
from pathlib import Path

import gi
import setproctitle as setproctitle

from core import SRC_DIR

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gio

import sys
from signal import signal, SIGUSR1

# noinspection PyUnresolvedReferences
import core.gtk_utils
from core.main_window import MainWindow
from core.widgets import IconDialog

if platform.system() == "Linux":
    from core.linux_keyboard import write
else:
    from keyboard import write

CUSTOM_KEYS_PARENT_SCHEMA = "org.cinnamon.desktop.keybindings"
CUSTOM_KEYS_BASENAME = "/org/cinnamon/desktop/keybindings/custom-keybindings"
CUSTOM_KEYS_SCHEMA = "org.cinnamon.desktop.keybindings.custom-keybinding"
PASTE_SCRIPT = "/usr/share/pyaccounts/PyAccounts/paste.sh"


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
            setproctitle.setproctitle("PyAccounts")
        else:
            dialog = IconDialog(
                "PyAccounts is already running",
                "Only one application instance can run at a time.",
                icon="dialog-warning",
            )
            dialog.show_all()

    def do_open(self, files: list[Gio.File], *args):
        """ Imports .dba files given in [files] list. """
        if not self.window:
            self.do_activate()

        for file in files:
            if file.path.endswith(".dba"):
                self.window.import_database(file.path)

    @staticmethod
    def fix_src_dir():
        """ Creates the SRC_DIR folder if it's absent. """
        src_dir = Path(SRC_DIR)
        if not src_dir.exists():
            src_dir.mkdir()

    @staticmethod
    def fix_settings():
        """ Creates empty settings.json if it's absent. """
        file = Path(SRC_DIR) / "settings.json"
        file.touch()

    @staticmethod
    def check_paste_shortcut() -> bool:
        """ Checks if there is a system shortcut to paste password. """

        # paste shortcut is a linux-only feature
        if platform.system() != "Linux":
            return True

        parent = Gio.Settings.new(CUSTOM_KEYS_PARENT_SCHEMA)
        custom_list = parent.get_strv("custom-list")

        for entry in custom_list:
            if entry == "__dummy__":
                continue

            path = f"{CUSTOM_KEYS_BASENAME}/{entry}/"
            schema = Gio.Settings.new_with_path(CUSTOM_KEYS_SCHEMA, path)
            if schema.get_string("name") == "PyAccounts":
                return True
        return False

    @staticmethod
    def create_paste_shortcut():
        """ Creates system shortcut to paste password. """
        parent = Gio.Settings.new(CUSTOM_KEYS_PARENT_SCHEMA)
        array = parent.get_strv("custom-list")
        array.append("custom100")
        parent.set_strv("custom-list", array)

        path = f"{CUSTOM_KEYS_BASENAME}/custom100/"
        new_schema = Gio.Settings.new_with_path(CUSTOM_KEYS_SCHEMA, path)
        new_schema.set_string("name", "PyAccounts")
        new_schema.set_string("command", PASTE_SCRIPT)
        new_schema.set_strv("binding", ('<Super>v',))

    def on_paste(self, *args):
        """
        Called when system shortcut (usually Super+V) to paste password from safe clipboard is
        pressed. Sends key press events to X server to simulate password typing.
        """
        time.sleep(0.1)
        write(self.window.safe_clipboard)


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
