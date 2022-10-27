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
from unittest.mock import patch, PropertyMock, Mock

import pytest

from core.gtk_utils import wait_until, items_names
from core.rename_database import RenameDatabase, ERROR_RENAMING_DB
from core.widgets import ErrorDialog


@pytest.fixture
def form(databases, main_window):
    form = RenameDatabase(main_window.databases[2], main_window)
    main_window.show_form(form)
    main_window.show_all()
    return form


def test_form_startup(form):
    assert form.title.text == "Rename main database"
    assert form.name.text == "main"


def test_validate_name(form):
    form.name.text = "data"  # `data` is already taken
    wait_until(lambda: form.name_error.mapped)

    # it's OK, however, to change name back to `main`
    form.name.text = "main"
    assert not form.name_error.mapped


def test_apply_enabled(form):
    # enter incorrect name
    form.name.text = ""
    assert not form.apply.sensitive
    assert form.apply.label == "_Save"

    # enter good name
    form.name.text = "good name"
    assert form.apply.sensitive
    assert form.apply.label == "✨ _Save"


def test_rename_database_success(form, src_dir):
    form.name.text = "main2"
    form.on_apply()

    # database file should be renamed
    assert not (src_dir / "main.dba").exists()
    assert (src_dir / "main2.dba").exists()

    # database should be renamed in the db_list
    db_names = items_names(form.main_window.db_list)
    assert "main" not in db_names
    assert "main2" in db_names

    # the rename database form should be hidden
    assert len(form.main_window.form_box.children) == 0


@patch("core.rename_database.ErrorDialog", autospec=True)
@patch("core.rename_database.Database.dba_file", new_callable=PropertyMock)
def test_rename_database_error(mock, dialog: "Mock[ErrorDialog]", form, faker):
    err = Exception(faker.sentence())
    mock.side_effect = err

    form.name.text = "main2"
    form.on_apply()
    dialog.assert_called_with(ERROR_RENAMING_DB, err)

    # db_list should be unchanged
    db_names = items_names(form.main_window.db_list)
    assert "main" in db_names
    assert "main2" not in db_names

    # the rename database form shouldn't be hidden
    assert form.main_window.form_box.children[0].__class__ == RenameDatabase
