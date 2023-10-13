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
from unittest.mock import patch, Mock, PropertyMock, ANY

import pytest
from gi.repository import GdkPixbuf, Gtk

import core
from core.create_account import CreateAccount
from core.database_utils import Database
from core.database_window import DatabaseWindow, SELECT_ACCOUNT_TO_EDIT, CONFIRM_ACCOUNT_DELETION, \
    SELECT_ACCOUNTS_TO_DELETE, CONFIRM_QUIT, SUCCESS_DB_SAVED, ERROR_DB_SAVE, \
    SUCCESS_CUTTING_ACCOUNTS, SUCCESS_COPYING_ACCOUNTS, CONFIRM_ACCOUNT_REPLACE
from core.display_account import DisplayAccount
from core.edit_account import EditAccount
from core.edit_database import EditDatabase
from core.gtk_utils import load_icon, item_name, items_names
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
    default = GdkPixbuf.Pixbuf.new_from_file_at_size("img/account_icons/account.svg", 50, 50)
    icon = db_window.load_account_icon("afjkdsjfjsjkfdjalsjfl")
    assert icon.pixbuf.get_pixels() == default.get_pixels()


def test_load_accounts(db_window):
    # load_accounts is called by DatabaseWindow constructor
    account_names = items_names(db_window.accounts_list)
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
        db_window.on_delete_accounts()
        mock.assert_called_with(CONFIRM_ACCOUNT_DELETION.format("mega"))


def test_confirm_account_deletion_Yes(db_window):
    row = db_window.accounts_list.children[0]
    row.activate()

    db_window.accounts_list.selection_mode = Gtk.SelectionMode.MULTIPLE
    db_window.accounts_list.select_all()

    with patch.object(core.database_window, "WarningDialog", autospec=True) as mock:
        mock.return_value.run.return_value = Gtk.ResponseType.YES
        db_window.on_delete_accounts()

        # accounts are removed from accounts lists
        assert not db_window.database.accounts
        assert not items_names(db_window.accounts_list)

        # no form should be shown
        assert not db_window.form_box.children


def test_confirm_account_deletion_No(db_window):
    row = db_window.accounts_list.children[0]
    db_window.accounts_list.select_row(row)

    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    with patch.object(core.database_window, "WarningDialog", autospec=True) as mock:
        mock.return_value.run.return_value = Gtk.ResponseType.NO
        db_window.on_delete_accounts()

        # account shouldn't be removed from accounts lists
        assert "mega" in db_window.database.accounts
        assert "gmail" in db_window.database.accounts

        account_names = items_names(db_window.accounts_list)
        assert "mega" in account_names
        assert "gmail" in account_names


def test_delete_account_no_selection(db_window):
    """Delete account button should display a warning in statusbar
    if there is no account selected."""
    db_window.on_delete_accounts()
    assert db_window.statusbar.label.text == f"✘ {SELECT_ACCOUNTS_TO_DELETE}"


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


def test_check_db_saved(db_window):
    assert db_window.title == "main"

    del db_window.database.accounts["gmail"]
    db_window.check_db_saved()
    assert db_window.title == "*main"

    db_window.on_save()
    assert db_window.title == "main"


def test_cut_accounts(db_window):
    # select an account
    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    db_window.cut_accounts()

    clipboard = db_window.main_window.account_clipboard
    assert clipboard.db_window == db_window
    assert clipboard.account_names == ["mega"]
    assert clipboard.is_cut
    assert db_window.statusbar.label.text == f"✔ {SUCCESS_CUTTING_ACCOUNTS}"


def test_copy_accounts(db_window):
    # select an account
    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    db_window.copy_accounts()

    clipboard = db_window.main_window.account_clipboard
    assert clipboard.db_window == db_window
    assert clipboard.account_names == ["mega"]
    assert not clipboard.is_cut
    assert db_window.statusbar.label.text == f"✔ {SUCCESS_COPYING_ACCOUNTS}"


@pytest.fixture
def db_window2(db_window):
    db = Database("test", "123")
    return DatabaseWindow(db, db_window.main_window)


def test_close_all_forms_when_pasting(account, db_window):
    db = Database("test", "123", {"gmail": account})
    db_window2 = DatabaseWindow(db, db_window.main_window)

    # select an account in db_window2 to open a form
    row = db_window.accounts_list.children[0]
    row.activate()

    # select an account for cutting in db_window
    row = db_window.accounts_list.children[1]
    row.activate()

    db_window.cut_accounts()

    # select another account in db_window to open a form
    row = db_window.accounts_list.children[0]
    row.activate()

    db_window2.paste_accounts()

    # no form should be shown in both windows
    assert not db_window.form_box.children
    assert not db_window2.form_box.children


def test_cut_and_paste_accounts(db_window, db_window2):
    # select an account
    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    db_window.cut_accounts()
    db_window2.paste_accounts()

    assert "mega" not in db_window.database.accounts
    assert "mega" in db_window2.database.accounts

    assert "mega" not in items_names(db_window.accounts_list)
    assert "mega" in items_names(db_window2.accounts_list)

    assert not db_window.main_window.account_clipboard
    assert "*" in db_window.title
    assert "*" in db_window2.title


def test_copy_and_paste_accounts(db_window, db_window2):
    # select an account
    row = db_window.accounts_list.children[1]
    db_window.accounts_list.select_row(row)

    db_window.copy_accounts()
    db_window2.paste_accounts()

    assert "mega" in db_window.database.accounts
    assert "mega" in db_window2.database.accounts

    assert "mega" in items_names(db_window.accounts_list)
    assert "mega" in items_names(db_window2.accounts_list)

    assert not db_window.main_window.account_clipboard
    assert "*" not in db_window.title
    assert "*" in db_window2.title


@patch("core.database_window.WarningDialog", autospec=True)
def test_paste_existing_account(dialog: Mock, db_window):
    # `mega` doesn't exist, but `gmail` does
    db = db_window.main_window.databases[1]
    db.open("123")
    db_window2 = DatabaseWindow(db, db_window.main_window)
    db_window2.delete_account("mega")
    db_window2.database.accounts["gmail"].email = "test@gmail.com"

    # move accounts choosing No in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.NO
    db_window.accounts_list.selection_mode = Gtk.SelectionMode.MULTIPLE
    db_window.accounts_list.select_all()
    db_window.cut_accounts()
    db_window2.paste_accounts()

    # there was a confirmation dialog shown about `gmail`
    dialog.assert_called_with(CONFIRM_ACCOUNT_REPLACE.format("gmail"))

    # `mega` is moved to db_window2
    assert "mega" not in db_window.database.accounts
    assert "mega" in db_window2.database.accounts
    assert "mega" not in items_names(db_window.accounts_list)
    assert "mega" in items_names(db_window2.accounts_list)

    # but `gmail` isn't
    assert "gmail" in db_window.database.accounts
    assert "gmail" in db_window2.database.accounts
    assert "gmail" in items_names(db_window.accounts_list)
    assert "gmail" in items_names(db_window2.accounts_list)
    assert db_window2.database.accounts["gmail"].email == "test@gmail.com"

    # try to move gmail from db_window to db_window2 again,
    # choosing Yes this time
    dialog.return_value.run.return_value = Gtk.ResponseType.YES
    db_window.accounts_list.select_all()
    db_window.cut_accounts()
    db_window2.paste_accounts()

    assert not items_names(db_window.accounts_list)
    assert not db_window.database.accounts

    # gmail should have been replaced
    assert items_names(db_window2.accounts_list) == ["gmail", "mega"]
    assert sorted(db_window2.database.accounts.keys()) == ["gmail", "mega"]
    assert db_window2.database.accounts["gmail"].email == "example@gmail.com"
