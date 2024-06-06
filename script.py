import random
from treys import Card, Deck, Evaluator

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

#player betting logic 
def player_bet(chips, min_bet):
    if chips == 0:
        print("You are all in. No further betting is possible.")
        return 0, 'all_in'
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

#computer betting logic
def computer_bet(computer_chips, player_bet_amount, min_bet):
    if computer_chips == 0:
        print("Computer is all in. No further betting is possible.")
        return 0, 'all_in'
    #comp decision based on random choice
    actions = ['call', 'raise', 'fold']
    action = random.choice(actions)

    if action == 'call':
        bet_amount = player_bet_amount
        if bet_amount > computer_chips:
            bet_amount = computer_chips # all in when not enough chips
        print("Computer Calls.")
    elif action == 'raise':
        if computer_chips > player_bet_amount + min_bet:
            bet_amount = player_bet_amount + min_bet
            print(f"Computer raises to ${bet_amount}.")
        else:
            bet_amount = computer_chips
            print("Computer goes all in.")
    elif action == 'fold':
        bet_amount = 0
        print("Computer folds.")
    return bet_amount, 'continue'

#betting round logic 
def betting_round(deck, player_chips, computer_chips, min_bet):
    player_bet_amount, player_status = player_bet(player_chips, min_bet)
    if player_status == 'fold':
        print("Player folds. Computer wins the round.")
        return 0, player_chips, computer_chips + player_bet_amount, 'end_round'  # Ensure chips are updated and round ends

    computer_bet_amount, computer_status = computer_bet(computer_chips, player_bet_amount, min_bet)
    if computer_status == 'fold':
        print("Computer folds. Player wins the round.")
        return 0, player_chips + computer_bet_amount, computer_chips, 'end_round'  # Ensure chips are updated and round ends

    pot = player_bet_amount + computer_bet_amount
    player_chips -= player_bet_amount
    computer_chips -= computer_bet_amount
    return pot, player_chips, computer_chips, 'continue'


def deal_community_cards(deck, count):
    community_cards, deck = deal_cards(deck, count)
    print(f"Community Cards: {community_cards}")
    return community_cards, deck

def determine_winner(player_hand, computer_hand, community_cards):
    evaluator = Evaluator()
    
    # Convert hand and community cards from string to card format
    player_hand_cards = [Card.new(card) for card in player_hand]
    computer_hand_cards = [Card.new(card) for card in computer_hand]
    community_cards = [Card.new(card) for card in community_cards]

    # Evaluate hands
    player_score = evaluator.evaluate(community_cards, player_hand_cards)
    computer_score = evaluator.evaluate(community_cards, computer_hand_cards)

    # Lower score indicates a better hand
    if player_score < computer_score:
        return 'player'
    elif player_score > computer_score:
        return 'computer'
    else:
        return 'tie'


def play_again():
    answer = input("Do you want to play another hand? (yes/no): ").lower()
    return answer == 'yes'

def main():
    deck, player_chips, computer_chips, min_bet = initialize_game()
    game_on = True

    while game_on:
        player_hand, deck = deal_cards(deck, 2)
        computer_hand, deck = deal_cards(deck, 2)
        print("Your hand:", player_hand)
        print("Your chip count:", player_chips)

        # Initial betting round
        pot, player_chips, computer_chips, game_status = betting_round(deck, player_chips, computer_chips, min_bet)

        if game_status == 'end_round':
            if not play_again():
                game_on = False
                print("Thanks for playing!")
            continue

        # Community cards and subsequent betting rounds are only dealt if the game status is 'continue'
        if game_status == 'continue':
            flop, deck = deal_community_cards(deck, 3)
            pot, player_chips, computer_chips, game_status = betting_round(deck, player_chips, computer_chips, min_bet)

            if game_status == 'continue':
                turn, deck = deal_community_cards(deck, 1)
                pot, player_chips, computer_chips, game_status = betting_round(deck, player_chips, computer_chips, min_bet)

            if game_status == 'continue':
                river, deck = deal_community_cards(deck, 1)
                pot, player_chips, computer_chips, game_status = betting_round(deck, player_chips, computer_chips, min_bet)

                if game_status == 'continue':
                    winner = determine_winner(player_hand, computer_hand, flop + turn + river)
                    if winner == 'player':
                        player_chips += pot
                        print("You win the pot!")
                    elif winner == 'computer':
                        computer_chips += pot
                        print("Computer wins the pot!")
                    else:
                        player_chips += pot / 2
                        computer_chips += pot / 2
                        print("It's a tie!")

        if not play_again():
            game_on = False
            print("Thanks for playing!")

if __name__ == "__main__":
    main()
