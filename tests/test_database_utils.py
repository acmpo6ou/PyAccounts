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
import shutil

import pytest

import core
from core.database_utils import Account, Database

account = Account(
    accountname="gmail",
    username="Gmail User",
    email="example@gmail.com",
    password="123",
    birthdate="01.01.2000",
    notes="My gmail account.",
    copy_email=False,
    attached_files={"file1": "ZmlsZTEgY29udGVudAo=", "file2": "ZmlsZTIgY29udGVudAo="},
)

account2 = Account(
    accountname="mega",
    username="Mega User",
    email="example@gmail.com",
    password="312",
    birthdate="05.01.2000",
    notes="My mega account.",
)

accounts = {
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


@pytest.fixture()
def src_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(core.database_utils, "SRC_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def main_db(src_dir):
    shutil.copy("tests/data/main.dba", src_dir)


def test_account_to_dict():
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


def test_account_from_dict():
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


def test_dumps():
    database = Database("main", "123", accounts)
    json = database.dumps()
    assert json == ACCOUNTS_JSON


def test_loads():
    database = Database("main")
    database.loads(ACCOUNTS_JSON)
    assert database.accounts == accounts


def test_database_opened():
    with_password = Database("main", "123")
    without_password = Database("main")

    assert with_password.opened
    assert not without_password.opened


def test_open_database(main_db):
    database = Database("main")
    database.open("123")

    assert database.password == "123"
    assert database.accounts == accounts


def test_close_database():
    database = Database("main", "123", accounts)
    database.close()

    assert database.password is None
    assert not database.accounts


def test_create_database(src_dir, salt):
    database = Database("main", "123", accounts)
    database.create()

    with open(src_dir / "main.dba", "rb") as db_file:
        actual_salt = db_file.read(16)
        assert actual_salt == salt

        token = db_file.read()
        data = Database.decrypt(token, "123", salt).decode()
        assert data == ACCOUNTS_JSON


def test_delete_database(src_dir, main_db):
    # GIVEN we have two databases: main (provided by main_db fixture) and crypt
    shutil.copy("tests/data/main.dba", src_dir / "crypt.dba")

    # WHEN we delete main
    db = Database("main")
    db.delete()

    # THEN its .dba file should be removed
    assert not (src_dir / "main.dba").exists()

    # and crypt.dba should be still there
    assert (src_dir / "crypt.dba").exists()
