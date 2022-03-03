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
def main_window():
    return MainWindow()
