from classbase import Card, Player
import random
import os
import time
from tabulate import tabulate

deck = []
suits = ["hearts", "spades", "diamonds", "clubs"]
numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
table = []

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
player_list = []
while True:
    player_name = input("-: ")
    if player_name == "":
        break
    else:
        player_list.append(Player(player_name))

print("Cool! Here are your players:")
for item in player_list:
    print(item)

#game set up
random.shuffle(deck)
i = 0
for item in deck:
    player_list[i].add_card(item)
    if i == (len(player_list) - 1):
        i = 0
    else:
        i += 1

#turn functions
def hand_info(player):
    print("Cards in your hand:")
    i = 0
    for item in player.show_hand():
        print(str(i) + ":" + "    " + str(item))
        i += 1

def show_pile(table):
    print("Current pile on the table:")
    num = 0
    for placement in table:
        num += len(placement)
    print("." * num)

def show_players(player_list):
    i = 0
    for item in player_list:
        print(str(i) + "    " + str(item))
        i += 1

def cheat_claim(player_list, last_player, recent_claim, table, last_player_index):
    print("Who is making the claim against " + str(last_player) + "?")
    show_players(player_list)
    while True:
        player_claiming_index = input("-: ")
        if player_claiming_index.isdigit() == True and int(player_claiming_index) >= 0 and int(player_claiming_index) < len(player_list) and int(player_claiming_index) != last_player_index:
            player_claiming = player_list[int(player_claiming_index)]
            break
        else:
            print("Not a valid player input")
    #check to see if it is true
    actual = table[-1]
    names = []
    for actual_card in actual:
        names.append(str(actual_card))
    values = []
    for name in names:
        name_list = name.split(" ")
        values.append(name_list[0])
    claimed_value = str(recent_claim[1])
    did_cheat = False
    for value in values:
        if value != claimed_value:
            did_cheat = True
    if len(values) != int(recent_claim[0]):
        did_cheat = True
    print("-"*20)
    print("That was ", did_cheat)
    print("-"*20)
    #if did cheat, add table to their hand, if not, add table to claimant's hand
    if did_cheat == True:
        cards_to_add = []
        for placement in table:
            for item in placement:
                cards_to_add.append(item)
        for item in cards_to_add:
            last_player.add_card(item)
    else:
        cards_to_add = []
        for placement in table:
            for item in placement:
                cards_to_add.append(item)
        table.clear()
        return player_claiming.hand.extend(cards_to_add)
    table.clear()
    show_pile(table)

def turn(cur_player, table, recent_claim, last_player, player_list, last_player_index):
    show_pile(table)
    print("You have ten seconds to hide your screen!")
    #time.sleep(10)
    print(str(cur_player) + " begin your turn.")
    hand_info(player_list[0])

#turns begin
#initialisation turn:
print("NOTE: FOR EVERY TURN YOU WILL HAVE 10 SECONDS TO PASS OVER SO YOU DONT SEE EACHOTHER'S CARDS")
print("-"*20)
print(player_list[0], "begins the game:")
print("You have 10 seconds to hide your screen!")
print("-"*20)
#time.sleep(10)
print("Your hand: ")
hand_info(player_list[0])
print("You may now enter the cards you want to place down, keep entering card numbers or enter nothing to stop adding.")
cards_in_motion = []
cards_in_motion_strings = []
indexes_used = []
while True:
    print(cards_in_motion_strings)
    card_input = input("-: ")
    if len(indexes_used) == 4:
        break
    if card_input == "" and len(indexes_used) > 1:
        break
    elif card_input.isdigit() == True and int(card_input) <= player_list[0].get_hand_size():
        cards_in_motion_strings.append(str(player_list[0].hand[int(card_input)]))
        cards_in_motion.append(player_list[0].hand[int(card_input)])
        indexes_used.append(int(card_input))
    else:
        print("That was not a valid input.")
print("Now you will decide what you are going to claim you are putting down.")
while True:
    claim_num = input("Enter the number of cards you claim: ")
    if claim_num.isdigit() == True and int(claim_num) <= player_list[0].get_hand_size() and int(claim_num) > 0:
        break
    else:
        print("That was not a valid number of cards.")
while True:
    claim_value = input("Enter value (1, 2, Jack) you claim: ")
    if claim_value in numbers:
        break
    else:
        print("That was not a valid value of card, please capitalize the first letter if a picture card.")

indexes_used.sort(reverse=True) #DO NOT FORGET TO SORT LIKE THIS, OR YOU WILL END UP WITH INDEX POPPING ISSUES LIKE IN HOI4 <---------------------------------------------------------------------------
for index in indexes_used:
    player_list[0].remove_card(index)

table.append(cards_in_motion)

recent_claim = [claim_num, claim_value]
last_player_index = 0

#after initialisation turn, will have to do turns player by player until a win is found
win_check = False
cur_player_index = 1
while win_check == False:
    cur_player = player_list[cur_player_index]
    last_player = player_list[last_player_index]
    #first checks if they want to do a cheat check
    print("\n"*200)
    show_pile(table)
    print(str(last_player) + " claimed they put down " + str(recent_claim[0]) + " " + str(recent_claim[1]) + "'s.")
    print("Does anyone want to call a cheat on the last round?")
    print("'1' - Yes")
    print("'2' - No")
    while True:
        claim_check = input("-: ")
        if claim_check == "1":
            cheat_claim(player_list, last_player, recent_claim, table, last_player_index)
            break
        elif claim_check == "2":
            break
        else:
            print("That was not a valid input")
    #once cheat check is over with, do a turn
    turn(cur_player, table, recent_claim, last_player, player_list, last_player_index)
    #update index of current player at the end of the turn cycle
    if cur_player_index == (len(player_list) - 1):
        cur_player_index = 0
    else:
        cur_player_index += 1
    #update index of last player value
    if last_player_index == (len(player_list) - 1):
        last_player_index = 0
    else:
        last_player_index += 1
    #check for win
    for person in player_list:
        if len(person.show_hand()) == 0:
            winner = str(person)
            win_check = True
            break

#final line
#print(winner + " won!!!")
