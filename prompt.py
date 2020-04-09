import sys

def prompt(display_text="",activated_commands=False):
    # PRIMARY COMMANDLINE INTERFACE
    # 1. Optional argument of a string that it will display to the user above the text prompt
    # 2. Optional argument of an object of commands to set as "active" in addition to the default universal commands
    # 3. PROMPT: Accept user text input
    # 4. RUN UNIVERSAL COMMANDS: the "action" function listed in the command_list object if input matches the "commands" of universal_commands
    # 5. RUN ACTIVE COMMANDS: the "action" function listed in the command_list object if input matches the "commands" of active_commands
    #
    # Note: Commands have an "action_arg" key that provides the option for an argument to pass to the function that is run when that command is called
    #    This is needed in order to pass char data around. Currently we have conditionals checking for this argument
    #    before we know how to phrase the syntax of the command's action. Hopefully we can find a cleaner way to do this in the future


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
            "action": do_quit,
            # "action_arg": False
        }
    command_list["universal"]["quit"] = quit_commands

    # UNIVERSAL HELP COMMANDS
    help_commands = {
            "title": "Help Screen",
            "commands": {'help', 'h'},
            "action": do_help,
            # "action_arg": False
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

        # TRY ACTIVE COMMANDS: None of the universal commands were matched, so check the active commands next
        if command_list["active"] == False: # if the prompt was sent without active commands, and input didnt match universal, then send the user's input back to the function that called this prompt
            return command
        else: # if active command options were sent with this prompt, check the user input against them 
            for cmd in command_list["active"]:
                if command in command_list["active"][cmd]["commands"]:
                    if command_list["active"][cmd]["action_arg"] != False:
                        active_response = command_list["active"][cmd]["action"](command_list["active"][cmd]["action_arg"])
                    else:
                        active_response = command_list["active"][cmd]["action"]()
                    if active_response != False:
                        return active_response
    
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

def do_help():
    splash("Help Screen: The commands that are currently available are listed below")

    splash("Universal Commands:")
    for cmd in command_list["universal"]:
        print("-",command_list["universal"][cmd]["title"],":",command_list["universal"][cmd]["commands"])

    if command_list["active"] != False:
        splash("Currently Active Commands:")
        for cmd in command_list["active"]:
            print("-",command_list["active"][cmd]["title"],":",command_list["active"][cmd]["commands"])

    input("\n(Press enter to return to the previous screen)") # just pause and require enter before returning to prompt

def do_quit():
    splash("Quit Screen")
    verify_quit = input(f"Are you sure you want to quit?\nQuit? [yes/no] ")

    if verify_quit == "yes":
        splash("GOOD BYE")
        quit()

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
                "action": select_char,
                "action_arg": False
            }
        }
        # print the login options that are available
        for item in login_commands:
            print("-",login_commands[item]["title"])
        
        # prompt the user to choose from the login options
        login_selection = prompt("Make a selection", login_commands)
        if login_selection != False:
            return login_selection

def display_stats(char):
    splash("You are playing:")
    display_char(char)