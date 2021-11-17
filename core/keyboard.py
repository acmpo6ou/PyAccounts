#!/usr/bin/python3

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

"""
Simple API to simulate key press events.
Note: some code of this module is taken from pyautogui library.
"""

import os

import Xlib.XK
from Xlib import X
from Xlib.display import Display
from Xlib.ext.xtest import fake_input

KEY_NAMES = (
    "\t",
    "\n",
    "\r",
    " ",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
    "accept",
    "add",
    "alt",
    "altleft",
    "altright",
    "apps",
    "backspace",
    "browserback",
    "browserfavorites",
    "browserforward",
    "browserhome",
    "browserrefresh",
    "browsersearch",
    "browserstop",
    "capslock",
    "clear",
    "convert",
    "ctrl",
    "ctrlleft",
    "ctrlright",
    "decimal",
    "del",
    "delete",
    "divide",
    "down",
    "end",
    "enter",
    "esc",
    "escape",
    "execute",
    "f1",
    "f10",
    "f11",
    "f12",
    "f13",
    "f14",
    "f15",
    "f16",
    "f17",
    "f18",
    "f19",
    "f2",
    "f20",
    "f21",
    "f22",
    "f23",
    "f24",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "final",
    "fn",
    "hanguel",
    "hangul",
    "hanja",
    "help",
    "home",
    "insert",
    "junja",
    "kana",
    "kanji",
    "launchapp1",
    "launchapp2",
    "launchmail",
    "launchmediaselect",
    "left",
    "modechange",
    "multiply",
    "nexttrack",
    "nonconvert",
    "num0",
    "num1",
    "num2",
    "num3",
    "num4",
    "num5",
    "num6",
    "num7",
    "num8",
    "num9",
    "numlock",
    "pagedown",
    "pageup",
    "pause",
    "pgdn",
    "pgup",
    "playpause",
    "prevtrack",
    "print",
    "printscreen",
    "prntscrn",
    "prtsc",
    "prtscr",
    "return",
    "right",
    "scrolllock",
    "select",
    "separator",
    "shift",
    "shiftleft",
    "shiftright",
    "sleep",
    "space",
    "stop",
    "subtract",
    "tab",
    "up",
    "volumedown",
    "volumemute",
    "volumeup",
    "win",
    "winleft",
    "winright",
    "yen",
    "command",
    "option",
    "optionleft",
    "optionright",
)

display = Display(os.environ["DISPLAY"])

keyboardMapping = dict([(key, None) for key in KEY_NAMES])
keyboardMapping.update(
    {
        "backspace": display.keysym_to_keycode(Xlib.XK.string_to_keysym("BackSpace")),
        "\b": display.keysym_to_keycode(Xlib.XK.string_to_keysym("BackSpace")),
        "tab": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Tab")),
        "enter": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Return")),
        "return": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Return")),
        "shift": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Shift_L")),
        "ctrl": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Control_L")),
        "alt": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Alt_L")),
        "pause": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Pause")),
        "capslock": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Caps_Lock")),
        "esc": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Escape")),
        "escape": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Escape")),
        "pgup": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Page_Up")),
        "pgdn": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Page_Down")),
        "pageup": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Page_Up")),
        "pagedown": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Page_Down")),
        "end": display.keysym_to_keycode(Xlib.XK.string_to_keysym("End")),
        "home": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Home")),
        "left": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Left")),
        "up": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Up")),
        "right": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Right")),
        "down": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Down")),
        "select": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Select")),
        "print": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Print")),
        "execute": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Execute")),
        "prtsc": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Print")),
        "prtscr": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Print")),
        "prntscrn": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Print")),
        "printscreen": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Print")),
        "insert": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Insert")),
        "del": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Delete")),
        "delete": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Delete")),
        "help": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Help")),
        "win": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Super_L")),
        "winleft": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Super_L")),
        "winright": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Super_R")),
        "apps": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Menu")),
        "num0": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_0")),
        "num1": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_1")),
        "num2": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_2")),
        "num3": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_3")),
        "num4": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_4")),
        "num5": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_5")),
        "num6": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_6")),
        "num7": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_7")),
        "num8": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_8")),
        "num9": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_9")),
        "multiply": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_Multiply")),
        "add": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_Add")),
        "separator": display.keysym_to_keycode(
            Xlib.XK.string_to_keysym("KP_Separator")
        ),
        "subtract": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_Subtract")),
        "decimal": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_Decimal")),
        "divide": display.keysym_to_keycode(Xlib.XK.string_to_keysym("KP_Divide")),
        "f1": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F1")),
        "f2": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F2")),
        "f3": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F3")),
        "f4": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F4")),
        "f5": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F5")),
        "f6": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F6")),
        "f7": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F7")),
        "f8": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F8")),
        "f9": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F9")),
        "f10": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F10")),
        "f11": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F11")),
        "f12": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F12")),
        "f13": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F13")),
        "f14": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F14")),
        "f15": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F15")),
        "f16": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F16")),
        "f17": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F17")),
        "f18": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F18")),
        "f19": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F19")),
        "f20": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F20")),
        "f21": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F21")),
        "f22": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F22")),
        "f23": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F23")),
        "f24": display.keysym_to_keycode(Xlib.XK.string_to_keysym("F24")),
        "numlock": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Num_Lock")),
        "scrolllock": display.keysym_to_keycode(
            Xlib.XK.string_to_keysym("Scroll_Lock")
        ),
        "shiftleft": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Shift_L")),
        "shiftright": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Shift_R")),
        "ctrlleft": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Control_L")),
        "ctrlright": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Control_R")),
        "altleft": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Alt_L")),
        "altright": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Alt_R")),
        # These are added because unlike a-zA-Z0-9, the single characters do not have a
        " ": display.keysym_to_keycode(Xlib.XK.string_to_keysym("space")),
        "space": display.keysym_to_keycode(Xlib.XK.string_to_keysym("space")),
        "\t": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Tab")),
        "\n": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Return")),
        # for some reason this needs to be cr, not lf
        "\r": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Return")),
        "\e": display.keysym_to_keycode(Xlib.XK.string_to_keysym("Escape")),
        "!": display.keysym_to_keycode(Xlib.XK.string_to_keysym("exclam")),
        "#": display.keysym_to_keycode(Xlib.XK.string_to_keysym("numbersign")),
        "%": display.keysym_to_keycode(Xlib.XK.string_to_keysym("percent")),
        "$": display.keysym_to_keycode(Xlib.XK.string_to_keysym("dollar")),
        "&": display.keysym_to_keycode(Xlib.XK.string_to_keysym("ampersand")),
        '"': display.keysym_to_keycode(Xlib.XK.string_to_keysym("quotedbl")),
        "'": display.keysym_to_keycode(Xlib.XK.string_to_keysym("apostrophe")),
        "(": display.keysym_to_keycode(Xlib.XK.string_to_keysym("parenleft")),
        ")": display.keysym_to_keycode(Xlib.XK.string_to_keysym("parenright")),
        "*": display.keysym_to_keycode(Xlib.XK.string_to_keysym("asterisk")),
        "=": display.keysym_to_keycode(Xlib.XK.string_to_keysym("equal")),
        "+": display.keysym_to_keycode(Xlib.XK.string_to_keysym("plus")),
        ",": display.keysym_to_keycode(Xlib.XK.string_to_keysym("comma")),
        "-": display.keysym_to_keycode(Xlib.XK.string_to_keysym("minus")),
        ".": display.keysym_to_keycode(Xlib.XK.string_to_keysym("period")),
        "/": display.keysym_to_keycode(Xlib.XK.string_to_keysym("slash")),
        ":": display.keysym_to_keycode(Xlib.XK.string_to_keysym("colon")),
        ";": display.keysym_to_keycode(Xlib.XK.string_to_keysym("semicolon")),
        "<": display.keysym_to_keycode(Xlib.XK.string_to_keysym("less")),
        ">": display.keysym_to_keycode(Xlib.XK.string_to_keysym("greater")),
        "?": display.keysym_to_keycode(Xlib.XK.string_to_keysym("question")),
        "@": display.keysym_to_keycode(Xlib.XK.string_to_keysym("at")),
        "[": display.keysym_to_keycode(Xlib.XK.string_to_keysym("bracketleft")),
        "]": display.keysym_to_keycode(Xlib.XK.string_to_keysym("bracketright")),
        "\\": display.keysym_to_keycode(Xlib.XK.string_to_keysym("backslash")),
        "^": display.keysym_to_keycode(Xlib.XK.string_to_keysym("asciicircum")),
        "_": display.keysym_to_keycode(Xlib.XK.string_to_keysym("underscore")),
        "`": display.keysym_to_keycode(Xlib.XK.string_to_keysym("grave")),
        "{": display.keysym_to_keycode(Xlib.XK.string_to_keysym("braceleft")),
        "|": display.keysym_to_keycode(Xlib.XK.string_to_keysym("bar")),
        "}": display.keysym_to_keycode(Xlib.XK.string_to_keysym("braceright")),
        "~": display.keysym_to_keycode(Xlib.XK.string_to_keysym("asciitilde")),
    }
)

for c in """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890""":
    keyboardMapping[c] = display.keysym_to_keycode(Xlib.XK.string_to_keysym(c))


def isShiftCharacter(character):
    return character.isupper() or character in set('~!@#$%^&*()_+{}|:">?')


def key_down(key):
    if isShiftCharacter(key):
        fake_input(display, X.KeyPress, keyboardMapping["shift"])

    fake_input(display, X.KeyPress, keyboardMapping[key])
    display.sync()


def key_up(key):
    if isShiftCharacter(key):
        fake_input(display, X.KeyRelease, keyboardMapping["shift"])

    fake_input(display, X.KeyRelease, keyboardMapping[key])
    display.sync()


def write(string):
    for key in string:
        if isShiftCharacter(key):
            fake_input(display, X.KeyPress, keyboardMapping["shift"])

        fake_input(display, X.KeyPress, keyboardMapping[key])
        fake_input(display, X.KeyRelease, keyboardMapping[key])
        fake_input(display, X.KeyRelease, keyboardMapping["shift"])
    display.sync()
