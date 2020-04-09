import sys

def prompt(display_text="",activated_commands={"": {"title": "","commands": "","action": ""}}):
    # This function receives an option argument of a string that it will display to the user above the text prompt
    # Then it accepts a text input command from the user
    # Then it checks the text input against universal commands that are always accepted
    # Then it returns the text input to whatever called this function, so that whatever called this can do its own handling of the user input

    #----------------------------
    # VALID COMMANDS: Create lists of possible commands that the prompt will respond to
    global command_list
    command_list = {}

    #----------------------------
    # ACTIVE COMMANDS: Set the commands that are currently active based on the arg passed into the function. These are in addition to Universal Commands.
    command_list["active"] = activated_commands

    #----------------------------
    # UNIVERSAL COMMANDS
    # Create a list of universal commands that the prompt will respond to everywhere in the user flow
    universal_commands = {}
    command_list["universal"] = universal_commands

    # UNIVERSAL QUIT COMMANDS
    quit_commands = {
            "title": "Quit Game",
            "commands": {'quit', 'exit', 'q', 'end'},
            "action": do_quit
        }
    command_list["universal"]["quit"] = quit_commands

    # UNIVERSAL HELP COMMANDS
    help_commands = {
            "title": "Help Screen",
            "commands": {'help', 'h'},
            "action": do_help
            }
    command_list["universal"]["help"] = help_commands
    # /end commands
    #----------------------------
    
    prompting = True
    while prompting is True:
        # PROMPT DISPLAY
        command = input(f"\n{display_text}\n:").lower()

        # TRY UNIVERSAL COMMANDS: Check the list of universal commands and run those first
        for cmd in command_list["universal"]:
            if command in command_list["universal"][cmd]["commands"]:
                command_list["universal"][cmd]["action"]()
                return command

        # TRY ACTIVE COMMANDS: None of the universal commands were matched, so check the active commands next
        for cmd in command_list["active"]:
            if command in command_list["active"][cmd]["commands"]:
                command_list["active"][cmd]["action"]()
                return command
    
def splash(splash_text):
    # Add some pretty framing to some text
    # The number of underscores used should equal the length of the text being used (with slight overhang)
    frame = "_" * (len(splash_text)+3)
    # Print the text frames in underscores
    print(f"\n{frame}\n\n {wordwrap(splash_text)}\n{frame}")

def wordwrap(to_wrap):
    # TODO: Add logic to clip strings and wrap them when they exceed a certain length
    # TODO: Add an optional argument to this function that clips the end of a string and does NOT wordwrap it, to create a max length for framing graphics etc
    wrapped = to_wrap
    return wrapped

def do_universal_command(command):
    #----------------------
    # UNIVERSAL COMMANDS
    # The following commands are "universal" and will be accepted no matter where in the program the user is at
    # (In other words, no matter what is calling this prompt() function, these will be considered valid commands that take priority
    # before returning the user's input to be evaluated by whatever called this prompt function)
    if command in command_list["universal"]["help"]["commands"]:
        do_help()
        return True  
    if command in command_list["universal"]["quit"]["commands"]:
        do_quit()
        return True
    return False

def do_active_command(command):
    if command in command_list["active"]:
        print("DO AN ACTIVE COMMAND")

def do_help():
    splash("Help Screen: The commands that are currently available are listed below"
    )

    splash("Universal Commands:")
    for cmd in command_list["universal"]:
        print("-",command_list["universal"][cmd]["title"],":",command_list["universal"][cmd]["commands"])

    splash("Currently Active Commands:")
    for cmd in command_list["active"]:
        print("-",command_list["active"][cmd]["title"],":",command_list["active"][cmd]["commands"])

    input("\n(Press enter to return to the previous screen)") # just pause and require enter before returning to prompt

def do_quit():
    splash("Quit Screen")
    try:
        verify_quit = input(f"Are you sure you want to quit?\nQuit? [yes/no] ")
    except:
        print(' VALIDATION ERROR: That is not a valid selection!')
        prompt('Try again')

    if verify_quit == "yes":
        splash("GOOD BYE")
        quit()
    # Cancel quit for any input except the positive case defined above. Just catch all the possible commands jic
    else:
        prompt()

def do_login():
    from roster import select_char

    login = True
    
    while login is True:
        splash("Login Screen")

        # Create a list of commands that are only available in the login login screen
        login_commands = { # note these display in reverse order
                "charselect": {
                    "title": "Character Select Roster",
                    "commands": {"char", "charselect", "roster", "select", "character"},
                    "action": select_char
                }
            }

        for item in login_commands:
            print("-",login_commands[item]["title"])
        login_selection = prompt("Make a selection", login_commands)