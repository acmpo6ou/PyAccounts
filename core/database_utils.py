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
Utilities for working with databases such as opening, encrypting, serializing them, etc...
"""
from dataclasses import dataclass, field

from typing import Dict


@dataclass
class Account:
    accountname: str
    username: str
    email: str
    password: str
    date: str
    comment: str
    copy_email: bool = True
    attached_files: Dict[str, str] = field(default_factory=dict)
