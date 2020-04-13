
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

    # end prompt() 

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
            for option in roster:
                char_name = option
                char_body = roster[option]["body"]
                char_speed = roster[option]["speed"]
                char_mind = roster[option]["mind"]
                char_heart = roster[option]["heart"]
                pchar = create_char(char_name, char_body, char_speed, char_mind, char_heart)
                display_char(pchar)
                print("--------------------------------")

            print(f'Input "login <character>" to select a character.')
            
            # VALIDATION
            if arg != "":
                print(f'{arg} is not in the roster. Please select a character that is available.')

        # CHARACTER SELECTED
        elif arg in roster:
            char_name = arg
            char_body = roster[arg]["body"]
            char_speed = roster[arg]["speed"]
            char_mind = roster[arg]["mind"]
            char_heart = roster[arg]["heart"]
            global char
            char = create_char(char_name, char_body, char_speed, char_mind, char_heart)
            # print stats
            world.do_who(self, char)
            print()
            global here
            here = destination("town",town)
            return True
        
    # end login()

class world(prompt):
    """Parent class for all class prompts for a character that is logged in"""

    def preloop(self):
        global here

    def do_where(self, arg):
        """Display your character's current location"""
        print(f'Location: {(here.name).title()}')

    def do_who(self, arg):
        """Display your character's current stats"""
        display_char(char)

    def do_test(self, arg):
        test()

    global exits
    exits = ""
    def do_look(self, arg):
        if monster:
            print("A",monster.name,"is here.")
        print("Nearby areas:",(exits).title())

class town(world):
    """
    1. After the user has selected a character in login() they arrive in the town
    2. The user sees a list of what they can do in the town
    3. Among the options available in town, is the option to leave the town and go to dungeon()
    """

    def preloop(self):
        # ARRIVING: When first arriving in a new place, the preloop for this place's prompt class runs
        # 1. Establish the exits out of this place
        # 2. User sees message informing them where they arrived
        # 3. User sees message informing them where they can go from here
        global here
        global monster
        monster = ""
        global exits
        exits = "dungeon" # set exits for the do_look() in the world class
        print(f'You arrive in {here.name}.')
        print()
        print (f'Nearby areas:',exits.title())

    def do_dungeon(self, arg):
        """Leave the town and travel to a dungeon."""
        global here
        here = destination("dungeon",dungeon)
        return True

class dungeon(world):
    """Go fight monsters!"""
    def preloop(self):
        # ARRIVING: When first arriving in a new place, the preloop for this place's prompt class runs
        # 1. Establish the exits out of this place
        # 2. User sees message informing them where they arrived
        # 3. User sees message informing them where they can go from here
        global here
        global monster
        monster = ""
        global exits
        exits = "town" # set exits for the do_look() in the world class
        print(f'You go into the {here.name}.')
        print(f'')
        print(f'Nearby areas:',exits.title())
        print(f'...Or you can <search> for trouble')

    def do_town(self, arg):
        """Flee the dungeon and return to town."""
        global here
        here = destination("town",town)
        return True

    def do_search(self, arg):
        """Search the dungeon for treasure! ...or trouble."""
        global monster
        monster = create_char("slime",1,1,1,1)
        print("A",monster.name,"appears!")


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

class destination(object):
    """This class sets the destination variable, and does so in such a way that a unique cmdloop can be called for that destination dynamically"""
    def __init__(self, name, func):
        self.name = name # title of the destination
        self.func = func # name of the cmdloop to be called

def display_char(char):
    # Display an individual character's stats
    # 1. Create formatting to make the stat page display all pretty
    # 2. Loop through the char data and display the relevant info
    # NOTE: Sorry I handled the sizes of the gaps all willy nilly and just made them work :/ probably should revisit this and make the math use uniform variables based on intended total page width
    # NOTE: print(char.__dict__) # prints the whole dictionary loaded in that var by its class
    pchar = vars(char)
    left_width = 10
    stats = {"body", "mind", "speed", "heart"}

    for item in pchar:
        if item not in stats:
            print(((left_width-len(item))*" "),item.title(),':',pchar[item])
        else: # if the stat is a number, display it as a visual
            print(((left_width-len(item))*" "),item.title(),': [',pchar[item],"]"+(" * "*pchar[item]))

if __name__ == '__main__':
    # START GAME: Run the initial prompt loop
    global here
    here = destination("login",login)

    while here:
        here.func().cmdloop()

