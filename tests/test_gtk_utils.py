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
from gi.repository import Gtk

from core.gtk_utils import ListOrder, abc_list_sort, delete_list_item


@pytest.mark.parametrize(
    "name1, name2, expected_order",
    (
        ("crypt", "main", ListOrder.ROW1_ROW2),
        ("main", "main", ListOrder.EQUAL),
        ("main", "crypt", ListOrder.ROW2_ROW1),
    ),
)
def test_abc_list_sort(name1, name2, expected_order):
    rows = []
    for name in (name1, name2):
        row = Gtk.ListBoxRow()
        label = Gtk.Label(name)
        box = Gtk.Box()

        box.add(label)
        row.add(box)
        rows.append(row)

    order = abc_list_sort(*rows)
    assert order == expected_order


def test_delete_item():
    list_box = Gtk.ListBox()
    for name in ("crypt", "data", "main"):
        label = Gtk.Label(name)
        box = Gtk.Box()
        box.add(label)
        list_box.add(box)

    delete_list_item(list_box, "data")
    assert len(list_box.children) == 2

    for row in list_box.children:
        label = row.children[0].children[0]
        assert label.text != "data"
