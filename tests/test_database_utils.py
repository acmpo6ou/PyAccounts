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

from core.database_utils import Account, Database


account = Account(
    accountname="gmail",
    username="Gmail User",
    email="example@gmail.com",
    password="123",
    birthdate="01.01.2000",
    notes="My gmail account.",
    copy_email=False,
    attached_files={"file1": "file1 content", "file2": "file2 content"},
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
    'gmail account.", "copy_email": false, "attach_files": {"file1": "file1 '
    'content", "file2": "file2 content"}}, "mega": {"account": "mega", "name": '
    '"Mega User", "email": "example@gmail.com", "password": "312", "date": '
    '"05.01.2000", "comment": "My mega account.", "copy_email": true, '
    '"attach_files": {}}}'
)


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
        "attach_files": {"file1": "file1 content", "file2": "file2 content"},
    }
    assert account_dict == expected_dict


def test_database_opened():
    with_password = Database("main", "123")
    without_password = Database("main")

    assert with_password.opened
    assert not without_password.opened


def test_dumps():
    database = Database("main", "123", accounts)
    json = database.dumps()
    assert json == ACCOUNTS_JSON
