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

from core.create_database import CreateDatabase
from core.gtk_utils import wait_until


def test_empty_name_error(databases, main_window):
    form = CreateDatabase(main_window)
    main_window.show_form(form)
    main_window.show_all()

    form.name.text = ""
    wait_until(lambda: form.name_error.mapped)
    assert not form.validate_name()

    form.name.text = "not empty"
    wait_until(lambda: not form.name_error.mapped)
    assert form.validate_name()
