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
import secrets
from random import SystemRandom
from string import digits, ascii_lowercase, ascii_uppercase, punctuation

from gi.repository import Gtk

from core.gtk_utils import GladeTemplate


class GenPassDialog(GladeTemplate):
    # <editor-fold>
    length_adj_max: Gtk.Adjustment
    length_adj_min: Gtk.Adjustment
    parent_widget: Gtk.Dialog
    min_length: Gtk.SpinButton
    max_length: Gtk.SpinButton
    numbers: Gtk.CheckButton
    upper: Gtk.CheckButton
    lower: Gtk.CheckButton
    punctuation: Gtk.CheckButton
    # </editor-fold>

    MIN_PASSWORD_LENGTH = 16
    MAX_PASSWORD_LENGTH = 32
    CHECKBOXES_STATE = (True, True, True, True)

    """
    A dialog to generate password.
    """

    def __init__(self, pass1: Gtk.Entry, pass2: Gtk.Entry):
        super().__init__("generate_password")

        self.pass1 = pass1
        self.pass2 = pass2

        # load last values of length and checkboxes
        self.min_length.value = self.MIN_PASSWORD_LENGTH
        self.max_length.value = self.MAX_PASSWORD_LENGTH
        (
            self.numbers.active,
            self.lower.active,
            self.upper.active,
            self.punctuation.active,
        ) = self.CHECKBOXES_STATE

    def on_cancel(self, _):
        self.parent_widget.hide()

    def genpass(self, min_length, max_length, chars) -> str:
        """
        Generates random password of length between [min_length] and [max_length].

        :param min_length: minimum password length.
        :param max_length: maximum password length.
        :param chars: list of strings with characters from which to generate the password.
        """

        if not chars:
            return ""

        # concatenate all character strings from `chars` into one big string
        chars_str = "".join(chars)

        # the password of a random length will be generated since this is more secure
        min_length = int(min_length)
        max_length = int(max_length)
        length = SystemRandom().randint(min_length, max_length)

        # generate purely random password from characters of chars_str
        password = "".join(secrets.choice(chars_str) for _ in range(length))

        # Because password generates randomly it won't necessarily contain
        # all characters that are specified in `chars`.
        # So here we check that generated password contains at least one
        # character from each string specified in `chars` and if it doesn't, we regenerate password
        is_good = True
        for s in chars:
            is_good = is_good and any(c in password for c in s)

        if not is_good:
            password = self.genpass(min_length, max_length, chars)
        return password

    def on_generate(self, _=None):
        """
        Generates password and fills pass1 and pass2 password fields with it.
        """

        all_chars = (digits, ascii_lowercase, ascii_uppercase, punctuation)
        checkboxes = (self.numbers, self.lower, self.upper, self.punctuation)
        chars = [
            all_chars[i] for i, checkbox in enumerate(checkboxes) if checkbox.active
        ]

        password = self.genpass(self.min_length.value, self.max_length.value, chars)
        self.pass1.text = password
        self.pass2.text = password

        # save last used length and checkboxes values
        GenPassDialog.MIN_PASSWORD_LENGTH = self.min_length.value
        GenPassDialog.MAX_PASSWORD_LENGTH = self.max_length.value
        GenPassDialog.CHECKBOXES_STATE = (
            self.numbers.active,
            self.lower.active,
            self.upper.active,
            self.punctuation.active,
        )
        self.parent_widget.hide()
