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
from string import digits, ascii_lowercase, ascii_uppercase, punctuation

import pytest
from gi.repository import Gtk

from core.generate_password import GenPassDialog


@pytest.mark.parametrize("punct", (True, False))
@pytest.mark.parametrize("upper", (True, False))
@pytest.mark.parametrize("lower", (True, False))
@pytest.mark.parametrize("nums", (True, False))
def test_generate_password(nums, lower, upper, punct):
    pass1 = Gtk.Entry()
    pass2 = Gtk.Entry()
    dialog = GenPassDialog(pass1, pass2)

    dialog.numbers.active = nums
    dialog.lower.active = lower
    dialog.upper.active = upper
    dialog.punctuation.active = punct

    dialog.on_generate()
    assert pass1.text == pass2.text

    # check if password contains at least one of numbers, lower letters, etc...
    assert any(c in pass1.text for c in digits) == nums
    assert any(c in pass1.text for c in ascii_lowercase) == lower
    assert any(c in pass1.text for c in ascii_uppercase) == upper
    assert any(c in pass1.text for c in punctuation) == punct
