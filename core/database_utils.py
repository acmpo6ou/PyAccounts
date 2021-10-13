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


@dataclass
class Database:
    name: str
    password: Optional[str] = None
    salt: Optional[bytes] = None
    accounts: Dict[str, Account] = field(default_factory=dict)

    @property
    def opened(self):
        """
        Represents whether database is opened or not, the database is
        considered opened when password is not None.
        """
        return False  # TODO: implement

    @property
    def saved(self):
        """
        Represents whether in-memory database is same as database on the disk.
        Used to check whether database needs to be saved. It is needed when closing
        database, with it we can determine whether to show confirmation dialog about unsaved
        data to user or not.
        """
        return False  # TODO: implement
