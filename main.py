
import cmd
import json
from random import randint

global char
char = False
global stats
stats = {"body", "magic"}

class prompt(cmd.Cmd):
    """
    GLOBAL PROMPT:
    - This is the primary input prompt that contains the global commands that should be available no matter where in the game the user is.
    - All of the functions in this class with "do_" prefix will be run when the user inputs their name
    - If user inputs a blank value, then the prompt does nothing and loops.
    - If another class inherits this class, then all of these functions will be available in their prompt, in addition to any functions within the child class.
    """
    prompt  = '\n: '

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
                char_magic = roster[option]["magic"]
                display_char(create_char(char_name, char_body, char_magic, False, 0, 0))
                print("--------------------------------")
            print(f'Input "login <character>" to select a character.')
            
            # VALIDATION
            if arg != "":
                print(f'{arg} is not in the roster. Please select a character that is available.')

        # CHARACTER SELECTED
        elif arg in roster:
            char_name = arg
            char_body = roster[arg]["body"]
            char_magic = roster[arg]["magic"]
            global char
            char = create_char(char_name, char_body, char_magic, False, 0, 0)
            print("--------------------------------")
            world.do_who(self, char)
            print("--------------------------------")
            global here
            here = destination("town",town)
            return True
        
    # end login()

class world(prompt):
    """Parent class for all class prompts for a character that is logged in"""

    global monster
    monster = False

    def preloop(self):
        global here

    def do_where(self, arg):
        """Display your character's current location"""
        print(f'Location: {(here.name).title()}')

    def do_who(self, arg):
        """Display your character's current stats"""
        display_char(char)

    global exits
    exits = ""
    def do_look(self, arg):
        """View the details of your current location. 
        Including anyone or anything that can be interacted with 
        as well as any locations that can be traveled to."""
        global activity
        global monster
        print("..................................")
        print(f'Location: {(here.name).title()}')
        if activity is not False:
            print(f"Activities:")
            for item in activity:
                print(" -",item)
        if monster is not False:
            print("A",monster.name,"is here.")
        print("----------------------------------")
        print("Nearby areas:",(exits).title())

    def do_attack(self, arg):
        """Attack someone or something."""
        global monster
        global char
        result = False
        if arg:
            if monster and arg == monster.name:
                enemy = monster
                print(f'You attack {(enemy.name).title()}')
                result = challenge(enemy, "body")
            else:
                print(f'There is no {arg} to attack.')
                return False
        else:
            print(f'Attack what? Pick a target with "attack <target>"')
            return False

        # Display the challenge result and deal damage
        if result == True:
            print(f'You hit the {enemy.name}!')
            enemy.wounds += 1
        elif result == False:
            print(f'The {enemy.name} hit you! OUCH!')
            char.wounds += 1
        else:
            print(f'You clashed with the {enemy.name} but neither of you were harmed.')

        ## need to replace crit code
        # # Double damage on critical hits
        # if char_roll > 2*enemy_roll:
        #     enemy.wounds += 1
        #     print(f'You overwhelm the {enemy.name}\'s defense!')
        # if 2*char_roll < enemy_roll:
        #     char.wounds += 1
        #     print(f'The {enemy.name} overwhelms your defense!')

        # Display current health when damage is dealt
        if result == False:
            print(f'You are {get_status(char.wounds)}.')
        if result == True:
            print(f'The {enemy.name} is {get_status(enemy.wounds)}.')

        # DEATH HANDLING
        wound_threshold = 5 # define how much damage kills
        if enemy.wounds >= wound_threshold:
            print(f'\n*** {(enemy.name).title()} died! ***\n')
            monster = False
            if (award_xp(enemy)):
                print(f'You gain experience!')
            world.do_look(self, False)
        if char.wounds >= wound_threshold:
            print("\n******************************")
            print(f' {(char.name).title()} died!')
            print("******************************\n")
            char = False
            global here
            here = destination("login",login)

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
        monster = False
        global activity
        activity = {"Rest at an inn","Train at the arena"}
        global exits
        exits = "Dungeon" # set exits for the do_look() in the world class
        world.do_look(self, False)
        
    def do_dungeon(self, arg):
        """Leave the town and travel to a dungeon."""
        global here
        here = destination("dungeon",dungeon)
        return True

    def do_rest(self, arg):
        """Take a rest at the inn to recuperate."""
        if char.wounds > 0:
            print(f'You were {get_status(char.wounds)}, but after resting at the inn you are all healed.')
            char.wounds = 0
        else:
            print("You rest at the inn, like a lazy good for nothing.")

    def do_train(self, arg):
        """Apply your experience to train your body and mind."""
        # The user is able to spend XP to increase their stats
        global stats

        if (char.xp < 1):
            print("While you could use the training, you need to have new experiences before you are ready to push your limits.")
        else:
            if not arg:
                print("You need to specify what stat you would like to train?")
            if arg in stats:
                char.xp -= 1
                char.__dict__[arg] += 1
                print(f'You train your {(arg).lower()} to become more powerful!')
                world.do_who(self, char)
            else:
                print("That is not something you can train. Your options are:")
                for option in stats:
                    print(" -",(option).title())

class dungeon(world):
    """Go fight monsters!"""
    def preloop(self):
        # ARRIVING: When first arriving in a new place, the preloop for this place's prompt class runs
        # 1. Establish the exits out of this place
        # 2. User sees message informing them where they arrived
        # 3. User sees message informing them where they can go from here
        global here
        global monster
        global exits
        exits = "Town" # set exits for the do_look() in the world class
        global activity
        activity = {"Search for trouble"}
        global dungeon_level
        dungeon_level = 1
        world.do_look(self, False)

    def do_town(self, arg):
        """Flee the dungeon and return to town."""
        global here
        global monster
        here = destination("town",town)
        return True

    def do_search(self, arg):
        """Search the dungeon for treasure! ...or trouble."""
        """Random chance to find: a random monster, or stairs leading deeper"""
        # No searching while monster present
        global monster
        if monster:
            print(f'You cannot search anymore until you deal with the {monster.name}.')
            return False

        # Load a random find: monster or stairs
        while monster == False:
            # Chance of finding a monster
            if (randint(0,19)):
                random_npc = randint(0,2)
                monster_list = ["slime", "skeleton", "imp"]
                monster = create_npc(monster_list[random_npc])
                print("A",monster.name,"appears!")
                return False
            # Chance of finding stairs
            else:
                print(f'You discover stairs leading deeper into the dungeon!')
                global dungeon_level
                dungeon_level += 1
                global here
                here = destination("Dungeon Level "+str(dungeon_level), dungeon)
                return False
        print(f'You find nothing.')

class create_char(object):
    """Creates a character data structure that can be called anywhere in the game"""
    def __init__(self, name, body, magic, aggro, wounds, xp):
        self.name = name
        self.body = body
        self.magic = magic
        self.aggro = aggro
        self.wounds = wounds
        self.xp = xp

def create_npc(mob):
    """Creates an NPC from the arg passed in if it matches an entry in the npc.json"""
    # 1. Create an npc based on the stats in the npc.json
    # 2. Magnify the npc stats by the current dungeon level
    with open('npc.json') as json_file:
        npcs = json.load(json_file)

    global monster
    global dungeon_level
    if mob in npcs:
        npc_name = mob
        npc_body = npcs[mob]["body"] * dungeon_level
        npc_magic = npcs[mob]["magic"] * dungeon_level
        npc_aggro = npcs[mob]["aggro"]
        return create_char(npc_name, npc_body, npc_magic, npc_aggro, 0, 0)

class destination(object):
    """This class sets the destination variable, and does so in such a way that a unique cmdloop can be called for that destination dynamically"""
    def __init__(self, name, func):
        
        # If the user is logged in as a character, then display a message when they travel to a new destination
        # If there is a monster present, let it attempt to block you from traveling
        if char:
            if monster:
                escape = challenge(monster, "body")
                if escape is False:
                    print(f'{monster.name} blocked your path to {name}!')
            print(".")
            print(".")
            print(".")
            print(f'{char.name} travels to the {name}!')
        self.name = name # title of the destination
        self.func = func # name of the cmdloop to be called

def display_char(pchar):
    # Display an individual character's stats
    # 1. Create formatting to make the stat page display all pretty
    # 2. Loop through the char data and display the relevant info
    # 3. Print wounds and xp if the user has already logged the char in
    # NOTE: print(char.__dict__) # prints the whole dictionary loaded in that var by its class
    pchar = vars(pchar)
    left_width = 10
    global stats

    for item in pchar:
        if item == "name": # name displays but is not formatted like stats
            print(((left_width-len(item))*" "),item.title(),':',pchar[item])
        if item in stats: # if the stat is a number, display it as a visual
            print(((left_width-len(item))*" "),item.title(),': [',pchar[item],"]"+(" * "*pchar[item]))

    # Only display the following with a selected character, do not display these in the login roster
    global char
    if char:
        for item in pchar:
            if (item == "xp"):
                print(" ------------------------------")
                print(((left_width-len("XP"))*" "),"XP : ",pchar[item])
            if (item == "wounds"):
                print(" ------------------------------")
                print(((left_width-len(item))*" "),item.title(),':',get_status(pchar[item]).title())
                print(left_width*" "," : [",pchar[item],"]"+(" X "*pchar[item]))

from dice import *
def challenge(enemy, stat):
    # Handle all conflicts and resolve them with dice rolls
    # 1. Define how many sides the dice will have
    # 2. Roll a number of dice for the char and the opponent equal to the value of the stat being challenged
    # 3. Take the highest roll from the char and the opponent and compare them, the highest wins
    # 4. Apply consequences for the outcome. Wound or its equivalent
    global char
    combat_dice = 100
    highest_roll = 0

    for x in range(0, char.__dict__[stat]):
        roll = dice(1,combat_dice)
        print(f' > DICE: {char.name} rolled {roll}')
        if roll > highest_roll:
            highest_roll = roll
    char_roll = highest_roll
    
    highest_roll = 0
    for x in range(0, enemy.__dict__[stat]):
        roll = dice(1,combat_dice)
        print(f' > DICE: {(enemy.name).title()} rolled {roll}')
        if roll > highest_roll:
            highest_roll = roll
    enemy_roll = highest_roll

    if char_roll > enemy_roll:
        return True
    elif enemy_roll > char_roll:
        return False
        
def get_status(damage):
    """Translates damage numbers into words"""
    wound_level = ["unwounded", "barely wounded", "lightly wounded", "moderately wounded", "very wounded", "severely wounded", "mortally wounded", "dead"]
    return wound_level[damage]

def award_xp(npc):
    """Assess if XP is warranted and apply it to the character"""
    char.xp += 1
    return True

if __name__ == '__main__':
    # START GAME: Run the initial prompt loop
    global here
    here = destination("login",login)
    while here:
        here.func().cmdloop()
