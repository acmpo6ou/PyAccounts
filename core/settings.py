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

from dataclasses import dataclass

from gi.repository import Gtk

from core.gtk_utils import GladeTemplate


class SettingsDialog(GladeTemplate):
    # <editor-fold>
    parent_widget: Gtk.Dialog
    general_font: Gtk.FontButton
    mono_font: Gtk.FontButton
    # </editor-fold>

    def __init__(self, main_window):
        super().__init__("settings")
        self.load_fonts()
        self.main_window = main_window

    def run(self):
        self.parent_widget.show()

    def on_cancel(self, _):
        self.destroy()

    def load_fonts(self):
        """
        Loads font settings from settings.json
        """
        # TODO: use main_window.settings

    def on_save(self, _):
        """
        Saves fonts to settings.json and applies changes.
        """
        # TODO: call main_window.load_css() to apply changes.
        # TODO: use main_window.settings.save()
        # TODO: handle any errors; call self.destroy() on success


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
        """
        Loads settings from settings.json
        """
        # TODO: set fields to loaded settings

    def save(self):
        """
        Saves settings to settings.json
        """
