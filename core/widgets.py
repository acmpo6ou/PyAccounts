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
