import random

from rlcard.games.euchre_trick.utils import init_euchre_deck


class EuchreDealer(object):
    ''' Initialize a Euchre dealer class
    '''
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_euchre_deck()
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, player, num):
        ''' Deal some cards from deck to one player

        Args:
            player (object): The object of EuchrePlayer
            num (int): The number of cards to be dealt
        '''
        for _ in range(num):
            card = self.deck.pop()
            player.hand.append(card)

    def flip_top_card(self):
        ''' Flip top card when a new game starts

        Returns:
            (object): The object of Card at the top of the deck
        '''
        top_card = self.deck.pop()
        return top_card