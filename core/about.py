#  Copyright (c) 2021. Bohdan Kolvakh
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

from gi.repository import Gtk

from core.gtk_utils import GladeTemplate


class AboutDialog(GladeTemplate):
    # <editor-fold>
    parent_widget: Gtk.AboutDialog
    # </editor-fold>

    def __init__(self):
        super().__init__("about")
        # TODO: set dialog version to current app version;
        #  use self.parent_widget.version and APP_VERSION constant

    def run(self):
        self.parent_widget.run()
