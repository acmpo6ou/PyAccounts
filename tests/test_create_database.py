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

from core.create_database import CreateDatabase
from core.database_utils import Database
from core.gtk_utils import wait_until
from core.widgets import NAME_TAKEN_ERROR, EMPTY_NAME_ERROR, UNALLOWED_CHARS_WARNING


@pytest.fixture
def form(databases, main_window):
    form = CreateDatabase(main_window)
    main_window.databases = [Database("main")]
    main_window.show_form(form)
    main_window.show_all()
    return form


def test_name_error(form):
    # name field contains a name that isn't taken
    form.name.text = "good name"
    wait_until(lambda: not form.name_error.mapped)
    assert form.validate_name()

    # name field has a name that is already taken
    form.name.text = "main"
    wait_until(lambda: form.name_error.mapped)
    assert form.name_error.text == NAME_TAKEN_ERROR
    assert not form.validate_name()

    # name field is empty
    form.name.text = ""
    wait_until(lambda: form.name_error.mapped)
    assert form.name_error.text == EMPTY_NAME_ERROR
    assert not form.validate_name()


def test_filter_name(form):
    form.name.text = "clean name"
    assert form.name.text == "clean name"
    assert form.main_window.statusbar.label.text == ""

    form.name.text = "-c/l(e)a%n. n$a!m*e_"
    assert form.name.text == "-cl(e)an. name_"
    assert form.main_window.statusbar.label.text == f"✘ {UNALLOWED_CHARS_WARNING}"


def test_password_errors(form):
    form.password.text = "123"
    form.repeat_password.text = "321"
    wait_until(lambda: not form.password_error.mapped)
    wait_until(lambda: form.passwords_diff_error.mapped)
    assert not form.validate_passwords()

    form.password.text = ""
    form.repeat_password.text = ""
    wait_until(lambda: form.password_error.mapped)
    wait_until(lambda: not form.passwords_diff_error.mapped)
    assert not form.validate_passwords()

    form.password.text = "123"
    form.repeat_password.text = "123"
    wait_until(lambda: not form.password_error.mapped)
    wait_until(lambda: not form.passwords_diff_error.mapped)
    assert form.validate_passwords()
