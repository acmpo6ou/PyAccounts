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

import base64
import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

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

    field_mapping = {
        "accountname": "account",
        "username": "name",
        "birthdate": "date",
        "notes": "comment",
        "attached_files": "attach_files",
    }
    reversed_mapping = {v: k for k, v in field_mapping.items()}

    def to_dict(self) -> dict:
        """
        Converts Account to dict renaming some fields.
        """
        return {self.field_mapping.get(k, k): v for k, v in self.__dict__.items()}

    @staticmethod
    def from_dict(_dict: dict) -> "Account":
        """
        Creates Account from dict.

        Note, that we can't use dictionary unpacking because the dict contains
        some keys that are different from arguments that need to be passed to
        Account constructor.
        """

        args = {Account.reversed_mapping.get(k, k): v for k, v in _dict.items()}
        return Account(**args)


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
        return self.password is not None

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

    def loads(self, string: str):
        """
        Deserializes json string to dict of accounts.
        """

        accounts_dict = json.loads(string)
        for accountname, account_dict in accounts_dict.items():
            self.accounts[accountname] = Account.from_dict(account_dict)

    def dumps(self) -> str:
        """
        Serializes accounts dict to json.
        """
        # TODO: use to_dict of Account to convert it to dict,
        #  serialize resulting dict of account dicts
        accounts_dicts = {
            accountname: account.to_dict() for accountname, account in self.accounts.items()
        }
        return json.dumps(accounts_dicts)

    def encrypt(self, string: str, salt: bytes) -> str:
        """
        Encrypts given string using database password and salt.
        """

    def decrypt(self, token: bytes, salt: bytes) -> bytes:
        """
        Decrypts given token using database password and salt.
        """

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password.encode()))
        f = Fernet(key)
        return f.decrypt(token)

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

        self.password = None
        self.accounts = {}

    def create(self):
        """
        Creates .dba file for database using its name and password.
        """

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
