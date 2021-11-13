#!/usr/bin/env python3

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

"""
Contains custom GTK widgets.
"""

from gi.repository import Gtk, Gdk

from core.about import AboutDialog
from core.gtk_utils import GladeTemplate, load_icon
from core.settings import SettingsDialog


class IconDialog(Gtk.Dialog):
    """
    Dialog containing icon and message.
    """

    # DO NOT REMOVE THIS, this is needed because of strange issues with _setattr from gtk_utils
    vbox = None

    def __init__(self, title, message, icon, *args, **kwargs):
        super().__init__(self, title=title, modal=True, *args, **kwargs)
        self.vbox = self.content_area
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox.add(box)

        image = load_icon(icon, 64)
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
            buttons=("_No", Gtk.ResponseType.NO, "Yes", Gtk.ResponseType.YES),
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


class DateChooserDialog(GladeTemplate):
    """
    A dialog to choose date.
    """

    def __init__(self):
        super().__init__("date_chooser")

    def run(self):
        response = self.parent_widget.run()
        self.destroy()
        return response


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

        self.shortcuts = Gtk.AccelGroup()
        self.add_accel_group(self.shortcuts)

        # TODO: test shortcuts
        # F1 to open About dialog
        self.shortcuts.connect(
            Gdk.keyval_from_name("F1"),
            0,  # don't use any modifiers (e.g. Ctrl or Shift)
            Gtk.AccelFlags.VISIBLE,
            self.on_about,
        )

    def show_form(self, form):
        """
        Adds and shows given form to form_box removing currently shown form.
        :param form: form to display.
        """

        # TODO: remove all forms from form_box, use foreach():
        #  https://lazka.github.io/pgi-docs/Gtk-3.0/classes/Container.html#Gtk.Container.foreach
        # TODO: add the form to form_box and show it

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

    def on_about(self, *args):
        """
        Displays about dialog.
        """
        AboutDialog().run()


class CreateForm(GladeTemplate):
    """
    Super class for CreateDatabase and CreateAccount.
    """

    def validate_name(self):
        """
        Validates name field, displaying error tip if database/account name is invalid.

        Possible problems with the name:
        * name field is empty
        * name field contains name that is already taken
        :return: True if name is valid.
        """
        # TODO: use `items` property to check if name already exists (this property will be
        #  implemented by subclasses

    def validate_passwords(self):
        """
        Validates password fields, displaying error tips if passwords are invalid.

        Possible problems with passwords:
        * password fields are empty
        * passwords from password fields don't match
        :return: True if passwords are valid.
        """

    def on_apply_enabled(self, _):
        """
        Enables or disables apply button depending on whether there are errors in the form.
        """
        # TODO: use validate_passwords and validate_name

    def on_pass_toggle(self, *args):
        """
        Toggles password visibility of both password fields.
        """

    def on_generate_password(self, _):
        """
        Displays dialog to generate password.
        """


class AttachedFilesMixin:
    def load_attached_files(self):
        """
        Populates attached_files list with attached files.
        """

        """
        iterate attached_files dict keys:
            create label with key text
            get icon associated with mime type of attached file using get_mime_type() from gtk_utils
            put icon and label into hbox
            add it to attached_files list box
        """
