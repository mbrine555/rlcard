from rlcard.games.euchre_trick.utils import is_left, is_right, NON_TRUMP_ORDER

class EuchreJudger(object):

    def judge_trick(self, game):
        ''' Judge the winner of the trick

        Args:
            game (EuchreGame): Instance of game to judge

        Returns:
            (int): The player id of the winner
        '''
        center_cards = game.center
        trump = game.trump
        leader = game.current_player
        player_order = self._get_player_order(leader)
        
        lead_suit = center_cards[leader].suit
        current_winning_card = center_cards[leader]
        
        # The right always wins
        if is_right(current_winning_card, trump):
            return self._get_winner_id(current_winning_card, center_cards)

        for player in player_order[1:]:
            candidate_card = center_cards[player]
            
            if is_right(candidate_card, trump):
                current_winning_card = candidate_card
                break

            # Card is not right and winning card is left, so move on
            if is_left(current_winning_card, trump):
                continue

            # Winning card is not right and played is left, so we can continue
            if is_left(candidate_card, trump):
                current_winning_card = candidate_card
                continue

            current_winning_card = self._get_winning_card(card1=candidate_card, 
                                                          card2=current_winning_card,
                                                          trump=trump,
                                                          lead_suit=lead_suit)
        
        return self._get_winner_id(current_winning_card, center_cards)

    def judge_hand(self, game):
        ''' Judge the winner of the hand

        Args:
            game (EuchreGame): Instance of game to judge

        Returns:
            (tuple): Tuple containing list of player ids of winning team 
                     and score
        '''
        team_1_score = game.score[0] + game.score[2]
        if team_1_score >= 3:
            return [0,2], 1
        else:
            return [1,3], 1

    def _get_player_order(self, leader):
        ''' Get order of cards played based on leader id

        Args:
            leader (int): Player id of leader

        Returns:
            (list): list of player ids in playing order
        '''
        return [(i+leader)%4 for i in range(4)]

    def _get_winning_card(self, card1, card2, trump, lead_suit):
        ''' Compare two cards to see what wins

        Args:
            card1 (Card): Candidate card to compare
            card2 (Card): Candidate card to compare
            trump (str): Current trump suit as letter (S,C,H,D)
            lead_suit (str): Current lead suit as letter (S,C,H,D)

        Returns:
            (Card): Winning card
        '''
        if (card1.suit != trump):
            if card1.suit == lead_suit:
                if self._greater_than_non_trump(card1, card2):
                    return card1
        
        if (card1.suit == trump):
            if card1.suit != card2.suit:
                return card1

            if self._greater_than_non_trump(card1, card2):
                return card1
        
        return card2

    @staticmethod
    def _greater_than_non_trump(card1, card2):
        ''' Compare two non-trump cards

        Args:
            card1 (Card): Candidate card to compare
            card2 (Card): Candidate card to compare

        Returns:
            (bool): Is card1 greater than card2?
        '''
        res = (NON_TRUMP_ORDER.index(card1.rank) > 
                NON_TRUMP_ORDER.index(card2.rank))
        return res

    @staticmethod
    def _get_winner_id(winning_card, center_cards):
        ''' Gets player id of winning card

        Args:
            winning_card (Card): Winner's card
            center_cards (dict): Dictionary of {player_id: card}

        Returns:
            (int): Player id of winner
        '''
        winner = [k for k, v in center_cards.items() if winning_card == v]
        return winner[0]