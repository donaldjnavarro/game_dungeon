# Written for Python 3+
from debug import *
from prompt import *
from game import *

char = False

print("\nType <help> to see the available commands.")

launch = True
while launch:
    #--------------------
    # Launch a prompt!
    # This creates the default prompt loop from which anything runs
    # 1. Send the user to the login page until they select a char
    # 2. After selecting a char, send the user to the town

    char = do_login()
    if char:
        splash(f"You enter the town.")
        while char:
            do_game(char)

    # end runtime loop
    #--------------------