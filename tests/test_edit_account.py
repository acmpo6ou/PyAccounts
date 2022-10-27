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

from core.edit_account import EditAccount
from core.gtk_utils import notes_text, items_names


@pytest.fixture
def form(account, db_window, main_window):
    db = main_window.databases[2]
    return EditAccount(db, account, db_window)


def test_load_attached_paths(form):
    assert form.attached_paths["file1"] is None
    assert form.attached_paths["file2"] is None


def test_load_account(form, account):
    assert form.title.text == f"Edit {account.accountname} account"
    assert form.name.text == account.accountname
    assert form.email.text == account.email
    assert form.username.text == account.username
    assert not form.copy_email.active
    assert form.password.text == account.password
    assert form.repeat_password.text == account.password
    assert form.birth_date.text == account.birthdate
    assert account.notes == notes_text(form.notes)

    files = items_names(form.attached_files)
    assert files == ["file1", "file2"]


def test_load_already_attached_files(form, account):
    form.attach_file("tests/data/file1.txt")
    result = form.build_account()

    assert result.attached_files["file1.txt"] == 'RmlsZSAxIGNvbnRlbnQuCg=='
    assert result.attached_files["file1"] == "ZmlsZTEgY29udGVudAo="
    assert result.attached_files["file2"] == "ZmlsZTIgY29udGVudAo="


def test_edit_account(form, account):
    form.name.text = "my account"
    form.on_apply()

    assert account.accountname not in form.database.accounts
    assert "my account" in form.database.accounts

    accounts = items_names(form.database_window.accounts_list)
    assert account.accountname not in accounts
    assert "my account" in accounts
