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

from core.gtk_utils import wait_until
from core.open_database import OpenDatabase, ERROR_DB_OPENING
from core.widgets import ErrorDialog


@pytest.fixture
def form(databases, main_window):
    form = OpenDatabase(main_window.databases[2], main_window)
    main_window.show_form(form)
    main_window.show_all()
    return form


def test_form_title(form):
    assert form.title.text == "Open main database"


def test_toggle_password(form):
    assert not form.password.visibility
    form.toggle_password_visibility()
    assert form.password.visibility
    form.toggle_password_visibility()
    assert not form.password.visibility


def test_clear_password(form):
    form.password.text = "123"
    form.clear_password()
    assert not form.password.text


def test_password_prefill(databases, main_window):
    form = OpenDatabase(main_window.databases[2], main_window)
    assert not form.password.text

    main_window.safe_clipboard = "passw0rd"
    form = OpenDatabase(main_window.databases[2], main_window)
    assert form.password.text == "passw0rd"


def test_open_database_success(form: OpenDatabase):
    form.password.text = "123"
    form.on_open_database()

    assert not form.incorrect_password.mapped
    assert form.main_window.databases[2].password == "123"
    assert len(form.main_window.form_box.children) == 0

    win = form.main_window.windows["main"]
    assert win.database == form.main_window.databases[2]


def test_open_database_incorrect_password(form):
    form.password.text = "pas"
    form.on_open_database()
    wait_until(lambda: form.incorrect_password.mapped)
    assert form.main_window.databases[2].password is None

    # when the user starts typing again, the error should disappear
    form.password.text = "pass"
    assert not form.incorrect_password.mapped


@patch("core.open_database.ErrorDialog", autospec=True)
@patch("core.open_database.Database.dba_file", new_callable=PropertyMock)
def test_open_database_error(mock, dialog: "Mock[ErrorDialog]", form, faker):
    err = Exception(faker.sentence())
    mock.side_effect = err

    form.on_open_database()
    dialog.assert_called_with(ERROR_DB_OPENING, err)

    # the open database form shouldn't be hidden
    assert form.main_window.form_box.children[0].__class__ == OpenDatabase

    # database password should be cleared
    assert form.main_window.databases[2].password is None
