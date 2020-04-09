# Written for Python 3+
from debug import *
from prompt import *
from game import *

char = False

splash("WELCOME!")
launch = True
while launch:
    #--------------------
    # Launch a prompt!
    # This creates the default prompt loop from which anything runs

    char = do_login()
    if char:
        splash(f"You enter the town.")
        while char:
            do_game(char)

    # end runtime loop
    #--------------------