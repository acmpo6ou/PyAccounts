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
from pathlib import Path
from unittest.mock import Mock, patch, PropertyMock

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
    ERROR_DB_DELETION,
    CONFIRM_QUIT,
    SUCCESS_DB_IMPORT,
    WARNING_DB_EXISTS,
    WARNING_DB_CORRUPTED,
    ERROR_DB_IMPORT,
    SELECT_DB_TO_EXPORT,
    SUCCESS_DB_EXPORT,
    ERROR_DB_EXPORT,
)
from core.open_database import OpenDatabase
from core.rename_database import RenameDatabase
from core.widgets import ErrorDialog, IconDialog


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

    main_window.on_edit_database(None)
    assert main_window.statusbar.label.text == f"✘ {SELECT_DB_TO_EDIT}"
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
    main_window.on_delete_database(None)
    assert main_window.statusbar.label.text == f"✘ {SELECT_DB_TO_DELETE}"


def test_delete_database_success(databases, main_window):
    main_db = main_window.databases[2]
    main_window.form_box.add(OpenDatabase(main_db))
    main_window.delete_database(main_db)

    # a success message should be shown in statusbar
    assert main_window.statusbar.label.text == f"✔ {SUCCESS_DB_DELETED}"

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


@patch("core.main_window.ErrorDialog", autospec=True)
@patch("core.main_window.Database.dba_file", new_callable=PropertyMock)
def test_delete_database_error(
    mock, dialog: "Mock[ErrorDialog]", databases, main_window, faker
):
    err = Exception(faker.sentence())
    mock.return_value.unlink.side_effect = err
    main_db = Database("main")

    # the ErrorDialog should be shown
    main_window.delete_database(main_db)
    dialog.assert_called_with(ERROR_DB_DELETION, err)

    # the database shouldn't be deleted from databases list
    assert Database("main") in main_window.databases

    # and from db_list
    db_list_names = []
    for row in main_window.db_list.children:
        label = row.children[0].children[-1]
        db_list_names.append(label.text)
    assert "main" in db_list_names

    # there shouldn't be any message shown in statusbar
    assert not main_window.statusbar.label.text


def test_quit_all_databases_are_closed(databases, main_window):
    # all databases are closed by default, so there shouldn't be any confirmation dialog
    assert not main_window.do_delete_event(None)


@patch("core.main_window.WarningDialog", autospec=True)
def test_quit_a_database_is_opened(dialog: Mock, databases, main_window):
    # there is an opened database
    main_window.databases[0].password = "123"

    main_window.do_delete_event(None)
    dialog.assert_called_with(CONFIRM_QUIT)


@patch("core.main_window.WarningDialog", autospec=True)
def test_confirm_quit_No(dialog: Mock, databases, main_window):
    # there is an opened database
    main_window.databases[0].password = "123"

    # choose No in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.NO
    assert main_window.do_delete_event(None)


@patch("core.main_window.WarningDialog", autospec=True)
def test_confirm_quit_Yes(dialog: Mock, databases, main_window):
    # there is an opened database
    main_window.databases[0].password = "123"

    # choose Yes in the confirmation dialog
    dialog.return_value.run.return_value = Gtk.ResponseType.YES
    assert not main_window.do_delete_event(None)


def test_select_main_database(databases, main_window):
    # turn on the main database feature
    main_window.config.main_db = True

    main_window.select_main_database()

    # the main database should be selected
    row = main_window.db_list.selected_row
    index = main_window.db_list.children.index(row)
    selected_db = main_window.databases[index]
    assert selected_db == Database("main")


@patch("gi.repository.Gtk.FileChooserDialog", autospec=True)
def test_import_dialog_Cancel(mock: "Mock[Gtk.FileChooserDialog]", main_window):
    # choose Cancel in the dialog
    mock.return_value.run.return_value = Gtk.ResponseType.CANCEL
    main_window.import_database = Mock()

    main_window.on_import_database()
    main_window.import_database.assert_not_called()


@patch("gi.repository.Gtk.FileChooserDialog", autospec=True)
def test_import_dialog_Import(mock: "Mock[Gtk.FileChooserDialog]", main_window, faker):
    # choose a file to import
    filename = faker.file_name()
    mock.return_value.filename = filename

    mock.return_value.run.return_value = Gtk.ResponseType.ACCEPT
    main_window.import_database = Mock()

    main_window.on_import_database()
    main_window.import_database.assert_called_with(filename)


@patch("core.main_window.IconDialog", autospec=True)
def test_import_database_success(dialog: Mock, src_dir, main_window):
    main_window.import_database("tests/data/main.dba")

    assert Path(src_dir / "main.dba").exists()
    assert Database("main") in main_window.databases

    # the database should appear in db_list
    db_list_names = []
    for row in main_window.db_list.children:
        label = row.children[0].children[-1]
        db_list_names.append(label.text)
    assert "main" in db_list_names

    # a success message should be shown in statusbar
    assert main_window.statusbar.label.text == f"✔ {SUCCESS_DB_IMPORT}"

    # there shouldn't be any dialogs shown
    dialog.assert_not_called()


@patch("core.main_window.IconDialog", autospec=True)
def test_import_database_already_exists(dialog: Mock, src_dir, main_window):
    IconDialog.run = lambda _: None
    shutil.copy("tests/data/main.dba", src_dir)
    main_window.import_database("tests/data/main.dba")

    dialog.assert_called_with("Warning!", WARNING_DB_EXISTS, "dialog-warning")
    dialog.return_value.run.assert_called()

    # the statusbar should be empty
    assert not main_window.statusbar.label.text


@patch("core.main_window.IconDialog", autospec=True)
def test_import_corrupted_database(dialog: Mock, src_dir, main_window):
    IconDialog.run = lambda _: None
    main_window.import_database("tests/data/corrupted.dba")

    dialog.assert_called_with("Warning!", WARNING_DB_CORRUPTED, "dialog-warning")
    dialog.return_value.run.assert_called()

    assert not Path(src_dir / "corrupted.dba").exists()
    assert Database("corrupted") not in main_window.databases

    # the database shouldn't be in db_list
    for row in main_window.db_list.children:
        label = row.children[0].children[-1]
        assert "corrupted" != label.text

    # the statusbar should be empty
    assert not main_window.statusbar.label.text


@patch("shutil.copy", autospec=True)
@patch("core.main_window.ErrorDialog", autospec=True)
def test_import_database_error(dialog: Mock, mock_copy: Mock, src_dir, main_window, faker):
    err = Exception(faker.sentence())
    mock_copy.side_effect = err
    ErrorDialog.run = lambda _: None

    main_window.import_database("tests/data/main.dba")

    dialog.assert_called_with(ERROR_DB_IMPORT, err)
    dialog.return_value.run.assert_called()

    assert Database("main") not in main_window.databases
    assert not main_window.statusbar.label.text

    # the database shouldn't be in db_list
    for row in main_window.db_list.children:
        label = row.children[0].children[-1]
        assert "main" != label.text


@patch("gi.repository.Gtk.FileChooserDialog", autospec=True)
def test_export_dialog_Cancel(mock: Mock, databases, main_window):
    # select main database
    row = main_window.db_list.children[2]
    main_window.db_list.select_row(row)

    # choose Cancel in the dialog
    mock.return_value.run.return_value = Gtk.ResponseType.CANCEL
    main_window.export_database = Mock()

    main_window.on_export_database()
    main_window.export_database.assert_not_called()


@patch("gi.repository.Gtk.FileChooserDialog", autospec=True)
def test_export_dialog_Export(mock: Mock, databases, main_window, faker):
    # select main database
    row = main_window.db_list.children[2]
    main_window.db_list.select_row(row)

    # choose export location
    filename = faker.file_name()
    mock.return_value.filename = filename

    mock.return_value.run.return_value = Gtk.ResponseType.ACCEPT
    main_window.export_database = Mock()

    main_window.on_export_database()
    main_db = main_window.databases[2]

    assert main_window.dialog.current_name == "main.dba"
    main_window.export_database.assert_called_with(main_db, filename)


@patch("gi.repository.Gtk.FileChooserDialog", autospec=True)
def test_export_database_no_selection(mock: Mock, databases, main_window, faker):
    # no database is selected
    main_window.on_export_database()

    assert main_window.statusbar.label.text == f"✘ {SELECT_DB_TO_EXPORT}"
    mock.return_value.run.assert_not_called()


def test_export_database_success(databases, main_window, src_dir):
    main_db = main_window.databases[2]
    test_dir = src_dir / "test"
    test_dir.mkdir()

    main_window.export_database(main_db, test_dir)

    assert (test_dir / "main.dba").exists()
    assert main_window.statusbar.label.text == f"✔ {SUCCESS_DB_EXPORT}"


@patch("shutil.copy", autospec=True)
@patch("core.main_window.ErrorDialog", autospec=True)
def test_export_database_error(dialog: Mock, mock_copy: Mock, main_window, faker):
    err = Exception(faker.sentence())
    mock_copy.side_effect = err
    ErrorDialog.run = lambda _: None

    main_window.export_database(Database("main"), "")

    dialog.assert_called_with(ERROR_DB_EXPORT, err)
    dialog.return_value.run.assert_called()
    assert not main_window.statusbar.label.text
