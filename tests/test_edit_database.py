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

from core.database_utils import Database
from core.database_window import DatabaseWindow
from core.edit_database import EditDatabase
from core.gtk_utils import item_name


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


def test_edit_database_success(src_dir, form):
    win = DatabaseWindow(form.main_window.databases[2], form.main_window)
    form.main_window.windows["main"] = win

    form.name.text = "database"
    form.password.text = "321"
    form.repeat_password.text = "321"
    form.on_apply()

    assert (src_dir / "database.dba").exists()
    assert not (src_dir / "main.dba").exists()
    
    db_names = [database.name for database in form.main_window.databases]
    assert "database" in db_names
    assert "main" not in db_names

    # db_list should also be updated
    db_names = [item_name(row) for row in form.main_window.db_list.children]
    assert "database" in db_names
    assert "main" not in db_names

    # the edit database form should be hidden
    assert len(form.main_window.form_box.children) == 0

    # DatabaseWindow of current database should be updated
    assert "main" not in form.main_window.windows

    win = form.main_window.windows["database"]
    assert win.database.name == "database"
    assert win.database.password == "321"
    assert win.title == "database"
