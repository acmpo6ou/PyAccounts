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
import platform
import shutil

import pytest

import core
from core.database_utils import Account
from core.database_window import DatabaseWindow
from core.main_window import MainWindow


@pytest.fixture()
def src_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(core, "SRC_DIR", tmp_path)
    return tmp_path


@pytest.fixture
def databases(src_dir):
    shutil.copy("tests/data/main.dba", src_dir)
    shutil.copy("tests/data/main.dba", src_dir / "crypt.dba")
    shutil.copy("tests/data/main.dba", src_dir / "data.dba")


@pytest.fixture
def main_window(monkeypatch, src_dir):
    monkeypatch.setattr("core.settings.SRC_DIR", src_dir)
    return MainWindow()


@pytest.fixture
def db_window(databases, main_window):
    db = main_window.databases[2]
    db.open("123")
    return DatabaseWindow(db, main_window)


@pytest.fixture
def account():
    return Account(
        accountname="gmail",
        username="Gmail User",
        email="example@gmail.com",
        password="123",
        birthdate="01.01.2000",
        notes="My gmail account.",
        copy_email=False,
        attached_files={"file1": "ZmlsZTEgY29udGVudAo=", "file2": "ZmlsZTIgY29udGVudAo="},
    )


@pytest.fixture(scope="session", autouse=True)
def mock_platform():
    """
    Always use Linux during tests to make dialogs consistent
    no matter on which OS you're running the tests.
    """
    platform.system = lambda: "Linux"
