import random

#create the deck
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [{'value': v, 'suit': s} for s in suits for v in values]
    random.shuffle(deck)
    return deck

#log to test deck creation
#deck = create_deck()
#print(deck)