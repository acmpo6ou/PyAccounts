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

"""
Defines most fundamental classes for PyAccounts: Account and Database.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Account:
    accountname: str
    username: str
    email: str
    password: str
    date: str
    notes: str
    copy_email: bool = True
    attached_files: Dict[str, str] = field(default_factory=dict)

    def to_dict(self):
        """
        Converts Account to dict renaming some fields.
        """
        # TODO: use Account.__dict__ method to convert it to dict
        # TODO: rename `notes` and `username` fields
