import random

def dice(number, sides):
    rolled = 0
    for x in range(number):
        rolled += random.randint(1,sides)
        # print("Rolled: ",rolled)
    return rolled

# total = dice(2,4)
# print(f'Dice Rolled: {total}')