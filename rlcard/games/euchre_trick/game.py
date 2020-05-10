import random
from copy import deepcopy

import numpy as np

from rlcard.games.euchre_trick.dealer import EuchreDealer as Dealer
from rlcard.games.euchre_trick.judger import EuchreJudger as Judge
from rlcard.games.euchre_trick.player import EuchrePlayer as Player
from rlcard.games.euchre_trick.utils import cards2list, is_left, is_right


class EuchreGame(object):

    def __init__(self, allow_step_back=False):
        self.allow_step_back = allow_step_back
        self.num_players = 4
        self.np_random = np.random.RandomState()

    def init_game(self):
        ''' Initialize players and state

        Returns:
            (tuple): Tuple containing:

                (dict): The first state in one game
                (int): Current player's id
        '''
        self.payoffs = [0 for _ in range(self.num_players)]

        self.judge = Judge()

        self.dealer = Dealer(self.np_random)
        self.dealer_player_id = random.randrange(0, self.num_players)
        self.players = [Player(i, self.np_random) for i in range(self.num_players)]

        self.trump = None
        self.lead_suit = None
        self.turned_down = None
        self.card_history = []
        self.center = {}
        self.score = {i:0 for i in range(self.num_players)}
        self.game_over = False

        # Each player is dealt 5 cards
        for player in self.players:
            self.dealer.deal_cards(player, 5)

        # Flip top card
        self.flipped_card = self.dealer.flip_top_card()

        # Move current player to left of dealer
        self.current_player = self._increment_player(self.dealer_player_id)
        state = self.get_state(self.current_player)
        return state, self.current_player

    def step(self, action):
        ''' Get the next state

        Args:
            action (str): A specific action

        Returns:
            (tuple): Tuple containing:

                (dict): next player's state
                (int): next plater's id
        '''
        if action == 'pick':
            # Order dealer to pick card up and move current player to dealer
            self._perform_pick_action()
            state = self.get_state(self.current_player)
            return state, self.current_player
    
        if action == 'pass':
            # Move current player to left unless dealer is stuck
            self._perform_pass()
            state = self.get_state(self.current_player)
            return state, self.current_player

        if action.startswith('call'):
            # Call trump suit and move current player to left of dealer
            suit = action.split('-')[1]
            self._perform_call(suit)
            state = self.get_state(self.current_player)
            return state, self.current_player

        if action.startswith('discard'):
            # Dealer chooses card to discard and player moves to left
            card = action.split('-')[1]
            self._perform_discard(card)
            state = self.get_state(self.current_player)
            return state, self.current_player
    
        # Play card and move player to left
        self._play_card(action)

        # End trick if 4 cards have been played
        if len(self.center) == 4:
            self._end_trick()
            # End game if all cards have been played
            if len(self.players[self.current_player].hand) == 0:
                self.winner, self.points = self.judge.judge_hand(self)
                self.game_over = True

        state = self.get_state(self.current_player)
        return state, self.current_player

    def get_state(self, player_id):
        ''' Return player's state

        Args:
            player_id (int): player id

        Returns:
            (dict): The state of the player
        '''
        state = {}
        player = self.players[player_id]

        state['hand'] = cards2list(player.hand)
        state['trump_called'] = self.trump is not None
        state['trump'] = self.trump
        state['turned_down'] = self.turned_down
        state['lead_suit'] = self.lead_suit
        state['card_history'] = self.card_history
        
        if self.flipped_card is not None:
            state['flipped'] = self.flipped_card.get_index()
        else:
            state['flipped'] = None
        
        state['center'] = {k:v.get_index() for k, v in self.center.items()}
        return state

    def _perform_pick_action(self):
        dealer_player = self.players[self.dealer_player_id]
        dealer_player.hand.append(self.flipped_card)
        self.card_history.append(self.flipped_card.get_index())
        self.trump = self.flipped_card.suit
        self.flipped_card = None
        self.calling_player = self.current_player
        self.current_player = self.dealer_player_id

    def _increment_player(self, player_id):
        return (player_id+ 1) % self.num_players

    def _perform_discard(self, card):
        player = self.players[self.current_player]
        for index, hand_card in enumerate(player.hand):
            if hand_card.get_index() == card:
                remove_index = index
                break
        card = player.hand.pop(remove_index)
        self.current_player = self._increment_player(self.current_player)

    def _play_card(self, action):
        player = self.players[self.current_player]
        for index, hand_card in enumerate(player.hand):
            if hand_card.get_index() == action:
                remove_index = index
                break
        card = player.hand.pop(remove_index)
        if len(self.center) == 0:
            if card.suit == self.trump or is_left(card, self.trump):
                self.lead_suit = self.trump
            else:
                self.lead_suit = card.suit
        self.center[self.current_player] = card
        self.current_player = self._increment_player(self.current_player)

    def _end_trick(self):
        winner = self.judge.judge_trick(self)
        self.score[winner] += 1
        for card in self.center.values():
            self.card_history.append(card.get_index())
        self.current_player = winner
        self.center = {}
        self.lead_suit = None

    def _perform_call(self, suit):
        self.trump = suit
        self.current_player = self._increment_player(self.dealer_player_id)

    def _perform_pass(self):
        if self.current_player == self.dealer_player_id:
            self.turned_down = self.flipped_card.suit
            self.flipped_card = None
        self.current_player = self._increment_player(self.current_player)

    def get_legal_actions(self):
        ''' Return the legal actions for current player

        Returns:
            (list): A list of legal actions
        '''
        hand = self.players[self.current_player].hand
        if len(hand) == 6:
            return [f"discard-{card.get_index()}" for card in hand]

        if self.trump is None:
            if self.turned_down is None:
                return ['pick', 'pass']
            else:
                actions = [f"call-{suit}" for suit in ['S', 'C', 'D', 'H'] if suit != self.turned_down]
                if self.current_player != self.dealer_player_id:
                    actions += ['pass']
                return actions

        if self.lead_suit is None:
            return [card.get_index() for card in hand]
        
        follow = [card.get_index() for card in hand if 
                    (card.suit == self.lead_suit and not is_left(card, self.trump)) or 
                    (is_left(card, self.lead_suit) and self.lead_suit == self.trump)]

        if len(follow) > 0:
            return follow
        return [card.get_index() for card in hand]

    def get_player_num(self):
        ''' Return the number of players in Limit Texas Hold'em

        Returns:
            (int): The number of players in the game
        '''
        return self.num_players

    def get_payoffs(self):
        ''' Return the payoffs of the game

        Returns:
            (list): Each entry corresponds to the payoff of one player
        '''
        payoffs = {}
        
        for i in range(self.num_players):
            if i in self.winner:
                payoffs[i] = self.points
            else:
                payoffs[i] = -self.points

        return payoffs

    def is_over(self):
        ''' Check if the game is over

        Returns:
            (boolean): True if the game is over
        '''
        return self.game_over

    @staticmethod
    def get_action_num():
        ''' Return the number of applicable actions

        Returns:
            (int): The number of actions. There are 61 actions
        '''
        return 54

    def get_player_id(self):
        ''' Return the current player's id

        Returns:
            (int): current player's id
        '''
        return self.current_player
