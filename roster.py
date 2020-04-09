import json
from prompt import prompt

def get_roster():
    # since we don't need to store the roster all the time, this function will fetch it from the json on an as needed basis
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
    char = False
    roster = get_roster()
    roster_commands = False

    while char is False:
        display_roster()
        char_select = prompt("What character would you like to play? ", roster_commands).title()
        
        # for cmd in roster_commands:
        if char_select in roster:
            print("You selected",char_select)
            char = {}
            char[char_select] = roster[char_select]
            return char

def display_char(char):
    if char is False:
        print("There is no character selected.")
    else:
        # print the current loop's object name
        gap = 13 # standard indentation characters
        print("_"*gap*3) # lead each entry with a pagebreak line
        for item in char:
            character = "Character" # the object has a name with no key, so we createa fake key for print uniformity
            spacing = " "*(gap - len(character)) # uniform display right rail
            print(spacing,character+":",item) 

            for key, value in char[item].items():
                if isinstance(value, int):
                    # visual_level = "|"+("*"*(value))+("-"*(4-value))+"|"
                    visual_level = "["+str(value)+"]"+"|"+("* "*(value))+("  "*(5-value))+"|"
                else:
                    visual_level = value
                spacing = " "*(gap - len(key)) # uniform display right rail
                print(spacing,key.title()+":",visual_level) # .title to capitalize
    print("_"*gap*3)
    
