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

from core.create_account import CreateAccount, CONFIRM_ATTACH_EXISTING_FILE, SELECT_FILES_TO_DETACH, \
    CONFIRM_FILES_DETACH
from core.gtk_utils import item_name
from core.widgets import DateChooserDialog, WarningDialog


@pytest.fixture
def form(db_window):
    return CreateAccount(db_window.database, db_window)


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


def test_detach_file_no_file_selected(form):
    form.on_detach_file()
    assert form.database_window.statusbar.label.text == f"✘ {SELECT_FILES_TO_DETACH}"


@patch("core.create_account.WarningDialog", autospec=True)
def test_detach_file_confirmation_dialog_message(dialog: Mock, form):
    form.attach_file("tests/data/main.dba")
    row = form.attached_files.children[0]
    form.attached_files.select_row(row)

    WarningDialog.run = lambda *args: None
    form.on_detach_file()
    dialog.assert_called_with(CONFIRM_FILES_DETACH)
    assert not form.database_window.statusbar.label.text


@patch("core.create_account.WarningDialog", autospec=True)
def test_detach_file_Yes(dialog: Mock, form):
    form.attach_file("tests/data/main.dba")
    form.attach_file("PyAccounts.py")
    form.attached_files.select_all()

    dialog.return_value.run.return_value = Gtk.ResponseType.YES
    form.on_detach_file()

    assert not form.attached_paths
    attached_files = [item_name(row) for row in form.attached_files.children]
    assert not attached_files


@patch("core.create_account.WarningDialog", autospec=True)
def test_detach_file_No(dialog: Mock, form):
    form.attach_file("tests/data/main.dba")
    form.attach_file("PyAccounts.py")
    form.attached_files.select_all()

    dialog.return_value.run.return_value = Gtk.ResponseType.NO
    form.on_detach_file()

    assert "main.dba" in form.attached_paths
    assert "PyAccounts.py" in form.attached_paths
    attached_files = [item_name(row) for row in form.attached_files.children]
    assert attached_files == ["main.dba", "PyAccounts.py"]


def test_drop_files(form):
    data = Mock()
    data.get_uris = lambda *args: (
        "file://tests/data/main.dba",
        "file:///home/",
        "file://PyAccounts.py",
    )

    form.on_drop_files(None, None, 0, 0, data, None, None)
    # file:// should be removed, and all folders should be skipped
    assert form.attached_paths["main.dba"] == "tests/data/main.dba"
    assert form.attached_paths["PyAccounts.py"] == "PyAccounts.py"
    assert len(form.attached_paths) == 2
