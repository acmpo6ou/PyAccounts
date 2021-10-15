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
            **kwargs
        )


class StatusBar:
    """
    A wrapper for Gtk.Statusbar to display messages that disappear in 15 seconds.
    """

    def __init__(self, statusbar):
        self.statusbar = statusbar

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
