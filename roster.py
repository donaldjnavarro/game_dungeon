import json
from prompt import prompt

def get_roster():
    # Set a roster variable based on a local json of characters
    with open('roster.json') as json_file:
        return json.load(json_file)

def display_roster():
    # Display the roster
    # 1. Grab the roster from a local json file
    # 2. Loop through the roster and display each char in it
    roster = get_roster()
    for item in roster:
        char_iteration = {}
        char_iteration[item] = roster[item]
        display_char(char_iteration)

def select_char():
    # Prompt the user to select a character
    # 1. Display the available characters
    # 2. Prompt the user to select a character
    # 3. If the user selects a valid character, end this function and return the character's data
    char = False
    roster = get_roster()
    roster_commands = False # this variable will catch the user's input that is returned from prompt()

    while char is False:
        display_roster()
        char_select = prompt("What character would you like to play? ", roster_commands).title()
        
        # User selected a valid char
        if char_select in roster:
            print("You selected",char_select)
            char = {}
            char[char_select] = roster[char_select]
            return char

def display_char(char):
    # Display an individual character's stats
    # 1. Create formatting to make the stat page display all pretty
    # 2. Loop through the char data and display the relevant info

    gap = 10 # standard indentation characters
    print("_"*gap*3) # lead each entry with a pagebreak line
    for item in char:
        character = "Character" # the object has a name with no key, so we createa fake key for print uniformity
        spacing = "|"+" "*(gap - len(character)) # uniform display right rail
        print(spacing,character+":",item) 

        for key, value in char[item].items():
            if isinstance(value, int):
                # visual_level = "|"+("*"*(value))+("-"*(4-value))+"|"
                visual_level = "["+str(value)+"] "+("* "*(value))+("  "*(5-value))
            else:
                visual_level = value
            spacing = "|"+" "*(gap - len(key)) # uniform display right rail
            print(spacing,key.title()+":",visual_level) # .title to capitalize
    print("_"*gap*3)
    
