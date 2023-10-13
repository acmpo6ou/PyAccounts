#  Copyright (c) 2021-2023. Bohdan Kolvakh
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
import logging
import os
import traceback
from typing import TYPE_CHECKING

from gi.repository import Gdk, Gtk, GdkPixbuf

from core.create_account import CreateAccount
from core.database_utils import Database, AccountClipboard
from core.display_account import DisplayAccount
from core.edit_account import EditAccount
from core.gtk_utils import (
    GladeTemplate,
    load_icon,
    abc_list_sort,
    add_list_item,
    item_name,
    delete_list_item,
)
from core.widgets import Window, WarningDialog, ErrorDialog

if TYPE_CHECKING:
    from core.main_window import MainWindow

ACCOUNT_ICONS_DIR = "img/account_icons/"

SELECT_ACCOUNT_TO_EDIT = "Please select an account to edit."
SELECT_ACCOUNTS_TO_DELETE = "Please select account(s) to delete."
CONFIRM_ACCOUNT_DELETION = "Delete selected accounts?"
CONFIRM_QUIT = (
    "Are you sure you want to close the database?\n"
    "Any unsaved changes will be lost!"
)
SUCCESS_DB_SAVED = "Database saved successfully!"
ERROR_DB_SAVE = "Error saving the database!"

SUCCESS_CUTTING_ACCOUNTS = "Cut account(s)."
SUCCESS_COPYING_ACCOUNTS = "Copied account(s)."
CONFIRM_ACCOUNT_REPLACE = "Account <b>{}</b> already exists in this database, replace?"


class DatabaseWindow(Window):
    # <editor-fold>
    image1: Gtk.Image
    image3: Gtk.Image
    image4: Gtk.Image
    parent_widget: Gtk.Box
    menubar_toolbar: Gtk.Box
    menubar: Gtk.MenuBar
    toolbar: Gtk.Toolbar
    separator: Gtk.Paned
    form_box: Gtk.Box
    accounts_list: Gtk.ListBox
    status_bar: Gtk.Label
    # </editor-fold>

    # it's important to sort icon names by length (longer names first),
    # because this way we will have better matches
    account_icons = [
        icon.removesuffix(".svg")
        for icon in sorted(
            os.listdir(ACCOUNT_ICONS_DIR),
            key=len, reverse=True,
        )
    ]

    def __init__(self, database: Database, main_window: "MainWindow"):
        GladeTemplate.__init__(self, "database_window")
        Window.__init__(self)

        self.main_window = main_window
        self.database = database

        self.config = main_window.config
        self.load_separator()

        self.ctrl_held = False
        self.shift_held = False
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK & Gdk.EventMask.KEY_RELEASE_MASK)
        self.connect("key_press_event", self.keypress)
        self.connect("key_release_event", self.keyrelease)

        # Ctrl+A to select all accounts
        self.shortcuts.connect(
            Gdk.keyval_from_name("a"),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE,
            self.on_select_all,
        )

        # Ctrl+S to save database
        self.shortcuts.connect(
            Gdk.keyval_from_name("s"),
            Gdk.ModifierType.CONTROL_MASK,
            Gtk.AccelFlags.VISIBLE,
            self.on_save,
        )

        self.load_accounts()
        self.title = database.name

    def keypress(self, _, event: Gdk.EventKey):
        """ Allow selecting multiple accounts when Ctrl or Shift is held. """
        if event.keyval == Gdk.KEY_Control_L:
            self.ctrl_held = True
            self.accounts_list.selection_mode = Gtk.SelectionMode.MULTIPLE
        elif event.keyval == Gdk.KEY_Shift_L:
            self.shift_held = True
            self.accounts_list.selection_mode = Gtk.SelectionMode.MULTIPLE

    def keyrelease(self, _, event: Gdk.EventKey):
        # When Ctrl or Shift is released, don't set accounts_list's selection mode
        # back to SINGLE just yet. This is because Gtk will deselect all the rows.
        if event.keyval == Gdk.KEY_Control_L:
            self.ctrl_held = False
        elif event.keyval == Gdk.KEY_Shift_L:
            self.shift_held = False

    def on_account_right_click(self, _, event: Gdk.EventButton):
        if event.button == Gdk.BUTTON_SECONDARY and event.type == Gdk.EventType.BUTTON_PRESS:
            menu = Gtk.Menu()

            funcs = (self.cut_accounts, self.copy_accounts, self.paste_accounts)
            names = ("Cut", "Copy", "Paste")
            for name, func in zip(names, funcs):
                icon = load_icon(f"gtk-{name.lower()}", 25)
                menu_item = Gtk.ImageMenuItem.new_with_label(name)
                menu_item.image = icon
                menu_item.connect("activate", func)
                menu.add(menu_item)

                if (name in ("Cut", "Copy") and not self.selected_accounts) or \
                   (name == "Paste" and not self.main_window.account_clipboard):
                    menu_item.sensitive = False

            menu.attach_to_widget(self.accounts_list, None)
            menu.show_all()
            menu.popup(None, None, None, None, event.button, event.time)

    @property
    def selected_accounts(self):
        return [item_name(row) for row in self.accounts_list.selected_rows]

    def cut_accounts(self, _=None):
        self.main_window.account_clipboard = AccountClipboard(
            self, self.selected_accounts, True
        )
        self.statusbar.success(SUCCESS_CUTTING_ACCOUNTS)

    def copy_accounts(self, _=None):
        self.main_window.account_clipboard = \
            AccountClipboard(self, self.selected_accounts)
        self.statusbar.success(SUCCESS_COPYING_ACCOUNTS)

    def paste_accounts(self, _=None):
        clipboard = self.main_window.account_clipboard
        if clipboard.db_window == self:
            self.main_window.account_clipboard = None
            return

        for name in clipboard.account_names:
            if name in self.database.accounts:
                response = WarningDialog(CONFIRM_ACCOUNT_REPLACE.format(name)).run()
                if response == Gtk.ResponseType.YES:
                    self.delete_account(name)
                else:
                    continue

            account = clipboard.db_window.database.accounts[name]
            CreateAccount.create_account(account, self)
            if clipboard.is_cut:
                clipboard.db_window.delete_account(name)

        # close all forms since they can display outdated info
        self.form_box.foreach(self.form_box.remove)
        other_box = clipboard.db_window.form_box
        other_box.foreach(other_box.remove)

        self.check_db_saved()
        clipboard.db_window.check_db_saved()
        self.main_window.account_clipboard = None

    def on_account_motion(self, event_box: Gtk.EventBox, _):
        """ When Shift is held, select accounts hovered over by mouse. """
        if self.shift_held:
            self.accounts_list.select_row(event_box.parent)

    def on_select_all(self, *args):
        self.accounts_list.select_all()

    def check_db_saved(self):
        """ Adds * to database window title if the database isn't saved. """
        prefix = '' if self.database.saved else '*'
        self.title = f"{prefix}{self.database.name}"

    def load_accounts(self):
        """
        Populates accounts_list with items.
        """

        self.accounts_list.sort_func = abc_list_sort
        for account_name in self.database.accounts:
            icon = self.load_account_icon(account_name)
            item = add_list_item(self.accounts_list, icon.pixbuf, account_name)
            item.add_events(Gdk.EventMask.POINTER_MOTION_MASK)
            item.connect("motion-notify-event", self.on_account_motion)

    def load_account_icon(self, accountname: str):
        """
        Returns account icon associated with given [accountname].
        """

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size("img/account_icons/account.svg", 50, 50)
        icon = Gtk.Image.new_from_pixbuf(pixbuf)
        for icon_name in self.account_icons:
            if icon_name in accountname.lower():
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    f"{ACCOUNT_ICONS_DIR}/{icon_name}.svg", 50, 50, True
                )
                return Gtk.Image.new_from_pixbuf(pixbuf)
        return icon

    def on_save(self, *args):
        """
        Saves database to disk.
        On success displays success message in statusbar, on error – error message.
        """

        try:
            self.database.dba_file.unlink(missing_ok=True)
            self.database.create()
            self.statusbar.success(SUCCESS_DB_SAVED)
            self.check_db_saved()
        except Exception as err:
            logging.error(traceback.format_exc())
            ErrorDialog(ERROR_DB_SAVE, err).run()

    def do_delete_event(self, event):
        """
        Called when user tries to close the window, propagates event to on_quit.
        NOTE: DO NOT move this method to Window superclass, or else it won't work.
        """
        return self.on_quit(event)

    def on_quit(self, _) -> bool:
        """
        Checks if database is saved, if it is – quits, otherwise displays confirmation dialog.
        :returns: True to prevent quiting and False to allow it.
        """

        if self.database.saved:
            response = Gtk.ResponseType.OK
        else:
            dialog = WarningDialog(
                CONFIRM_QUIT,
                buttons=(
                    "_Cancel", Gtk.ResponseType.CANCEL,
                    "Save", Gtk.ResponseType.ACCEPT,
                    "Ok", Gtk.ResponseType.OK,
                ),
            )
            response = dialog.run()

        if response == Gtk.ResponseType.CANCEL:
            return True

        if response == Gtk.ResponseType.ACCEPT:
            self.on_save()

        self.database.close()
        for db in self.main_window.databases:
            if db.name == self.database.name:
                db.close()

        # hide EditDatabase form if the database we're closing
        # is being edited
        if self.main_window.form_box.children:
            form = self.main_window.form_box.children[0]
            if all((
                "EditDatabase" in str(form.__class__),
                form.database.name == self.database.name,
            )):
                form.destroy()

        return False

    def on_account_selected(self, _, row: Gtk.ListBoxRow):
        # when an account is selected and Ctrl is not held,
        # set accounts_list's selection mode to SINGLE
        if not self.ctrl_held:
            self.accounts_list.selection_mode = Gtk.SelectionMode.SINGLE
            # after changing selection mode, all rows are deselected
            # so here we select the row again
            self.accounts_list.select_row(row)

        account = self.database.accounts[item_name(row)]
        self.show_form(DisplayAccount(account, self))

    def on_create_account(self, _=None):
        self.show_form(CreateAccount(self.database, self))

    def on_edit_account(self, _=None):
        """
        Displays edit account form for selected account.
        """

        # show warning in statusbar if there is no account selected
        row = self.accounts_list.selected_row
        if not row:
            self.statusbar.warning(SELECT_ACCOUNT_TO_EDIT)
            return

        account_name = item_name(row)
        account = self.database.accounts[account_name]
        self.show_form(EditAccount(self.database, account, self))

    def on_delete_accounts(self, _=None):
        """
        Displays confirmation dialog asking user
        if he really wants to delete selected accounts.
        """

        # show warning in statusbar if there are no accounts selected
        if not self.selected_accounts:
            self.statusbar.warning(SELECT_ACCOUNTS_TO_DELETE)
            return

        if WarningDialog(CONFIRM_ACCOUNT_DELETION).run() == Gtk.ResponseType.YES:
            for account_name in self.selected_accounts:
                self.delete_account(account_name)
            self.check_db_saved()
            self.form_box.children[0].destroy()

    def delete_account(self, account_name):
        """ Deletes account from the database and accounts_list. """
        del self.database.accounts[account_name]
        delete_list_item(self.accounts_list, account_name)
