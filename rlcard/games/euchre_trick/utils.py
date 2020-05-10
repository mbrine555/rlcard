from rlcard.core import Card

# Maps trump suit to left bower
LEFT = {'D': 'HJ', 'H': 'DJ', 'C': 'SJ', 'S': 'CJ'}

# Order of cards from low->high for non-trump suits
NON_TRUMP_ORDER = ['9', 'T', 'J', 'Q', 'K', 'A']

def init_euchre_deck():
    ''' Initialize a 24 card Euchre deck
    Returns:
        (list): A list of Card object
    '''
    suit_list = ['S', 'H', 'D', 'C']
    rank_list = ['A', '9', 'T', 'J', 'Q', 'K']
    res = [Card(suit, rank) for suit in suit_list for rank in rank_list]
    return res

def cards2list(cards):
    return [card.get_index() for card in cards]

def is_left(card, trump):
    return card.get_index() == LEFT[trump]

def is_right(card, trump):
    return card.get_index() == trump + 'J'