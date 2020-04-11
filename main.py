import cmd
import json

class prompt(cmd.Cmd):
    """
    GLOBAL PROMPT:
    - This is the primary input prompt that contains the global commands that should be available no matter where in the game the user is.
    - All of the functions in this class with "do_" prefix will be run when the user inputs their name
    - If user inputs a blank value, then the prompt does nothing and loops.
    - If another class inherits this class, then all of these functions will be available in their prompt, in addition to any functions within the child class.
    """
    prompt  = ': '

    def do_help(self, arg):
        print('HELP SCREEN')

    def do_quit(self, arg):
        print('QUIT SCREEN')
        return True # End the current prompt loop
    
    def emptyline(self):
        # When the user presses enter without typing anything
        # return cmd.Cmd.emptyline(self) # this will repeat the last entered command
        return False # Take no action and load a new prompt

    # end prompt() This location is reached the first time the prompt is launched

class login(prompt):
    # LANDING PAGE: This is the initial page the user lands on
    # 1. Inherit Quit and Help options from the prompt() class
    # 2. Login option provides interface for selecting a character from a local json file
    # 3. After selecting a character the user is navigated to the town() class

    # ROSTER
    global roster
    with open('roster.json') as json_file:
        roster = json.load(json_file)

    def do_login(self, arg):
        # LOGIN FLOW:
        #   Display the roster of characters
        #   Start a prompt loop that accepts 

        arg = arg.title()
        print('You have selected '+arg)

    def do_roster(self, arg):
        # Display the roster
        # 1. Grab the roster from a local json file
        # 2. Loop through the roster and display each char in it
        for item in roster:
            char_iteration = {}
            char_iteration[item] = roster[item]
            display_char(char_iteration)
    # end login()

def display_char(char):
    # Display an individual character's stats
    # 1. Create formatting to make the stat page display all pretty
    # 2. Loop through the char data and display the relevant info
    # NOTE: Sorry I handled the sizes of the gaps all willy nilly and just made them work :/ probably should revisit this and make the math use uniform variables based on intended total page width

    gap = 9 # standard indentation characters
    border = " "+("-"*gap*3)
    print(border) # lead each entry with a pagebreak line
    for item in char:
        character = "Character" # the object has a name with no key, so we createa fake key for print uniformity
        spacing = "|"+" "*(gap - len(character)) # uniform display right rail
        rightrail = ((14-len(str(item)))*" ")+"|"
        print(spacing,character+":",item,rightrail) 
        print(" "+("-"*gap*3))

        for key, value in char[item].items():
            if isinstance(value, int):
                visual_level = "["+str(value)+"] "+("* "*(value))+("  "*(5-value))
                rightrail = ((4-len(str(value)*3))*" ")+"|"
            else:
                visual_level = value
                rightrail = ((15-len(str(value)))*" ")+"|"
            spacing = "|"+" "*(gap - len(key)) # create indent to align text right
            print(spacing,key.title()+":",visual_level+rightrail) # .title to capitalize
    print(border+"\n")
# end display_char()

# Run the prompt loop
login().cmdloop()