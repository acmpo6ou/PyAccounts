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
import time

from gi.repository import Gtk

from core.gtk_utils import wait_until
from core.widgets import StatusBar


def test_statusbar_message(faker):
    msg = faker.sentence()
    statusbar = StatusBar(Gtk.Label())

    statusbar.message(msg, 0.1)
    assert statusbar.label.text == msg

    # after 0.1 second the message should disappear
    wait_until(lambda: not statusbar.label.text)


def test_statusbar_success(faker):
    msg = faker.sentence()
    statusbar = StatusBar(Gtk.Label())

    statusbar.success(msg)
    assert statusbar.label.text == f"✔ {msg}"
