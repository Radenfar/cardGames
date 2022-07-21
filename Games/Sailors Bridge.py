from classbase import Card, Player
import random
import os

#Start a game off by renaming the file to the name of the game with first letter capitalization

deck = []
suits = ["hearts", "spades", "diamonds", "clubs"]
numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
table = []
hidden_pile = []

for suit in suits:
    for number in numbers:
        if suit == "spades" or suit == "clubs":
            deck.append(Card(suit, number, "black"))
        else:
            deck.append(Card(suit, number, "red"))
            
game_name = os.path.splitext(os.path.basename(__file__))[0]

#startup routine
printer = "Welcome to:" + " " + game_name
print(printer)
print("-"*(len(printer)))
print("Add players: ")
print("-------------")
print("Add a player by typing their name below. Enter nothing to stop adding players.")
print("Note: For Sailors Bridge there is a maximum of 5 players.")
player_list = []
while True:
    player_name = input("-: ")
    if player_name == "" or len(player_list) == 5:
        break
    else:
        player_list.append(Player(player_name))

print("Cool! Here are your players:")
for item in player_list:
    print(item)
print("-"*20)

#Game Setup
turn_nums = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
turn_trumps = ['hearts', 'clubs', 'diamonds', 'spades', 'no trump', 'hearts', 'clubs', 'diamonds', 'spades', 'no trump', 'hearts', 'clubs', 'diamonds', 'spades', 'no trump', 'hearts', 'clubs', 'diamonds', 'spades']

for turn_num in turn_nums:
    pass

def round(player_list, turn_num, turn_trumps, deck):
    pass