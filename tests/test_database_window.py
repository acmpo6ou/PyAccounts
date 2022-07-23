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
from unittest.mock import patch, Mock, PropertyMock

import pytest
from gi.repository import GdkPixbuf, Gtk

import core
from core.create_account import CreateAccount
from core.database_window import DatabaseWindow, SELECT_ACCOUNT_TO_EDIT, CONFIRM_ACCOUNT_DELETION, \
    SELECT_ACCOUNT_TO_DELETE, CONFIRM_QUIT, SUCCESS_DB_SAVED, ERROR_DB_SAVE
from core.display_account import DisplayAccount
from core.edit_account import EditAccount
from core.gtk_utils import load_icon, item_name
from core.widgets import ErrorDialog


@pytest.fixture
def window(databases, main_window):
    db = main_window.databases[2]
    db.open("123")
    return DatabaseWindow(db, main_window)


def test_window_title(window):
    assert window.title == "main"


def test_load_account_icon(window):
    gmail_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        "img/account_icons/gmail.svg", 50, 50, True
    )

    icon = window.load_account_icon("gmail")
    icon2 = window.load_account_icon("gmail2")
    icon3 = window.load_account_icon("_gmail")

    assert icon.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()
    assert icon2.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()
    assert icon3.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()

    # `git` goes before `github` in assets,
    # but `github` should be a more exact match
    github_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        "img/account_icons/github.svg", 50, 50, True
    )
    icon = window.load_account_icon("GitHub")
    assert icon.pixbuf.get_pixels() == github_pixbuf.get_pixels()

    # if the icon wasn't found the default one should be loaded
    default = load_icon("cs-user-accounts", 50).pixbuf
    icon = window.load_account_icon("afjkdsjfjsjkfdjalsjfl")
    assert icon.pixbuf.get_pixels() == default.get_pixels()


def test_load_accounts(window):
    # load_accounts is called by DatabaseWindow constructor
    account_names = [item_name(row) for row in window.accounts_list.children]
    assert account_names == ["gmail", "mega"]


def test_on_create_account(window):
    window.on_create_account()
    form = window.form_box.children[0]
    assert isinstance(form, CreateAccount)


def test_edit_account(window):
    """Edit account button should show edit account form."""

    # select an account
    row = window.accounts_list.children[1]
    window.accounts_list.select_row(row)

    window.on_edit_account()

    form = window.form_box.children[0]
    assert isinstance(form, EditAccount)
    assert form.account == window.main_window.databases[2].accounts["mega"]


def test_edit_account_no_selection(window):
    """Edit account button should display a warning in statusbar
    if there is no account selected."""

    window.on_edit_account()
    assert window.statusbar.label.text == f"✘ {SELECT_ACCOUNT_TO_EDIT}"
    assert not window.form_box.children  # no form should be shown


def test_confirm_account_deletion_dialog_message(window):
    row = window.accounts_list.children[1]
    window.accounts_list.select_row(row)

    with patch.object(core.database_window, "WarningDialog", autospec=True) as mock:
        window.on_delete_account()
        mock.assert_called_with(CONFIRM_ACCOUNT_DELETION.format("mega"))


def test_confirm_account_deletion_Yes(window):
    row = window.accounts_list.children[1]
    window.accounts_list.select_row(row)

    with patch.object(core.database_window, "WarningDialog", autospec=True) as mock:
        mock.return_value.run.return_value = Gtk.ResponseType.YES
        window.on_delete_account()

        # account is removed from accounts lists
        assert "mega" not in window.database.accounts

        for row in window.accounts_list.children:
            assert item_name(row) != "mega"

        # no form should be shown
        assert not window.form_box.children


def test_confirm_account_deletion_No(window):
    row = window.accounts_list.children[1]
    window.accounts_list.select_row(row)

    with patch.object(core.database_window, "WarningDialog", autospec=True) as mock:
        mock.return_value.run.return_value = Gtk.ResponseType.NO
        window.on_delete_account()

        # account shouldn't be removed from accounts lists
        assert "mega" in window.database.accounts

        account_names = [item_name(row) for row in window.accounts_list.children]
        assert "mega" in account_names


def test_delete_account_no_selection(window):
    """Delete account button should display a warning in statusbar
    if there is no account selected."""
    window.on_delete_account()
    assert window.statusbar.label.text == f"✘ {SELECT_ACCOUNT_TO_DELETE}"


@patch("core.database_window.WarningDialog", autospec=True)
def test_quit_database_is_saved(dialog, window):
    # the database is saved, so there shouldn't be any confirmation dialog
    assert not window.do_delete_event(None)


@patch("core.database_window.WarningDialog", autospec=True)
def test_quit_database_is_not_saved_message(dialog: Mock, window):
    # the database is not saved
    del window.database.accounts["mega"]

    window.do_delete_event(None)
    dialog.assert_called_with(CONFIRM_QUIT)


@patch("core.database_window.WarningDialog", autospec=True)
def test_confirm_quit_No(dialog: Mock, window):
    # the database is not saved
    del window.database.accounts["mega"]

    # choose No in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.NO
    assert window.do_delete_event(None)


@patch("core.database_window.WarningDialog", autospec=True)
def test_confirm_quit_Yes(dialog: Mock, window):
    # the database is not saved
    del window.database.accounts["mega"]

    # choose Yes in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.YES
    assert not window.do_delete_event(None)
    assert not window.database.opened


def test_save_database_success(window):
    window.on_save()
    assert window.statusbar.label.text == f"✔ {SUCCESS_DB_SAVED}"


@patch("core.database_window.ErrorDialog", autospec=True)
@patch("core.database_window.Database.dba_file", new_callable=PropertyMock)
def test_save_database_error(mock, dialog: "Mock[ErrorDialog]", window, faker):
    err = Exception(faker.sentence())
    mock.side_effect = err

    window.on_save()
    dialog.assert_called_with(ERROR_DB_SAVE, err)
    assert not window.statusbar.label.text
