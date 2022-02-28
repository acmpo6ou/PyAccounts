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
import shutil
from unittest.mock import Mock, patch

import pytest
from gi.repository import Gtk, GdkPixbuf

import core
from core.create_database import CreateDatabase
from core.database_utils import Database
from core.edit_database import EditDatabase
from core.main_window import (
    MainWindow,
    SELECT_DB_TO_EDIT,
    SELECT_DB_TO_DELETE,
    CONFIRM_DB_DELETION,
    SUCCESS_DB_DELETED,
)
from core.open_database import OpenDatabase
from core.rename_database import RenameDatabase
from core.widgets import StatusBar


@pytest.fixture
def databases(src_dir):
    shutil.copy("tests/data/main.dba", src_dir)
    shutil.copy("tests/data/main.dba", src_dir / "crypt.dba")
    shutil.copy("tests/data/main.dba", src_dir / "data.dba")


@pytest.fixture
def main_window():
    return MainWindow()


def test_get_databases(databases, main_window):
    # get_databases is called by MainWindow constructor

    expected_dbs = [Database("crypt"), Database("data"), Database("main")]
    assert main_window.databases == expected_dbs


def test_load_databases(databases, main_window):
    # load_databases is called by MainWindow constructor

    # get icons and labels of elements in the database list
    icons = []
    labels = []

    for row in main_window.db_list.children:
        hbox: Gtk.HBox = row.children[0]
        icons.append(hbox.children[0])
        labels.append(hbox.children[1])

    # all icons should be PyAccounts app icons
    expected_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale("img/icon.svg", 50, 50, True)
    for icon in icons:
        assert icon.pixbuf.get_pixels() == expected_pixbuf.get_pixels()
    assert len(icons) == 3

    # all labels should contain appropriate databases names
    db_names = [label.text for label in labels]
    assert db_names == ["crypt", "data", "main"]


def test_on_create_database(main_window):
    main_window.on_create_database(None)
    form = main_window.form_box.children[0]
    assert isinstance(form, CreateDatabase)


def test_select_closed_database(databases, main_window):
    """When selecting a database, the open database form should be displayed
    if the database is closed."""

    # select a database
    row = main_window.db_list.children[2]
    main_window.db_list.select_row(row)

    form = main_window.form_box.children[0]
    assert isinstance(form, OpenDatabase)
    assert form.database == main_window.databases[2]


def test_select_opened_database(databases, main_window):
    """When selecting an opened database, the open database form shouldn't be displayed."""

    # make a database opened
    main_window.databases[2].password = "123"

    # select it
    row = main_window.db_list.children[2]
    main_window.db_list.select_row(row)

    assert not main_window.form_box.children


def test_edit_closed_database(databases, main_window):
    """Edit database button should display
    rename database form if selected database is closed."""

    # select a database
    row = main_window.db_list.children[1]
    main_window.db_list.select_row(row)

    main_window.on_edit_database(None)

    form = main_window.form_box.children[0]
    assert isinstance(form, RenameDatabase)
    assert form.database == main_window.databases[1]


def test_edit_opened_database(databases, main_window):
    """Edit database button should display
    edit database form if selected database is opened."""

    # make a database opened
    main_window.databases[1].password = "123"

    # select it
    row = main_window.db_list.children[1]
    main_window.db_list.select_row(row)

    main_window.on_edit_database(None)

    form = main_window.form_box.children[0]
    assert isinstance(form, EditDatabase)
    assert form.database == main_window.databases[1]


def test_edit_database_no_selection(databases, main_window):
    """Edit database button should display a warning in statusbar
    if there is no database selected."""

    statusbar = Mock(StatusBar)
    main_window.statusbar = statusbar
    main_window.on_edit_database(None)

    statusbar.warning.assert_called_with(SELECT_DB_TO_EDIT)
    assert not main_window.form_box.children  # no form should be shown


def test_confirm_database_deletion_dialog_message(databases, main_window):
    # select a database
    row = main_window.db_list.children[1]
    main_window.db_list.select_row(row)

    with patch.object(core.main_window, "WarningDialog", autospec=True) as mock:
        # press on delete database button
        main_window.on_delete_database(None)

        # the confirmation dialog should have been displayed with the correct message
        db_name = main_window.databases[1].name
        mock.assert_called_with(CONFIRM_DB_DELETION.format(db_name))


def test_confirm_database_deletion_Yes(databases, main_window):
    # select a database
    row = main_window.db_list.children[1]
    main_window.db_list.select_row(row)

    main_window.delete_database = Mock()
    with patch.object(core.main_window, "WarningDialog", autospec=True) as mock:
        # press on delete database button, and choose Yes in confirmation dialog
        mock.return_value.run.return_value = Gtk.ResponseType.YES
        main_window.on_delete_database(None)

        # the delete_database should have been called
        db = main_window.databases[1]
        main_window.delete_database.assert_called_with(db)


def test_confirm_database_deletion_No(databases, main_window):
    # select a database
    row = main_window.db_list.children[1]
    main_window.db_list.select_row(row)

    main_window.delete_database = Mock()
    with patch.object(core.main_window, "WarningDialog", autospec=True) as mock:
        # press on delete database button, and choose No in confirmation dialog
        mock.return_value.run.return_value = Gtk.ResponseType.NO
        main_window.on_delete_database(None)

        # the MainWindow's delete_database shouldn't have been called
        main_window.delete_database.assert_not_called()


def test_delete_database_no_selection(databases, main_window):
    """Delete database button should display a warning in statusbar
    if there is no database selected."""

    statusbar = Mock(StatusBar)
    main_window.statusbar = statusbar

    main_window.on_delete_database(None)
    statusbar.warning.assert_called_with(SELECT_DB_TO_DELETE)


def test_delete_database_success(databases, main_window):
    main_db = main_window.databases[2]
    main_window.form_box.add(OpenDatabase(main_db))
    main_window.delete_database(main_db)

    # a success message should be shown in statusbar
    assert SUCCESS_DB_DELETED in main_window.statusbar.label.text

    # the database should be removed from databases list
    assert Database("main") not in main_window.databases

    # and from db_list as well
    for row in main_window.db_list.children:
        label = row.children[0].children[-1]
        assert label.text != "main"

    # its .dba file should be deleted
    assert not main_db.dba_file.exists()

    # no form should be shown
    assert not main_window.form_box.children
