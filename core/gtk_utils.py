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

"""
Contains various utilities to simplify development with GTK.
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
        self.vbox = self.get_content_area()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox.add(hbox)

        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon(icon, 48, Gtk.IconLookupFlags.FORCE_SVG)
        image = Gtk.Image.new_from_pixbuf(icon)
        image.props.margin = 10
        hbox.add(image)

        label = Gtk.Label(message)
        label.props.margin = 10
        hbox.add(label)

    def run(self):
        self.show_all()
        response = super().run()
        self.destroy()
        return response
