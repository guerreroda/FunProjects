# ========================
# The parameters
NPlayers = 4
simulations = 10000

# Test the whole deck (True) or a set of cards (False)
many = True

# If testing a set of cards:
# Fill the value of the cards
V0, V1 = 14, 10
# Suited (1) or odd (0) cards 
suited = 1
# Position of the player.
tested_player = 0

# ========================


# ========================
# ========================
# The Code
# ========================
# ========================

data = []

import random
import pandas as pd

while True:
    try:
        NPlayers = int(NPlayers)
        while NPlayers < 2 :
            NPlayers = input('Define Number of players? (More than 1)')
            if NPlayers is int and NPlayers>1 : break
    except :
        print("Introduce a number.")
        NPlayers = input('Define Number of players? (More than 1)')
        continue
    else:
        break

# ========================
# Player Order.
# (Not used)
# The initial order is {turn : player}
position = dict()
# Assign each turn a player.
for x in list(range(0, NPlayers,1)) : position[x] = x

# Basically, take the current turn and substract one (t = 0 is first)
# If the current position is 0, assign the last position
def new_position(current_position) :
    position[x] = position[x]-1 if position[x]>0 else NPlayers-1

# ========================
# The Cards.
# Cards are an object with a value and color.
class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

# To show cards, print their value and suit
def show(h) :
    openhand = []
    if isinstance(h,list) :
        for x in h : openhand.append((x.value, x.color))
    else :  openhand = (h.value, h.color)
    return openhand

# To test the relative value of particular cards, we create them:
def makecard(string) :
    if len(string) == 3 :
        value, suit = string[0:2] , string[2:3]
    if len(string) == 2 :
        value, suit = string[0:1], string[1:2]
    if suit == "d" : suit = "diamonds"
    if suit == "c" : suit = "cubs"
    if suit == "h" : suit = "hearts"
    if suit == "s" : suit = "spades"

    return Card(int(value),suit)

# ========================
# The Value of Hands

# Royal Flush.
def is_royal(Cards, royal=False) :
    # Get a list with the color of all cards with value larger than 9 
    matched = [x.color for x in Cards if x.value > 9]
    # Count there are 5 suited cards.
    if len(matched) > 0 and matched.count(matched[0]) == 5 : royal = True
    return royal

# Pairs: Return the number of pairs.
# Warning: Three of a Kind and Four of a Kind count as pairs.
def is_pairs(Cards, pairs=0) :
    Cards = [ x.value for x in Cards ]
    for item in Cards :
        if len( [x for x in Cards if x==item] ) > 1 :
            Cards = [ x for x in Cards if x != item ]
            pairs = pairs+1
    return pairs

def is_three(Cards, three=False) :
    Cards = [ x.value for x in Cards ]
    for i in Cards :
        if sum([ x == i for x in Cards ]) == 3 : three = True
    return three

def is_four(Cards, four=False) :
    Cards = sorted([ x.value for x in Cards ])
    for i in Cards :
        if sum([ x == i for x in Cards ]) == 4 : four = True
    return four

# For Full you need at least 2 pairs (one is 3 of a kind) and a three of a kind.
def is_full(Cards, full=False) :
    if is_pairs(Cards) > 1 and is_three(Cards) : full = True
    return full

def is_suited(Cards,suited = False) :
    # To check if they are suited, find 5 cards of more of the same suit.
    for color in ["hearts", "diamonds", "clubs", "spades"] :
        if sum([ x.color == color for x in Cards ])>4 : suited = True
    return suited

def is_straight(Cards, straight=False) :
    # Only values are needed.
    Cards = sorted([ x.value for x in Cards ])
    for r in range(3) :
        if set( list( range(Cards[r],Cards[r]+5) ) ) <= set(Cards) : straight = True
    # Test wheel
    if straight == False and 14 in Cards and set( list( range(2,6) ) ) <= set(Cards) : straight = True
    return straight

def is_straigh_flush(Cards, straight_flush=False) :
    # find the state
    C = sorted([ x.value for x in Cards ])
    for r in range(3) :
        # Identify the straight
        progression = list( range(C[r],C[r]+5) )
        if set( progression ) <= set(C) :
            # If the progression is in the hand, check the colors are the same for all cards
            for color in ["hearts", "diamonds", "clubs", "spades"] :
                if len([ x.value for x in Cards if x.color == color and x.value in progression ])>4 :
                    straight_flush = True
    return straight_flush

# Value of hand and tabl:
# Takes the hand and table.
# Returns the value and high card.
def value(Hand, Table) :
    ##########################
    # Find the highest value first:
    Cards = Hand + Table
    result = { "Value" : 0, "Hand": "High Card", "High": max([Hand[0].value, Hand[1].value]) }
    
    if is_royal(Cards) : result["Value"] = 10; result["Hand"] = "Royal Flush"
    elif is_straigh_flush(Cards) : result["Value"] = 9; result["Hand"] = "Straight Flush"
    elif is_four(Cards) : result["Value"] = 8 ; result["Hand"] = "Four of a kind"
    elif is_full(Cards) : result["Value"] = 7 ; result["Hand"] = "Full House"
    elif is_suited(Cards) : result["Value"] = 6; result["Hand"] = "Flush"
    elif is_straight(Cards) : result["Value"] = 5; result["Hand"] = "Straight"
    elif is_three(Cards) : result["Value"] = 4; result["Hand"] = "Three of a kind"
    elif is_pairs(Cards) > 0 : result["Value"] = is_pairs(Cards); result["Hand"] = "Pairs"
        
    return result

# ========================
# Testing Hand
# Makes the cards to test their odds.

def hand_tester(Value1=None, Value2=None, suit=None, deck=None) :
    if Value1==Value2 : suit=0
    try :
        if suit == 1 : card1 = "d"; card2 = "d"
        elif suit == 0 : card1 = "d"; card2 = "s"
        tested_hand = makecard(str(Value1) + card1), makecard(str(Value2) + card2)
    except : tested_hand = None
    return tested_hand

# ========================
# The Dealer
# A function that takes a desk, assigns hands, and discovers the table.
# If there is a hand tested, the dealer removes those cards from the deck.

def dealer(deck, NPlayers, tested_hand = None, tested_player = 0) :
    last_card = 0
    # give each player a hand
    hands = dict()
    if tested_hand is not None :
        for x in deck :
            if (( x.value == tested_hand[0].value )&( x.color == tested_hand[0].color )) : deck.remove(x)
            if (( x.value == tested_hand[1].value )&( x.color == tested_hand[1].color )) : deck.remove(x)
    for player in list(range(0, NPlayers,1)) :
        if tested_hand is not None and player == tested_player : hands[tested_player] = [ tested_hand[0] , tested_hand[1] ]
        else :
            hands[player] = [deck[last_card], deck[last_card+1] ]
            # Define the last card in the table
            last_card = deck.index( hands[player][1] ) + 1

    # Fill the table with 5 cards
    table = []
    for x in range(1,6) : table.append(deck[last_card]); last_card = last_card + x
    
    return hands, table, last_card

# ========================
# ========================
# The Game.
# Run N simulations were decks are created and shuffled.
# Create the hand of interest (or none.
# Deals.
# Creates standings of winners.
# And assigns value to define the winners.
# ========================

if many == False :
    for simul in range(0, simulations) :
        print(simul)
        # Make the deck
        deck = [Card(value, color) for value in range(2, 15) for color in ["hearts", "diamonds", "clubs", "spades"]]
        # randomly shuffle the deck
        random.shuffle(deck)

        # Deal hands
        new_hand = hand_tester(V0, V1, suited, deck)
        # new_hand = None
        hands, table, last = dealer(deck, NPlayers, tested_hand = new_hand)

        # Define winner, draw, or loss
        standings = dict()
        for player, hand in hands.items() : standings[player] = value(hands[player],table)['Value']
        winners = [player for player, v in standings.items() if v == max( standings.values()) ]

        # Tie-Breaker with high Card
        if len(winners) > 1 :
            standings = dict()
            for player in winners : standings[player] = value(hands[player],table)['High']
            winners = [player for player, v in standings.items() if v == max( standings.values()) ]

        if tested_player in winners and len(winners)==1 : result = 1
        elif tested_player in winners and len(winners)>1 : result = 0.5
        elif tested_player not in winners : result = 0

        results = {
            'card1' : V0 ,
            'card2' : V1 ,
            'suited' : suited ,
            'result' : result ,
            'N' : simul
        }

        data.append(results)



if many == True :
    for x in range(2,15) :
        for y in  range(2,15) :
            if x >= y : V0, V1 = x, y
            else : continue
            print(x,y)
            for s in range(0,2) :
                suited = s
                V0, V1 = x, y
                tested_player = 0
                for simul in range(0, simulations+1) :

                    # Make the deck
                    deck = [Card(value, color) for value in range(2, 15) for color in ["hearts", "diamonds", "clubs", "spades"]]
                    # randomly shuffle the deck
                    random.shuffle(deck)

                    # Deal hands
                    new_hand = hand_tester(V0, V1, suited, deck)
                    # new_hand = None
                    hands, table, last = dealer(deck, NPlayers, tested_hand = new_hand)

                    # Define winner, draw, or loss
                    standings = dict()
                    for player, hand in hands.items() : standings[player] = value(hands[player],table)['Value']
                    winners = [player for player, v in standings.items() if v == max( standings.values()) ]

                    # Tie-Breaker with high Card
                    if len(winners) > 1 :
                        standings = dict()
                        for player in winners : standings[player] = value(hands[player],table)['High']
                        winners = [player for player, v in standings.items() if v == max( standings.values()) ]

                    if tested_player in winners and len(winners)==1 : result = 1
                    elif tested_player in winners and len(winners)>1 : result = 0.5
                    elif tested_player not in winners : result = 0

                    results = {
                        'card1' : V0 ,
                        'card2' : V1 ,
                        'suited' : suited ,
                        'result' : result ,
                        'N' : simul,
                        'position' : tested_player,
                        'Players' : NPlayers
                    }

                    data.append(results)

df = pd.DataFrame(data)
df = df.groupby(['card1',"card2","suited"]).mean()
df.to_csv("simulations.csv")
