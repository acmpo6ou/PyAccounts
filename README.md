[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![GTK version](https://img.shields.io/badge/gtk-v3.24+-success)
![Python version](https://img.shields.io/badge/python-v3.10-success)

# PyAccounts
**PyAccounts** – is a simple accounts database manager made using Python 3 and GTK 3.

You can easily manage your accounts and store them safely in encrypted databases.
The interface of PyAccounts is common and easy to use.
PyAccounts is completely free and open source project.

## Installation
```commandline
sudo add-apt-repository ppa:acmpo6ou/pyaccounts
sudo apt update
sudo apt install pyaccounts
```

## Development
```commandline
sudo apt install libcairo2 libcairo2-dev libgirepository1.0-dev python3-tk devscripts debhelper python3-paramiko
```

## Updating
- run tests
- Change version by search and replace in PyAccounts folder!
    - usually `PyAccounts.desktop` and `__init__.py`
- Generate changelog with `dch -i`
- Update install file if necessary
- Remove existing venv if requirements were changed
- `deactivate`!!!
- `deb/prevenv.sh`
- `debuild --no-tgz-check -S --lintian-opts --no-lintian`
- `lintian --info`
- `dput pyaccounts pyaccounts_1.x.x-1_source.changes`
