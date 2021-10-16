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

"""
Contains custom GTK widgets.
"""

import gi

from core.gtk_utils import GladeTemplate
from core.settings import SettingsDialog

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class IconDialog(Gtk.Dialog):
    """
    Dialog containing icon and message.
    """

    vbox = None

    def __init__(self, title, message, icon, *args, **kwargs):
        super().__init__(self, title=title, *args, **kwargs)
        self.vbox = self.content_area
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox.add(box)

        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon(icon, 48, Gtk.IconLookupFlags.FORCE_SVG)
        image = Gtk.Image.new_from_pixbuf(icon)
        image.margin = 10
        box.add(image)

        label = Gtk.Label(message)
        label.margin = 10
        box.add(label)

    def run(self):
        self.show_all()
        response = super().run()
        self.destroy()
        return response


class WarningDialog(IconDialog):
    """
    Dialog with warning icon and 2 buttons: `Yes` and `No`.
    """

    def __init__(self, message, *args, **kwargs):
        super().__init__(
            title="Warning!",
            message=message,
            icon="dialog-warning",
            modal=True,
            buttons=("No", Gtk.ResponseType.NO, "_Yes", Gtk.ResponseType.YES),
            *args,
            **kwargs,
        )


class ErrorDialog(IconDialog):
    """
    Dialog with error icon, error message and details.
    """

    def __init__(self, message, details, *args, **kwargs):
        super().__init__(
            title="Error!",
            message=message,
            icon="dialog-error",
            modal=True,
            *args,
            **kwargs,
        )
        details_label = Gtk.Label()
        details_label.markup = f"<span font_desc='Ubuntu Mono 20'>{details}</span>"
        details_label.selectable = True
        details_label.xalign = 0
        details_label.margin_start = 5
        details_label.margin_end = 5

        expander = Gtk.Expander.new_with_mnemonic("_Details")
        expander.add(details_label)
        self.vbox.add(expander)


class StatusBar:
    """
    A wrapper for Gtk.Statusbar to display messages that disappear in 15 seconds.
    """

    def __init__(self, statusbar):
        self.statusbar = statusbar

    def message(self, message):
        """
        Displays message that disappears in 15 seconds on status bar.
        """
        # TODO: use GObject.timeout_add() to add callback to clear status bar in 15 seconds.

    def success(self, message):
        """
        Displays a success message.
        """
        # TODO: display ✔ before the message

    def warning(self, message):
        """
        Displays a warning.
        """
        # TODO: display ✘ before the message


class Window(Gtk.Window, GladeTemplate):
    """
    Super class for MainWindow and DatabaseWindow.
    """

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(1280, 720)
        self.set_icon_from_file("img/icon.svg")
        self.load_separator()
        self.statusbar = StatusBar(self.statusbar)

    def load_separator(self):
        """
        Loads separator position from settings.json
        """

    def on_separator_moved(self, separator, _):
        """
        Saves separator position to settings.json
        """

    def on_preferences(self, _):
        """
        Displays preferences dialog.
        """
        SettingsDialog(self.main_window).run()

    def on_about(self, _):
        """
        Displays about dialog.
        """
        # TODO: set dialog version to current app version
