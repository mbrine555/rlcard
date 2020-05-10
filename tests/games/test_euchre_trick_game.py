import unittest

from rlcard.games.euchre_trick.dealer import EuchreDealer

class TestEuchreTrickGame(unittest.TestCase):

    def test_euchre_dealer(self):
        dealer = EuchreDealer()
        self.assertEqual(len(dealer.deck), 24)

    def test_euchre_dealer_flip(self):
        dealer = EuchreDealer()
        actual_top_card = dealer.deck[0]
        self.assertEqual(actual_top_card, dealer.flip_top_card())

if __name__ == '__main__':
    unittest.main()