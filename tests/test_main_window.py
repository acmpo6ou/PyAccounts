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
from gi.repository import Gtk, GdkPixbuf

from core.database_utils import Database
from core.main_window import MainWindow


@pytest.fixture
def databases(src_dir):
    shutil.copy("tests/data/main.dba", src_dir)
    shutil.copy("tests/data/main.dba", src_dir / "crypt.dba")
    shutil.copy("tests/data/main.dba", src_dir / "data.dba")


def test_get_databases(databases):
    main_window = MainWindow()
    dbs = main_window.get_databases()

    expected_dbs = [Database("crypt"), Database("data"), Database("main")]
    assert dbs == expected_dbs


def test_load_databases(databases):
    # load_databases is called by MainWindow constructor
    main_window = MainWindow()

    # get icons and labels of elements in the database list
    icons = []
    labels = []

    for row in main_window.db_list.children:
        hbox: Gtk.HBox = row.children[0]
        icons.append(hbox.children[0])
        labels.append(hbox.children[1])

    # all icons should be PyAccounts app icons
    expected_icon = Gtk.Image.new_from_file("img/icon.svg")
    for icon in icons:
        icon: Gtk.Image
        p: GdkPixbuf.Pixbuf = icon.pixbuf
        assert icon.pixbuf == expected_icon.pixbuf
    assert len(icons) == 3

    # all labels should contain appropriate databases names
    db_names = [label.text for label in labels]
    assert db_names == ["main", "data", "crypt"]
