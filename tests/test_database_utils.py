#  Copyright (c) 2021-2023. Bohdan Kolvakh
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
import shutil

import pytest

from core.database_utils import Account, Database


@pytest.fixture
def account2():
    return Account(
        accountname="mega",
        username="Mega User",
        email="example@gmail.com",
        password="312",
        birthdate="05.01.2000",
        notes="My mega account.",
    )


@pytest.fixture
def accounts(account, account2):
    return {
        account.accountname: account,
        account2.accountname: account2,
    }


ACCOUNTS_JSON = (
    '{"gmail": {"account": "gmail", "name": "Gmail User", "email": '
    '"example@gmail.com", "password": "123", "date": "01.01.2000", "comment": "My '
    'gmail account.", "copy_email": false, "attach_files": {"file1": "ZmlsZTEgY29udGVudAo='
    '", "file2": "ZmlsZTIgY29udGVudAo="}}, "mega": {"account": "mega", "name": '
    '"Mega User", "email": "example@gmail.com", "password": "312", "date": '
    '"05.01.2000", "comment": "My mega account.", "copy_email": true, '
    '"attach_files": {}}}'
)


@pytest.fixture()
def salt(monkeypatch):
    salt = b"0123456789abcdef"
    monkeypatch.setattr("os.urandom", lambda x: salt)
    return salt


@pytest.fixture
def main_db(src_dir):
    shutil.copy("tests/data/main.dba", src_dir)


def test_account_to_dict(account):
    account_dict = account.to_dict()

    expected_dict = {
        "account": "gmail",
        "name": "Gmail User",
        "email": "example@gmail.com",
        "password": "123",
        "date": "01.01.2000",
        "comment": "My gmail " "account.",
        "copy_email": False,
        "attach_files": {"file1": "ZmlsZTEgY29udGVudAo=", "file2": "ZmlsZTIgY29udGVudAo="},
    }
    assert account_dict == expected_dict


def test_account_from_dict(account):
    _dict = {
        "account": "gmail",
        "name": "Gmail User",
        "email": "example@gmail.com",
        "password": "123",
        "date": "01.01.2000",
        "comment": "My gmail " "account.",
        "copy_email": False,
        "attach_files": {"file1": "ZmlsZTEgY29udGVudAo=", "file2": "ZmlsZTIgY29udGVudAo="},
    }

    _account = Account.from_dict(_dict)

    assert _account == account


def test_dumps(accounts):
    database = Database("main", "123", accounts)
    json = database.dumps()
    assert json == ACCOUNTS_JSON


def test_loads(accounts):
    database = Database("main")
    database.loads(ACCOUNTS_JSON)
    assert database.accounts == accounts


def test_database_opened():
    with_password = Database("main", "123")
    without_password = Database("main")

    assert with_password.opened
    assert not without_password.opened


def test_open_database(main_db, accounts):
    database = Database("main")
    database.open("123")

    assert database.password == "123"
    assert database.accounts == accounts


def test_close_database(accounts):
    database = Database("main", "123", accounts)
    database.close()

    assert database.password is None
    assert not database.accounts


def test_create_database(src_dir, salt, accounts):
    database = Database("main", "123", accounts)
    database.create()

    with open(src_dir / "main.dba", "rb") as db_file:
        actual_salt = db_file.read(16)
        assert actual_salt == salt

        token = db_file.read()
        data = Database.decrypt(token, "123", salt).decode()
        assert data == ACCOUNTS_JSON


def test_rename_database(src_dir, main_db):
    db = Database("main")
    db.rename("crypt")

    assert db.name == "crypt"
    assert not (src_dir / "main.dba").exists()
    assert (src_dir / "crypt.dba").exists()


def test_database_saved(main_db, accounts):
    db = Database("main", "123", accounts)
    assert db.saved

    del db.accounts["gmail"]
    assert not db.saved


def test_database_saved_no_database(main_db, accounts):
    """
    database.saved should return False if the database on disk doesn't exist.
    """
    db = Database("main", "123", accounts)
    assert db.saved

    db.dba_file.unlink()
    assert not db.saved


def test_save_database(src_dir, main_db, accounts):
    db = Database("main", "123", accounts)

    new_accounts = accounts.copy()
    del new_accounts["mega"]
    db.save("crypt", "321", new_accounts)

    new_db = Database("crypt")
    new_db.open("321")
    assert new_db.accounts == new_accounts
    assert not (src_dir / "main.dba").exists()


def test_save_database_name_didnt_change(src_dir, main_db, accounts):
    """
    Saving a database when its name didn't change.

    For Database.save(), it's important to first delete old database and then create new one,
    not the other way around. Because if the name of the database didn't change during saving,
    the database file will be removed.
    """
    db = Database("main", "123", accounts)

    new_accounts = accounts
    del new_accounts["mega"]
    db.save("main", "321", new_accounts)  # the name is still `main`

    new_db = Database("main")
    new_db.open("321")
    assert new_db.accounts == new_accounts
