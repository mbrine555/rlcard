import unittest
import numpy as np

from rlcard.games.euchre_trick.dealer import EuchreDealer
from rlcard.games.euchre_trick.player import EuchrePlayer as Player
from rlcard.games.euchre_trick.game import EuchreGame as Game

class TestEuchreTrickGame(unittest.TestCase):

    def test_get_player_num(self):
        game = Game()
        player_num = game.get_player_num()
        self.assertEqual(player_num, 4)

    def test_get_action_num(self):
        game = Game()
        action_num = game.get_action_num()
        self.assertEqual(action_num, 54)

    def test_euchre_dealer(self):
        dealer = EuchreDealer(np.random.RandomState())
        self.assertEqual(len(dealer.deck), 24)

    def test_euchre_dealer_flip(self):
        dealer = EuchreDealer(np.random.RandomState())
        actual_top_card = dealer.deck[0]
        self.assertEqual(actual_top_card, dealer.flip_top_card())

    def test_euchre_deal(self):
        dealer = EuchreDealer(np.random.RandomState())
        player = Player(player_id=1, np_random=np.random.RandomState())
        dealer.deal_cards(player, num=5)
        self.assertEqual(len(player.hand), 5)

    def test_init_game(self):
        game = Game()
        state, current_player = game.init_game()
        self.assertEqual(len(state['hand']), 5)
        self.assertEqual(state['trump'], None)
        self.assertEqual(state['card_history'], [])
        self.assertEqual(state['lead_suit'], None)
        self.assertEqual(state['trump_called'], False)
        self.assertEqual(state['turned_down'], None)
        self.assertEqual(state['center'], {})
        self.assertEqual(len(state['flipped']), 2)
        self.assertEqual(current_player, (game.dealer_player_id+1) % 4)

    def test_step(self):
        game = Game()
        state, current_player = game.init_game()
        

if __name__ == '__main__':
    unittest.main()