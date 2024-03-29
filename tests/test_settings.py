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

from core.settings import Config, SettingsDialog


@pytest.fixture
def dialog(main_window, src_dir, monkeypatch):
    monkeypatch.setattr("core.settings.SRC_DIR", src_dir)
    return SettingsDialog(main_window)


def test_load_settings_empty_config(dialog):
    config = Config()
    assert config.separator_position == 0.67
    assert not config.main_db
    assert config.general_font == '30px "Ubuntu"'
    assert config.monospace_font == '35px "Ubuntu Mono"'


def test_load_settings(dialog, src_dir):
    shutil.copyfile("tests/data/settings.json", src_dir / "settings.json")
    config = Config()

    assert config.separator_position == 0.7
    assert config.main_db
    assert config.general_font == '32px "Ubuntu"'
    assert config.monospace_font == '32px "Ubuntu Mono"'


def test_save_settings(dialog, src_dir):
    settings = src_dir / "settings.json"
    settings.touch()
    config = Config()

    config.separator_position = 0.7
    config.main_db = True
    config.general_font = '32px "Ubuntu"'
    config.monospace_font = '32px "Ubuntu Mono"'

    config.save()
    expected_settings = open("tests/data/settings.json").read()
    settings = open(settings).read()
    assert settings == expected_settings


def test_load_preferences(dialog, main_window):
    main_window.config.general_font = '32px "Arial"'
    main_window.config.monospace_font = '24px "Inconsolata Medium"'
    main_window.config.main_db = True

    dialog.load_settings()
    assert dialog.general_font.font == "Arial 32"
    assert dialog.mono_font.font == "Inconsolata Medium 24"
    assert dialog.main_db.active


def test_save(dialog, main_window):
    dialog.general_font.font = "Arial 32"
    dialog.mono_font.font = "Inconsolata Medium 24"
    dialog.main_db.active = True
    dialog.on_save()

    assert main_window.config.general_font == '32px "Arial"'
    assert main_window.config.monospace_font == '24px "Inconsolata Medium"'
    assert main_window.config.main_db
