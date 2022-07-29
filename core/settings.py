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
import json
import logging
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from gi.repository import Gtk

from core import SRC_DIR
from core.gtk_utils import GladeTemplate

if TYPE_CHECKING:
    from core.main_window import MainWindow


class SettingsDialog(GladeTemplate):
    # <editor-fold>
    parent_widget: Gtk.Dialog
    general_font: Gtk.FontButton
    mono_font: Gtk.FontButton
    main_db: Gtk.Switch

    # </editor-fold>

    def __init__(self, main_window: "MainWindow"):
        super().__init__("settings")
        self.main_window = main_window
        self.load_settings()

    def run(self):
        self.parent_widget.show()

    def on_cancel(self, _):
        self.destroy()

    def load_settings(self):
        config = self.main_window.config
        self.general_font.font_name = config.general_font
        self.mono_font.font_name = config.monospace_font
        self.main_db.active = config.main_db

    def on_save(self, _=None):
        """ Saves fonts to settings.json and applies changes. """
        config = self.main_window.config
        config.general_font = self.general_font.font_name
        config.monospace_font = self.mono_font.font_name
        config.main_db = self.main_db.active

        config.save()
        self.main_window.load_css()
        self.destroy()


@dataclass
class Config:
    """
    Represents app settings.
    """

    separator_position = 1000
    main_db = False
    general_font = "Ubuntu 30"
    monospace_font = "Ubuntu Mono 35"

    def __post_init__(self):
        self.load()

    def load(self):
        """ Loads settings from settings.json """
        path = Path(SRC_DIR) / "settings.json"

        try:
            file = open(path)
            settings = json.load(file)
        except Exception:
            logging.error(traceback.format_exc())
            return

        self.__dict__ = settings

    def save(self):
        """ Saves settings to settings.json """
        path = Path(SRC_DIR) / "settings.json"

        try:
            file = open(path, "w")
            json.dump(self.__dict__, file)
        except Exception:
            logging.error(traceback.format_exc())
            return
