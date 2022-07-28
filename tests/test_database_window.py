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
from unittest.mock import patch, Mock, PropertyMock, ANY

from gi.repository import GdkPixbuf, Gtk

import core
from core.create_account import CreateAccount
from core.database_window import DatabaseWindow, SELECT_ACCOUNT_TO_EDIT, CONFIRM_ACCOUNT_DELETION, \
    SELECT_ACCOUNT_TO_DELETE, CONFIRM_QUIT, SUCCESS_DB_SAVED, ERROR_DB_SAVE
from core.display_account import DisplayAccount
from core.edit_account import EditAccount
from core.edit_database import EditDatabase
from core.gtk_utils import load_icon, item_name
from core.widgets import ErrorDialog


def test_window_title(db_window):
    assert db_window.title == "main"


def test_load_account_icon(db_window):
    gmail_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        "img/account_icons/gmail.svg", 50, 50, True
    )

    icon = db_window.load_account_icon("gmail")
    icon2 = db_window.load_account_icon("gmail2")
    icon3 = db_window.load_account_icon("_gmail")

    assert icon.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()
    assert icon2.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()
    assert icon3.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()

    # `git` goes before `github` in assets,
    # but `github` should be a more exact match
    github_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        "img/account_icons/github.svg", 50, 50, True
    )
    icon = db_window.load_account_icon("GitHub")
    assert icon.pixbuf.get_pixels() == github_pixbuf.get_pixels()

    # if the icon wasn't found the default one should be loaded
    default = load_icon("cs-user-accounts", 50).pixbuf
    icon = db_window.load_account_icon("afjkdsjfjsjkfdjalsjfl")
    assert icon.pixbuf.get_pixels() == default.get_pixels()


def test_load_accounts(db_window):
    # load_accounts is called by DatabaseWindow constructor
    account_names = [item_name(row) for row in db_window.accounts_list.children]
    assert account_names == ["gmail", "mega"]


def test_select_account(db_window):
    # select an account
    row = db_window.accounts_list.children[0]
    row.activate()

    form = db_window.form_box.children[0]
    assert isinstance(form, DisplayAccount)
    assert form.account == db_window.database.accounts["gmail"]


def test_on_create_account(db_window):
    db_window.on_create_account()
    form = db_window.form_box.children[0]
    assert isinstance(form, CreateAccount)


def test_edit_account(db_window):
    """Edit account button should show edit account form."""

    # select an account
    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    db_window.on_edit_account()

    form = db_window.form_box.children[0]
    assert isinstance(form, EditAccount)
    assert form.account == db_window.main_window.databases[2].accounts["mega"]


def test_edit_account_no_selection(db_window):
    """Edit account button should display a warning in statusbar
    if there is no account selected."""

    db_window.on_edit_account()
    assert db_window.statusbar.label.text == f"✘ {SELECT_ACCOUNT_TO_EDIT}"
    assert not db_window.form_box.children  # no form should be shown


def test_confirm_account_deletion_dialog_message(db_window):
    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    with patch.object(core.database_window, "WarningDialog", autospec=True) as mock:
        db_window.on_delete_account()
        mock.assert_called_with(CONFIRM_ACCOUNT_DELETION.format("mega"))


def test_confirm_account_deletion_Yes(db_window):
    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    with patch.object(core.database_window, "WarningDialog", autospec=True) as mock:
        mock.return_value.run.return_value = Gtk.ResponseType.YES
        db_window.on_delete_account()

        # account is removed from accounts lists
        assert "mega" not in db_window.database.accounts

        for row in db_window.accounts_list.children:
            assert item_name(row) != "mega"

        # no form should be shown
        assert not db_window.form_box.children


def test_confirm_account_deletion_No(db_window):
    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    with patch.object(core.database_window, "WarningDialog", autospec=True) as mock:
        mock.return_value.run.return_value = Gtk.ResponseType.NO
        db_window.on_delete_account()

        # account shouldn't be removed from accounts lists
        assert "mega" in db_window.database.accounts

        account_names = [item_name(row) for row in db_window.accounts_list.children]
        assert "mega" in account_names


def test_delete_account_no_selection(db_window):
    """Delete account button should display a warning in statusbar
    if there is no account selected."""
    db_window.on_delete_account()
    assert db_window.statusbar.label.text == f"✘ {SELECT_ACCOUNT_TO_DELETE}"


@patch("core.database_window.WarningDialog", autospec=True)
def test_quit_database_is_saved(dialog, db_window):
    # the database is saved, so there shouldn't be any confirmation dialog
    assert not db_window.do_delete_event(None)


@patch("core.database_window.WarningDialog", autospec=True)
def test_quit_database_is_not_saved_message(dialog: Mock, db_window):
    # the database is not saved
    del db_window.database.accounts["mega"]

    db_window.do_delete_event(None)
    dialog.assert_called_with(CONFIRM_QUIT, buttons=ANY)


@patch("core.database_window.WarningDialog", autospec=True)
def test_confirm_quit_Cancel(dialog: Mock, db_window):
    # the database is not saved
    del db_window.database.accounts["mega"]

    # choose Cancel in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.CANCEL
    assert db_window.do_delete_event(None)


@patch("core.database_window.WarningDialog", autospec=True)
def test_confirm_quit_Ok(dialog: Mock, db_window):
    # the database is not saved
    del db_window.database.accounts["mega"]

    # choose Ok in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.OK
    assert not db_window.do_delete_event(None)
    assert not db_window.database.opened


def test_hide_edit_db_form_when_its_window_closes(db_window):
    window = db_window.main_window
    form = EditDatabase(db_window.database, window)
    window.show_form(form)

    db_window.do_delete_event(None)
    assert not window.form_box.children


def test_save_database_success(db_window):
    db_window.on_save()
    assert db_window.statusbar.label.text == f"✔ {SUCCESS_DB_SAVED}"


@patch("core.database_window.ErrorDialog", autospec=True)
@patch("core.database_window.Database.dba_file", new_callable=PropertyMock)
def test_save_database_error(mock, dialog: "Mock[ErrorDialog]", db_window, faker):
    err = Exception(faker.sentence())
    mock.side_effect = err

    db_window.on_save()
    dialog.assert_called_with(ERROR_DB_SAVE, err)
    assert not db_window.statusbar.label.text
