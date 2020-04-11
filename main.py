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

    def do_quit(self, arg):
        """Close the program. Nothing is saved."""
        print('QUIT SCREEN')
        quit()
        # Removing this: beware this in prompt, it only ends the current prompt and enables the user to travel backwards into previous prompts
        # return True # End the current prompt loop
    
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

    def preloop(self):
        # Call this when the user first arrives in this class
        print(" -----------")
        print("| New Game!")
        print(" -----------")
        print("| - Login")
        print("| - Help")
        print("| - Quit")
        print(" -----------")

    def do_login(self, arg):
        """Display a list of characters. This command with an argument will select a character and start the game."""
        # 1. User sees the roster of characters available in the local roster.json
        # 2. User selects character from the roster
        # 3. User is navigated to town() after selecting a character

        # ROSTER FETCH:
        # 1. Grab the roster from a local json file
        # 2. Loop through the roster and display each char in it
        global roster
        with open('roster.json') as json_file:
            roster = json.load(json_file)

        # USER INPUT: CHAR SELECT
        # 1. Roster displays if the user inputs "login" without a valid char name
        # 2. If the user enters an invalid character name, send validation message
        # 3. User selects a character from the roster
        # 4. User that selected a valid character is navigated to town()        
        arg = arg.title()

        # ROSTER DISPLAY
        if arg not in roster:
            for item in roster:
                char_iteration = {}
                char_iteration[item] = roster[item]
                display_char(char_iteration)
            print(f'Input "login <character>" to select a character.')
            
            # VALIDATION
            if arg != "":
                print(f'{arg} is not in the roster. Please select a character that is available.')

        # CHARACTER SELECTED
        elif arg in roster:
            print('You have selected '+arg)
            char_name = arg
            char_body = roster[arg]["body"]
            char_speed = roster[arg]["speed"]
            char_mind = roster[arg]["mind"]
            char_heart = roster[arg]["heart"]
            global char
            char = create_char(char_name, char_body, char_speed, char_mind, char_heart)
            town().cmdloop()
        
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

class create_char(object):
    """
    Creates a character data structure that can be called anywhere in the game
    """
    def __init__(self, name, body, speed, mind, heart):
        self.name = name
        self.body = body
        self.speed = speed
        self.mind = mind
        self.heart = heart

class world(prompt):
    """Parent class for all class prompts for a character that is logged in"""


    def preloop(self):
        global here
        here = "...somewhere." #default value that hopefully will never be called. Assign this variable in every class that inherits this class

    def do_where(self, arg):
        """Display your character's current location"""
        print(f'You are {here}')

    def do_who(self, arg):
        """Display your character's current stats"""
        # print(char.__dict__) # prints the whole dictionary loaded in that var by its class
        pchar = vars(char)
        left_width = 10
        stats = {"body", "mind", "speed", "heart"}

        for item in pchar:
            if item not in stats:
                print(((left_width-len(item))*" "),item.title(),':',pchar[item])
            else: # if the stat is a number, display it as a visual
                print(((left_width-len(item))*" "),item.title(),': [',pchar[item],"]"+(" * "*pchar[item]))

class town(world):
    """
    1. After the user has selected a character in login() they arrive in the town
    2. The user sees a list of what they can do in the town
    3. Among the options available in town, is the option to leave the town and go to dungeon()
    """

    def preloop(self):
        # Call this when the user first arrives in this class
        global here
        here = "in a town."
        print(f'You arrive {here}.')

    def do_dungeon(self, arg):
        """Leave the town and travel to a dungeon."""
        dungeon().cmdloop()

class dungeon(world):
    """Go fight monsters!"""

    def preloop(self):
        global here
        here = "in a dungeon"
        print(f'You go {here}.')

    def do_town(self, arg):
        """Flee the dungeon and return to town."""
        town().cmdloop()

    def do_search(self, arg):
        """Search the dungeon for treasure! ...or trouble."""

# START GAME: Run the initial prompt loop
if __name__ == '__main__':
    login().cmdloop()
