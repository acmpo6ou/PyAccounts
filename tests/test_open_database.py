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
import pytest

from core.open_database import OpenDatabase, OPEN_DB_TITLE


@pytest.fixture
def form(databases, main_window):
    form = OpenDatabase(main_window.databases[2])
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
