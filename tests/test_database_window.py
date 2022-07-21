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
from gi.repository import GdkPixbuf

from core.database_window import DatabaseWindow
from core.gtk_utils import load_icon, item_name


@pytest.fixture
def window(databases, main_window):
    db = main_window.databases[2]
    db.open("123")
    return DatabaseWindow(db, main_window)


def test_window_title(window):
    assert window.title == "main"


def test_load_account_icon(window):
    gmail_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        "img/account_icons/gmail.svg", 50, 50, True
    )

    icon = window.load_account_icon("gmail")
    icon2 = window.load_account_icon("gmail2")
    icon3 = window.load_account_icon("_gmail")

    assert icon.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()
    assert icon2.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()
    assert icon3.pixbuf.get_pixels() == gmail_pixbuf.get_pixels()

    # `git` goes before `github` in assets,
    # but `github` should be a more exact match
    github_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        "img/account_icons/github.svg", 50, 50, True
    )
    icon = window.load_account_icon("GitHub")
    assert icon.pixbuf.get_pixels() == github_pixbuf.get_pixels()

    # if the icon wasn't found the default one should be loaded
    default = load_icon("cs-user-accounts", 50).pixbuf
    icon = window.load_account_icon("afjkdsjfjsjkfdjalsjfl")
    assert icon.pixbuf.get_pixels() == default.get_pixels()


def test_load_accounts(window):
    # load_accounts is called by DatabaseWindow constructor
    account_names = [item_name(row) for row in window.accounts_list.children]
    assert account_names == ["gmail", "mega"]
