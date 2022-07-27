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
from pathlib import Path

from PyAccounts import Application


def test_fix_src_dir(monkeypatch):
    monkeypatch.setattr("PyAccounts.SRC_DIR", "/tmp/.PyAccounts")
    app = Application()

    app.fix_src_dir()
    assert Path("/tmp/.PyAccounts").exists()
    Path("/tmp/.PyAccounts").rmdir()


def test_fix_settings(src_dir, monkeypatch):
    monkeypatch.setattr("PyAccounts.SRC_DIR", src_dir)
    app = Application()

    app.fix_settings()
    assert (src_dir / "settings.json").exists()
