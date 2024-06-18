import unittest
from unittest.mock import patch
from script import create_deck, deal_cards, betting_round, initialize_game

class TestPokerGame(unittest.TestCase):

    def test_deck_length(self):
        """Test that the deck has 52 cards after creation."""
        deck = create_deck()
        self.assertEqual(len(deck), 52)

    def test_deal_cards(self):
        """Test dealing cards reduces the deck size appropriately."""
        deck = create_deck()
        _, deck = deal_cards(deck, 2)
        self.assertEqual(len(deck), 52 - 2)

    def test_game_initialization(self):
        """Test the initial game setup for correct chip counts and minimum bet."""
        deck, player_chips, computer_chips, min_bet = initialize_game()
        self.assertEqual(player_chips, 100)
        self.assertEqual(computer_chips, 100)
        self.assertEqual(min_bet, 10)
        self.assertEqual(len(deck), 52)

    @patch('builtins.input', side_effect=['call'])
    @patch('script.random.choice', return_value='call')
    def test_betting_round(self, mock_random_choice, mock_input):
        """Test the betting round logic for simple scenarios."""
        deck = create_deck()
        pot, player_chips, computer_chips, game_status = betting_round(deck, 100, 100, 0, 10)
        # Assuming player and computer both 'call' the minimum bet for simplicity
        self.assertEqual(pot, 20)  # Both bet $10
        self.assertEqual(player_chips, 90)
        self.assertEqual(computer_chips, 90)
        self.assertEqual(game_status, 'continue')

    @patch('script.input', return_value='all in')
    @patch('script.random.choice', return_value='call')
    def test_end_game_distribution(self, mock_choice, mock_input):
        """Test the distribution of chips at the end of the game."""
        deck = create_deck()
        pot, player_chips, computer_chips, game_status = betting_round(deck, 100, 100, 0, 10)
        # Assuming the game ends after one all-in call
        self.assertEqual(pot, 200)  # Both go all-in with $100 starting chips
        self.assertEqual(game_status, 'continue')  # Assuming continue for simplicity
        # Add logic to simulate the end of the game if needed


# If you want the tests to run when you directly run this script
if __name__ == '__main__':
    unittest.main()
