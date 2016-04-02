# -*- coding: utf-8 -*-

"""
Manage Message Shortcuts


"""

import json
import re
import prof

ENABLED = True
SHORTCUTS_DICTIONARY = {u'shrug': u'¯\_(ツ)_/¯',
                        u'yay': u'\o/'}

plugin_win = "Shortcuts"


def _handle_win_input(win, line):
    prof.win_show(win, line)


def create_win():
    if prof.win_exists(plugin_win) == False:
        prof.win_create(plugin_win, _handle_win_input)


def _substitute(message):
    if ENABLED:
        shortcuts = re.findall(r'(?:^|\s)(:\w+:)(?=\s|$)', message)
        for s in shortcuts:
            shortcut_text = SHORTCUTS_DICTIONARY.get(s.strip()[1:-1])
            if shortcut_text:
                message = message.replace(s.strip(), shortcut_text)

    return message


def save(key, value):
    global SHORTCUTS_DICTIONARY
    SHORTCUTS_DICTIONARY[key] = value


def _list_shortcuts():
    global SHORTCUTS_DICTIONARY
    # ordered_dict = sorted(DICTIONARY.items(), key=lambda t: t[0])
    prof.cons_show(u'Shortcuts: ')
    for key, value in SHORTCUTS_DICTIONARY.iteritems():
        prof.cons_show(u':{0}: => {1}'.format(key, value))


def _cmd_shortcuts(arg1=None, arg2=None, arg3=None):
    global ENABLED

    if arg1 == None:
        prof.cons_show("Shortcuts Plugin is {}.".format("ON" if ENABLED else "OFF"))
    elif arg1 == "on":
        ENABLED = True
    elif arg1 == "off":
        ENABLED = False
    elif arg1 == "list":
        _list_shortcuts()
    elif arg1 == "set":
        if arg2 == None:
            prof.cons_bad_cmd_usage("/shortcuts")
        else:
            save(arg2, arg3)
    else:
        prof.cons_bad_cmd_usage("/shortcuts")


def prof_pre_chat_message_send(jid, message):
    return _substitute(message)


def prof_pre_room_message_send(room, message):
    return _substitute(message)


def prof_pre_priv_message_send(room, nick, message):
    return _substitute(message)


def prof_init(version, status):
    synopsis = [
        "/shortcuts",
        "/shortcuts on|off",
        "/shortcuts set <name> <text>"
    ]
    description = "Manage shortcuts for emoticons or other stuff"
    args = [
        [ "on|off", "Enable/disable shortcuts" ],
        [ "set <name> <text>", "Save shortcut" ],
        [ "list", "List Shortcuts Dictionary"]
    ]
    examples = [
        "/shortcuts",
        "/shortcuts on",
        "/shortcuts set lol \"Laughing out loud\""
    ]

    prof.register_command("/shortcuts", 0, 3, synopsis, description, args, examples, _cmd_shortcuts)
    prof.register_ac("/shortcuts", [ "on", "off", "set" ])

    shortcut_keys = [":{}:".format(k) for k in SHORTCUTS_DICTIONARY.keys()]
    # prof.cons_show(", ".join(shortcut_keys))
    prof.register_ac(" ", shortcut_keys)