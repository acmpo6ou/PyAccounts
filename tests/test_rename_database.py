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

from core.gtk_utils import wait_until
from core.rename_database import RenameDatabase


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

