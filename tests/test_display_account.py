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

from core.display_account import DisplayAccount, NOTES_PLACEHOLDER
from core.gtk_utils import notes_text, item_name


@pytest.fixture
def form(account, db_window):
    return DisplayAccount(account, db_window)


def test_load_data(form: DisplayAccount, account):
    assert account.accountname in form.accountname.text
    assert account.email in form.email.text
    assert account.username in form.username.text
    assert "username" in form.to_copy.text
    assert '●' * 24 in form.password.text
    assert account.birthdate in form.birth_date.text
    assert notes_text(form.notes) == NOTES_PLACEHOLDER

    files = [item_name(row) for row in form.attached_files.children]
    assert files == ["file1", "file2"]
