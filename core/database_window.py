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
SELECT_ACCOUNT_TO_DELETE = "Please select an account to delete."
CONFIRM_ACCOUNT_DELETION = "Delete <b>{}</b> account?"
CONFIRM_QUIT = (
    "Are you sure you want to close the database?\n" "Any unsaved changes will be lost!"
)
SUCCESS_DB_SAVED = "Database saved successfully!"
ERROR_DB_SAVE = "Error saving the database!"

SUCCESS_CUTTING_ACCOUNTS = "Cut account(s)."
SUCCESS_COPYING_ACCOUNTS = "Copied account(s)."


class DatabaseWindow(Window):
    # <editor-fold>
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
            key=lambda x: len(x),
            reverse=True,
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
        self.add_events(Gdk.EventMask.KEY_PRESS_MASK & Gdk.EventMask.KEY_RELEASE_MASK)
        self.connect("key_press_event", self.keypress)
        self.connect("key_release_event", self.keyrelease)

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
        """ Allow selecting multiple accounts when Ctrl is held. """
        if event.keyval == 65507:  # TODO: replace with const for Ctrl
            self.accounts_list.selection_mode = Gtk.SelectionMode.MULTIPLE
            self.ctrl_held = True

    def keyrelease(self, _, event: Gdk.EventKey):
        """
        When Ctrl is released, don't set accounts_list's selection mode
        back to SINGLE just yet. This is because Gtk will deselect all the rows.
        """
        if event.keyval == 65507:  # TODO: replace with const for Ctrl
            self.ctrl_held = False

    def on_account_right_click(self, _, event: Gdk.EventButton):
        if event.button == Gdk.BUTTON_SECONDARY and event.type == Gdk.EventType.BUTTON_PRESS:
            menu = Gtk.Menu()

            funcs = (self.cut_account, self.copy_account, self.paste_account)
            names = ("Cut", "Copy", "Paste")
            for name, func in zip(names, funcs):
                icon = load_icon(f"gtk-{name.lower()}", 25)
                menu_item = Gtk.ImageMenuItem.new_with_label(name)
                menu_item.image = icon
                menu_item.connect("activate", func)
                menu.add(menu_item)

            menu.attach_to_widget(self.accounts_list, None)
            menu.show_all()
            menu.popup(None, None, None, None, event.button, event.time)

    @property
    def selected_accounts(self):
        return [item_name(row) for row in self.accounts_list.selected_rows]

    def cut_accounts(self, _=None):
        self.main_window.account_clipboard = AccountClipboard(
            db_window=self, account_names=self.selected_accounts, is_cut=True
        )
        self.statusbar.success(SUCCESS_CUTTING_ACCOUNTS)

    def copy_accounts(self, _=None):
        # TODO: set main_window.accounts_clipboard with appropriate data
        #  show Statusbar message
        print("copy")

    def paste_accounts(self, _=None):
        # TODO: if account clipboard db is equal to current db
        #  set account clipboard to None
        # TODO: if account clipboard is None, return
        # TODO: for each copied account name:
        #  check if it's in current db:
        #    if yes -> show a confirmation dialog with Yes, No
        #       Yes:
        #          delete the account in current db (and from list also)
        #          proceed to else
        #    else:
        #       create account in current db (use CreateAccount.create_account)
        #       delete account in clipboard db (also updating the list)
        #           call delete_account() on the db window
        #  clear account clipboard
        print("paste")

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
            add_list_item(self.accounts_list, icon.pixbuf, account_name)

    def load_account_icon(self, accountname: str):
        """
        Returns account icon associated with given [accountname].
        """

        icon = load_icon("cs-user-accounts", 50)
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

    def on_delete_account(self, _=None):
        """
        Displays confirmation dialog asking user if he really wants to delete selected account.
        """

        # show warning in statusbar if there is no account selected
        row = self.accounts_list.selected_row
        if not row:
            self.statusbar.warning(SELECT_ACCOUNT_TO_DELETE)
            return

        account_name = item_name(row)
        message = CONFIRM_ACCOUNT_DELETION.format(account_name)
        response = WarningDialog(message).run()

        if response == Gtk.ResponseType.YES:
            self.delete_account(account_name)
            self.check_db_saved()
            self.form_box.children[0].destroy()

    def delete_account(self, account_name):
        """ Deletes account from the database and accounts_list. """
        del self.database.accounts[account_name]
        delete_list_item(self.accounts_list, account_name)
