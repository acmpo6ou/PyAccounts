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

from _pytest import monkeypatch

from core import settings
from core.settings import Config


def test_load_settings_empty_config():
    config = Config()
    assert config.separator_position == 1000
    assert not config.main_db
    assert config.general_font == "Ubuntu 30"
    assert config.monospace_font == "Ubuntu Mono 35"


def test_load_settings(src_dir, monkeypatch):
    monkeypatch.setattr("core.settings.SRC_DIR", src_dir)
    shutil.copyfile("tests/data/settings.json", src_dir / "settings.json")
    config = Config()

    assert config.separator_position == 2000
    assert config.main_db
    assert config.general_font == "Ubuntu 32"
    assert config.monospace_font == "Ubuntu Mono 64"
