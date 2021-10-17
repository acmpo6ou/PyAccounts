#!/usr/bin/python3

#  Copyright (c) 2022. Bohdan Kolvakh
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

import gi

gi.require_version("Gtk", "3.0")
from core.gtk_utils import GladeTemplate
from string import digits, ascii_lowercase, ascii_uppercase, punctuation

ALL_CHARS = (digits, ascii_lowercase, ascii_uppercase, punctuation)


class GenPassDialog(GladeTemplate):
    """
    A dialog to generate password.
    """

    def __init__(self, pass1, pass2):
        super().__init__("generate_password")
        self.checkboxes = (self.numbers, self.lower, self.upper, self.punctuation)

        self.pass1 = pass1
        self.pass2 = pass2

    def on_cancel(self, _):
        self.parent_widget.hide()

    def genpass(self, length, chars):
        """
        Generates random password.

        :param length: length of password to generate.
        :param chars: characters from which to generate password.
        :return: generated random password.
        """
        # Because password generates randomly it won't necessarily contain all characters that
        # are specified in `chars`.
        # So here we check that generated password contains at least one character from each string
        # specified in `chars` and if it doesn't, we regenerate password

    def on_generate(self, _):
        """
        Generates password and fills pass1 and pass2 password fields with it.
        """
        """
        chars = []
        For each index, checkbox in enumerate checkboxes:
            if it is checked:
                get characters associated with that checkbox (using ALL_CHARS[index])
                add them to chars

        call genpass passing it chars and password length
        fill password fields with generated password
        hide dialog
        """
