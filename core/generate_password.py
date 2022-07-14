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

from gi.repository import Gtk

from core.gtk_utils import GladeTemplate


class GenPassDialog(GladeTemplate):
    # <editor-fold>
    length_adj: Gtk.Adjustment
    parent_widget: Gtk.Dialog
    length: Gtk.SpinButton
    numbers: Gtk.CheckButton
    upper: Gtk.CheckButton
    lower: Gtk.CheckButton
    punctuation: Gtk.CheckButton
    # </editor-fold>

    PASSWORD_LENGTH = 16

    """
    A dialog to generate password.
    """

    def __init__(self, pass1: Gtk.Entry, pass2: Gtk.Entry):
        super().__init__("generate_password")

        # TODO: set password length to PASSWORD_LENGTH
        self.pass1 = pass1
        self.pass2 = pass2

    def on_cancel(self, _):
        self.parent_widget.hide()

    def genpass(self, length, chars) -> str:
        """
        Generates random password.

        :param length: length of password to generate.
        :param chars: list of strings with characters from which to generate password.
        """
        # TODO: uncomment this
        # concatenate all character strings from `chars` into one big string
        # chars_str = "".join(chars)
        # generate purely random password from characters of chars_str
        # "".join(secrets.choice(chars_str) for _ in range(length))

        # Because password generates randomly it won't necessarily contain all characters that
        # are specified in `chars`.
        # So here we check that generated password contains at least one character from each string
        # specified in `chars` and if it doesn't, we regenerate password
        # TODO: implement password regeneration

    def on_generate(self, _=None):
        """
        Generates password and fills pass1 and pass2 password fields with it.
        """

        all_chars = (digits, ascii_lowercase, ascii_uppercase, punctuation)
        checkboxes = (self.numbers, self.lower, self.upper, self.punctuation)
        chars = []

        """
        For each index, checkbox in enumerate checkboxes:
            if it is checked:
                get characters associated with that checkbox (using all_chars[index])
                add them to chars

        call genpass passing it chars and password length
        fill password fields with generated password
        hide dialog
        """
        # TODO: save last password length in PASSWORD_LENGTH
