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

"""
Defines most fundamental classes for PyAccounts: Account and Database.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TypeAlias


@dataclass
class Account:
    accountname: str
    username: str
    email: str
    password: str
    birthdate: str
    notes: str
    copy_email: bool = True
    attached_files: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """
        Converts Account to dict renaming some fields.
        """

        field_mapping = {
            "accountname": "account",
            "username": "name",
            "birthdate": "date",
            "notes": "comment",
            "attached_files": "attach_files",
        }
        return {field_mapping.get(k, k): v for k, v in self.__dict__.items()}


Accounts: TypeAlias = dict[str, Account]


@dataclass
class Database:
    name: str
    password: str | None = None
    accounts: Accounts = field(default_factory=dict)

    @property
    def opened(self) -> bool:
        """
        Represents whether database is opened or not, the database is
        considered open when password is not None.
        """
        return False  # TODO: implement

    @property
    def saved(self) -> bool:
        """
        Represents whether in-memory database is same as database on the disk.

        Used to check whether database needs to be saved. It is needed when closing
        database. With it, we can determine whether to show confirmation dialog about unsaved
        data to user or not.
        """
        # TODO: create new Database instance, a copy of self
        # TODO: use open() on new instance to read data from disk
        # TODO: compare `accounts` property of self and disk database
        return False

    def loads(self, string: str) -> Accounts:
        """
        Deserializes json string to dict of accounts.
        """
        # TODO: use json to deserialize string, then replace dicts inside accounts dict with
        #  corresponding Account instances.

    def dumps(self, accounts: Accounts) -> str:
        """
        Serializes accounts dict to json.
        """
        # TODO: use to_dict of Account to convert it to dict,
        #  serialize resulting dict of account dicts

    @staticmethod
    def gensalt() -> bytes:
        """
        Generates 16 purely random bytes of salt.
        """
        return b""

    def encrypt(self, string: str, salt: bytes) -> str:
        """
        Encrypts given string using database password and salt.
        """

    def decrypt(self, string: str, salt: bytes) -> str:
        """
        Decrypts given string using database password and salt.
        """

    def open(self, password: str):
        """
        Opens database using its name, password and salt.

        In particular opening database means reading content of corresponding .dba file,
        decrypting and deserializing it, then assigning deserialized accounts dict to `accounts`
        field of Database.
        :param password: password to open the database.
        """
        # TODO: save password to `password` field
        # TODO: read .dba file; assign first 16 bytes to `salt` and decrypt remaining bytes,
        #  fill `accounts` property

    def close(self):
        """
        Clears `password` and `accounts` fields, effectively closing the database.
        """

    def create(self):
        """
        Creates .dba file for database using its name and password.
        """
        # TODO: use gensalt() to generate salt

    def delete(self):
        """
        Deletes .dba file associated with this Database instance.
        """

    def rename(self, name: str):
        """
        Renames .dba file associated with this Database instance.
        :param name: new database name.
        """
        # TODO: set self.name to new name

    def save(self, name: str, password: str, accounts: Accounts):
        """
        Deletes old database and creates new one, more specifically:
        it replaces old database with a new one.

        :param name: new name for the database.
        :param password: new password for the database.
        :param accounts: new `accounts` dict for the database.
        """
