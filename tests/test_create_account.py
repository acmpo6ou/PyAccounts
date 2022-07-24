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
from unittest.mock import Mock, patch

import pytest
from gi.repository import Gtk

from core.create_account import CreateAccount, CONFIRM_ATTACH_EXISTING_FILE
from core.gtk_utils import item_name
from core.widgets import DateChooserDialog


@pytest.fixture
def form(databases, main_window):
    db = main_window.databases[2]
    db.open("123")
    return CreateAccount(db)


def test_date_chooser_dialog_default_date():
    dialog = DateChooserDialog("05.11.2000")
    year, month, day = dialog.calendar.date
    assert (year, month, day) == (2000, 10, 5)


@patch("core.create_account.WarningDialog", autospec=True)
def test_attach_file(dialog: Mock, form):
    form.attach_file("tests/data/main.dba")
    assert form.attached_paths["main.dba"] == "tests/data/main.dba"
    dialog.assert_not_called()

    attached_files = [item_name(row) for row in form.attached_files.children]
    assert attached_files == ["main.dba"]


@patch("core.create_account.WarningDialog", autospec=True)
def test_attach_file_confirmation_dialog_message(dialog: Mock, src_dir, form):
    # main.dba is already attached
    form.attach_file("tests/data/main.dba")

    # if we try to attach a file with the same name,
    # there should be a confirmation dialog
    form.attach_file(f"{src_dir}/main.dba")
    dialog.assert_called_with(CONFIRM_ATTACH_EXISTING_FILE.format("main.dba"))


@patch("core.create_account.WarningDialog", autospec=True)
def test_attach_same_file(dialog: Mock, src_dir, form):
    # main.dba is already attached
    form.attach_file("tests/data/main.dba")

    # if we try to attach it again,
    # there SHOULDN'T be a confirmation dialog shown
    form.attach_file("tests/data/main.dba")
    dialog.assert_not_called()

    # and there shouldn't be a duplicate file attached
    attached_files = [item_name(row) for row in form.attached_files.children]
    assert attached_files == ["main.dba"]


@patch("core.create_account.WarningDialog", autospec=True)
def test_attach_file_confirmation_dialog_No(dialog: Mock, src_dir, form):
    # main.dba is already attached
    form.attach_file("tests/data/main.dba")

    # choose No in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.NO
    form.attach_file(f"{src_dir}/main.dba")

    # the attached file path should be unchanged
    assert form.attached_paths["main.dba"] == "tests/data/main.dba"

    # and there shouldn't be a duplicate file attached
    attached_files = [item_name(row) for row in form.attached_files.children]
    assert attached_files == ["main.dba"]


@patch("core.create_account.WarningDialog", autospec=True)
def test_attach_file_confirmation_dialog_Yes(dialog: Mock, src_dir, form):
    # main.dba is already attached
    form.attach_file("tests/data/main.dba")

    # choose No in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.YES
    form.attach_file(f"{src_dir}/main.dba")

    # the attached file path should have been replaced
    assert form.attached_paths["main.dba"] == f"{src_dir}/main.dba"

    # but there shouldn't be a duplicate file attached
    attached_files = [item_name(row) for row in form.attached_files.children]
    assert attached_files == ["main.dba"]
