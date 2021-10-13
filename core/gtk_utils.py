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
from gi.repository import GObject, Gtk


def _getattr(self, item):
    """
    A fluent API to get GTK object's attributes.

    Instead of writing:
    >>> label.get_text()
    >>> label.props.angle
    This method allows us to write:
    >>> label.text
    >>> label.angle
    Which is a more pythonic API.
    """
    try:
        return getattr(self.props, item)
    except AttributeError:
        return getattr(self, f"get_{item}")()


def _setattr(self, item, value):
    """
    A fluent API to set GTK object's attributes.

    Instead of writing:
    >>> label.set_text("test")
    >>> label.props.angle = 90
    This method allows us to write:
    >>> label.text = "test"
    >>> label.angle = 90
    Which is a more pythonic API.
    """
    try:
        return setattr(self.props, item, value)
    except AttributeError:
        pass

    try:
        getattr(self, f"set_{item}")(value)
    except AttributeError:
        original_setattr(self, item, value)


# save original __setattr__
original_setattr = GObject.Object.__setattr__

# replace __getattr__ and __setattr__ with our methods that provide fluent API
GObject.Object.__getattr__ = _getattr
GObject.Object.__setattr__ = _setattr


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
