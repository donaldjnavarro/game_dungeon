# Written for Python 3+
from debug import *
from prompt import *
import launch_var

splash("WELCOME?")
launch = True
while launch:
    #--------------------
    # Launch a prompt!
    # This creates the default prompt loop from which anything runs

    command = prompt()

    # Place any unique command calls here. These will define the user experience flow

    # If the script gets this far then the user input something we haven't defined
    # print(f"I don't recognize that command.")
    # do_help()
    # end runtime loop
    #--------------------