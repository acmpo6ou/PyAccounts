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

from core.edit_database import EditDatabase


@pytest.fixture
def form(databases, main_window):
    db = main_window.databases[2]
    db.open("123")
    form = EditDatabase(db, main_window)
    main_window.show_form(form)
    main_window.show_all()
    return form


def test_form_startup(form):
    assert form.title.text == "Edit main database"
    assert form.name.text == "main"
    assert form.password.text == "123"
    assert form.repeat_password.text == "123"
