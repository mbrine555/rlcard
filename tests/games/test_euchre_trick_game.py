import unittest
import numpy as np

from rlcard.games.euchre_trick.dealer import EuchreDealer
from rlcard.games.euchre_trick.player import EuchrePlayer as Player

class TestEuchreTrickGame(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()