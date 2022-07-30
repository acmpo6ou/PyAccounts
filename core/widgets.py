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
Contains custom GTK widgets.
"""
import base64
import logging
import re
import tempfile
import traceback
import typing
from datetime import datetime

from gi.repository import Gtk, Gdk, GLib

from core.about import AboutDialog
from core.database_utils import Database
from core.generate_password import GenPassDialog
from core.gtk_utils import GladeTemplate, load_icon, add_list_item, get_mime_icon
from core.settings import SettingsDialog, Config

if typing.TYPE_CHECKING:
    from core.main_window import MainWindow

NAME_TAKEN_ERROR = "This name is already taken!"
EMPTY_NAME_ERROR = "Please, provide a name!"
UNALLOWED_CHARS_WARNING = \
    "Only latin symbols, numbers and .()-_ are allowed" \
    " to use in the database name."


class IconDialog(Gtk.Dialog):
    """
    Dialog containing icon and message.
    """

    # DO NOT REMOVE THIS, this is needed because of strange issues with
    # _setattr from gtk_utils
    vbox = None

    def __init__(self, title: str, message: str, icon: str, *args, **kwargs):
        super().__init__(self, title=title, modal=True, *args, **kwargs)
        self.vbox = self.content_area
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.vbox.add(box)

        image = load_icon(icon, 64)
        image.margin = 10
        box.add(image)

        label = Gtk.Label(message, use_markup=True)
        label.margin = 10
        box.add(label)

    def run(self) -> Gtk.ResponseType:
        self.show_all()
        response = super().run()
        self.destroy()
        return response


class WarningDialog(IconDialog):
    """
    Dialog with warning icon and 2 buttons: `Yes` and `No`.
    """

    def __init__(self, message: str, buttons: tuple = None, *args, **kwargs):
        if not buttons:
            buttons = ("_No", Gtk.ResponseType.NO, "Yes", Gtk.ResponseType.YES)

        super().__init__(
            title="Warning!",
            message=message,
            icon="dialog-warning",
            buttons=buttons,
            *args,
            **kwargs,
        )


class ErrorDialog(IconDialog):
    """
    Dialog with error icon, error message and details.
    """

    def __init__(self, message: str, err: Exception, *args, **kwargs):
        super().__init__(
            title="Error!",
            message=message,
            icon="dialog-error",
            *args,
            **kwargs,
        )

        # fmt: off
        error_class = str(err.__class__) \
            .removeprefix("<class '") \
            .removesuffix("'>")
        # fmt: on
        details = f"{error_class}:\n{err}"

        details_label = Gtk.Label()
        details_label.markup = f"<span font_desc='Ubuntu Mono 20'>{details}</span>"
        details_label.selectable = True
        details_label.line_wrap = True
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
    calendar: Gtk.Calendar

    def __init__(self, date_str: str):
        super().__init__("date_chooser")
        date = datetime.strptime(date_str, "%d.%m.%Y").date()
        self.calendar.select_month(date.month - 1, date.year)
        self.calendar.select_day(date.day)

    def run(self) -> Gtk.ResponseType:
        response = self.parent_widget.run()
        self.destroy()
        return response


class StatusBar:
    """
    A wrapper around Gtk.Label to display messages that disappear in 15 seconds.
    """

    def __init__(self, label: Gtk.Label):
        self.label = label

    def clear(self):
        self.label.text = ""

    def message(self, message: str, time=15):
        """
        Displays message that disappears in 15 seconds on status bar.
        :param time: used in tests not to wait 15 seconds.
        """

        self.label.markup = message
        GLib.timeout_add_seconds(time, self.clear)

    def success(self, message: str):
        """
        Displays a success message.
        """
        self.message(f"<span color='#6db442'>✔</span> {message}")

    def warning(self, message: str):
        """
        Displays a warning.
        """
        self.message(f"<span color='#f04a50'>✘</span> {message}")


class Window(Gtk.Window, GladeTemplate):
    """
    Super class for MainWindow and DatabaseWindow.
    """

    form_box: Gtk.Box
    separator: Gtk.Paned
    config: Config

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(1280, 720)
        self.set_icon_from_file("img/icon.svg")
        self.statusbar = StatusBar(self.status_bar)

        self.shortcuts = Gtk.AccelGroup()
        self.add_accel_group(self.shortcuts)

        # F1 to open About dialog
        self.shortcuts.connect(
            Gdk.keyval_from_name("F1"),
            0,  # don't use any modifiers (e.g. Ctrl or Shift)
            Gtk.AccelFlags.VISIBLE,
            self.on_about,
        )

    def show_form(self, form: GladeTemplate):
        """
        Adds given form to form_box removing currently shown form.
        :param form: form to display.
        """

        self.form_box.foreach(lambda form: self.form_box.remove(form))
        self.form_box.add(form)
        form.show()

    def load_separator(self):
        """ Loads separator position from settings.json """
        self.separator.position = self.config.separator_position

    def on_separator_moved(self, separator: Gtk.Paned, _):
        """ Saves separator position to settings.json """
        self.config.separator_position = separator.position
        self.config.save()

    def on_preferences(self, _):
        """ Displays preferences dialog. """
        SettingsDialog(self.main_window).run()

    @staticmethod
    def on_about(*_):
        """ Displays about dialog. """
        AboutDialog().run()


class FilterDbNameMixin:
    main_window: "MainWindow"

    def on_filter_name(self, entry: Gtk.Entry):
        """
        Removes unallowed characters from database name.
        Shows a warning explaining the user that he's trying to enter unallowed characters.
        """

        old_name = entry.text
        cleaned = re.sub(r"[^-_().a-zA-Z\d ]", '', entry.text)
        entry.text = cleaned

        if cleaned != old_name:
            self.main_window.statusbar.warning(UNALLOWED_CHARS_WARNING)


class ValidateNameMixin:
    # <editor-fold>
    name: Gtk.Entry
    name_error: Gtk.Label
    items: list[Database]

    # </editor-fold>

    def validate_name(self) -> bool:
        """
        Validates name field, displaying error tip if database name is invalid.

        Possible problems with database name:
        * name field is empty
        * name field contains name that is already taken;

        Note that for RenameDatabase, EditDatabase and EditAccount it's OK
         if database name hasn't changed throughout editing, and they will
         implement the `items` getter appropriately.
        :return: True if name is valid.
        """

        if self.name.text == "":
            self.name_error.show()
            self.name_error.text = EMPTY_NAME_ERROR
            return False
        else:
            self.name_error.hide()

        if self.name.text in self.items:
            self.name_error.show()
            self.name_error.text = NAME_TAKEN_ERROR
            return False

        return True


class AttachedFilesMixin:
    attached_files: Gtk.ListBox

    def load_attached_files(self, attached_files: dict[str, typing.Any]):
        """
        Populates attached_files list with attached files.
        """

        for file in attached_files:
            tmp = tempfile.NamedTemporaryFile("wb")
            try:
                data = attached_files[file].encode()
                content = base64.b64decode(data)
                tmp.write(content)
                tmp.flush()
            except Exception:
                logging.error(traceback.format_exc())

            icon = get_mime_icon(tmp.name)
            add_list_item(self.attached_files, icon.pixbuf, file)


class CreateForm(GladeTemplate, ValidateNameMixin):
    """
    Super class for CreateDatabase and CreateAccount.
    """
    # <editor-fold>
    name: Gtk.Entry
    password: Gtk.Entry
    repeat_password: Gtk.Entry
    name_error: Gtk.Label
    password_error: Gtk.Label
    passwords_diff_error: Gtk.Label
    apply: Gtk.Button
    items: list[Database]
    # </editor-fold>

    APPLY_BUTTON_TEXT = "_Create"

    def validate_passwords(self) -> bool:
        """
        Validates password fields, displaying error tips if passwords are invalid.

        Possible problems with passwords:
        * password fields are empty
        * passwords from password fields don't match
        :return: True if passwords are valid.
        """
        result = True

        if self.password.text != self.repeat_password.text:
            self.passwords_diff_error.show()
            result = False
        else:
            self.passwords_diff_error.hide()

        if self.password.text == "":
            self.password_error.show()
            result = False
        else:
            self.password_error.hide()

        return result

    def on_apply_enabled(self, _):
        """
        Enables or disables apply button depending on whether there are errors in the form.
        """

        name_good = self.validate_name()
        passwords_good = self.validate_passwords()
        self.apply.sensitive = name_good and passwords_good

        # This is needed because when button is disabled the ✨ emoji
        # doesn't appear greyed out, so we just remove it
        # and display the emoji only when button is enabled
        emoji = "✨ " if name_good and passwords_good else ""
        self.apply.label = f"{emoji}{self.APPLY_BUTTON_TEXT}"

    def on_generate_password(self, _):
        """
        Displays dialog to generate password.
        """
        GenPassDialog(self.password, self.repeat_password).show_all()

    def on_icon_press(self, entry, icon_pos, _):
        if icon_pos == Gtk.EntryIconPosition.PRIMARY:
            self.toggle_password_visibility()
        else:
            self.clear_password(entry)

    def toggle_password_visibility(self):
        """
        Toggles password visibility of both password fields.
        """

        visibility = self.password.visibility
        self.password.visibility = not visibility
        self.repeat_password.visibility = not visibility

        icon_name = "visibility" if visibility else "image-red-eye"
        self.password.set_icon_from_icon_name(
            Gtk.EntryIconPosition.PRIMARY, icon_name
        )
        self.repeat_password.set_icon_from_icon_name(
            Gtk.EntryIconPosition.PRIMARY, icon_name
        )

    @staticmethod
    def clear_password(entry: Gtk.Entry):
        entry.text = ""
