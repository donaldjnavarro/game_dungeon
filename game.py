from prompt import *
from roster import *

def do_game(char):
    stat_commands = {
            "stat": {
                "title": "Character Stats",
                "commands": {"stat"},
                "action": display_char,
                "action_arg": char
            }
        }

    while char:
        prompt("",stat_commands)
