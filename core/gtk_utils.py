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

"""
Contains various utilities to simplify development with GTK.
"""
from enum import IntEnum

from gi.repository import GObject, Gtk, Gio


# noinspection PyUnresolvedReferences
def _getattr(self, item: str):
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
        return object.__getattribute__(self.props, item)
    except AttributeError:
        return object.__getattribute__(self, f"get_{item}")()


# noinspection PyUnresolvedReferences
def _setattr(self, item: str, value):
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


def delete_item(self, item_name: str):
    """
    An extension function for Gtk.ListBox.
    Removes item from Gtk.ListBox by its name.
    """

    """
    iterate through self.widgets:
        get first child from widget
        if child text equals item_name:
            remove widget from self
            break
    """


class ListOrder(IntEnum):
    """Used by abc_list_sort sort function to indicate the order of Gtk.ListBoxRow items."""

    ROW1_ROW2 = -1
    EQUAL = 0
    ROW2_ROW1 = 1


def abc_list_sort(row1: Gtk.ListBoxRow, row2: Gtk.ListBoxRow) -> ListOrder:
    """
    Sort function for Gtk.ListBox to sort its items alphabetically.

    For more details see:
    https://lazka.github.io/pgi-docs/Gtk-3.0/callbacks.html#Gtk.ListBoxSortFunc
    """
    ...


# now Gtk.ListBox will have a convenient method to remove it's items by name
Gtk.ListBox.delete = delete_item


class GladeTemplate(Gtk.Bin):
    """
    Simplifies loading of glade ui files.
    This class should be subclassed to automatically load needed ui file.
    """

    def __init__(self, template: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.builder = Gtk.Builder.new_from_file(f"ui/{template}.glade")
        self.parent_widget = self.builder.get_object(template)
        self.add(self.parent_widget)
        self.builder.connect_signals(self)

    # noinspection PyUnresolvedReferences
    def __getattr__(self, item: str):
        """
        Simplifies widget access, instead of making builder.get_object() calls we can
        access widgets directly as attributes.

        Instead of writing this:
        >>> form.builder.get_object("mywidget")
        We can do this:
        >>> form.mywidget

        :param item: id of the widget.
        """
        # try to get widget from builder
        builder = object.__getattribute__(self, "builder")
        widget = builder.get_object(item)

        # if worked, return the widget
        if widget:
            attrs = object.__getattribute__(self, "__dict__")
            attrs[item] = widget  # cache it
            return widget

        # else, attribute we're trying to get is not a widget, so we return it the normal way
        return object.__getattribute__(self, item)


def load_icon(icon_name: str, size: int) -> Gtk.Image:
    """
    Returns icon from default theme.
    """
    icon_theme = Gtk.IconTheme.get_default()
    icon = icon_theme.load_icon(icon_name, size, Gtk.IconLookupFlags.FORCE_SVG)
    return Gtk.Image.new_from_pixbuf(icon)


def get_mime_icon(path: str) -> Gtk.Image:
    """
    Returns mime icon associated with file given in `path`.
    :param path: path to file icon of which we want to get.
    """
    # TODO: test this function; it returns Image, test image.pixbuf property
    file = Gio.File.new_for_path(path)
    info = file.query_info("standard::*", Gio.FileQueryInfoFlags.NONE, None)
    return load_icon(info.icon.names[0], 64)
