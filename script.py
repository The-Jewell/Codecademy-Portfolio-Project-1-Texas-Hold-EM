import random

#create the deck
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [{'value': v, 'suit': s} for s in suits for v in values]
    random.shuffle(deck)
    return deck

def initialize_game():
    deck = create_deck() # create and shuffle deck 
    player_chips = 100
    computer_chips = 100 
    min_bet = 10
    return deck, player_chips, computer_chips, min_bet

def deal_cards(deck, number):
    hand = deck[:number]
    del deck[:number]
    return hand, deck

#initialize the game 
deck, player_chips, computer_chips, min_bet = initialize_game()

#deal two cards to player and the computer
player_hand, deck = deal_cards(deck, 2)
computer_hand, deck = deal_cards(deck, 2)

#print player hand and chip count 
print("Your hand:", player_hand)
print("Your chip count:", player_chips)

def player_bet(chips, min_bet):
    print("The minimum bet is $10")
    print(f"Your chip count: ${chips}")
    bet = input("Enter 'call' to place minimum bet, 'raise' to increase the bet, 'all in' to bet everything, or 'fold' to fold your hand:").lower()

    if bet =='call':
        bet_amount = min_bet
    elif bet == 'raise':
        if chips > min_bet:
            raise_amount = int(input(f"Enter your raise amount(must be between $10 and ${chips - min_bet}): "))
            bet_amount = min_bet + raise_amount
            if bet_amount > chips:
                print("Raise amount is too high, you are going all in.")
                bet_amount = chips
        else:
            print("Not enough chips to raise, calling instead.")
            bet_amount = min_bet
    elif bet == 'all in':
        bet_amount = chips
    elif bet == 'fold':
        return 0, 'fold'
    else:
        print("Invalid input. Defaulting to call.")
        bet_amount = min_bet
    return bet_amount, 'continue'

#player places a bet 
player_bet_amount, game_status = player_bet(player_chips, min_bet)
if game_status == 'fold':
    print("You have folded.")
else:
    player_chips -= player_bet_amount
    print(f"You bet ${player_bet_amount}. You have ${player_chips} left.")


def computer_bet(computer_chips, player_bet_amount, min_bet):
    #comp decision based on random choice
    actions = ['call', 'raise', 'fold']
    action = random.choice(actions)

    if action == 'call':
        bet_amount = player_bet_amount
        if bet_amount > computer_chips:
            bet_amount = computer_chips # all in when not enough chips
        print("Computer Calls")
    elif action == 'raise':
        if computer_chips > player_bet_amount + min_bet:
            bet_amount = player_bet_amount + min_bet
            print(f"Computer raises to ${bet_amount}.")
        else:
            bet_amount == computer_chips
            print("Computer goes all in.")
    elif action == 'fold':
        bet_amount = 0
        print("Computer folds.")

    return bet_amount, action

#example of a betting round
player_bet_amount, player_status = player_bet(player_chips, min_bet)
if player_status != 'fold':
    computer_chips -= player_bet_amount
    computer_bet_amount, computer_status = computer_bet(computer_chips, player_bet_amount, min_bet)
    if computer_status != 'fold':
        computer_chips -= computer_bet_amount
    else:
        #handle what happens when computer folds
        pass
else:
    #handle what happens when player folds
    pass

#after initial betting round 
if player_status != 'fold' and computer_status != 'fold':
    #deal flop
    flop, deck = deal_cards(deck, 3)
    print("Flop:", flop)
    #betting round for flop
    #repeat for turn and river 

#determine winner 
#award pot 
#ask for new game or end 