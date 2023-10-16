from abc import ABC
from deck.deck import Deck
from player.player import Player
from briscola.briscola_type import BriscolaType
from constants import *

import time

class Briscola(ABC):
    N_PLAYERS = None
    HAND_SIZE = None
    
    def __init__(self, players: list, wait: bool = False):
        super().__init__()
        self.deck = Deck()
        self.players = players
        self.wait = wait
        self.teams_index = None
        self.score = [0 for i in range(self.N_PLAYERS)]
        self.game_state_init()
    
    def type(self) -> BriscolaType:
        pass
    
    def game_state_init(self):
        self.game_state = {
            'game_type': self.type().value,
            'players': []
        }
        for i, player in enumerate(self.players):
            player.set_id_type(i, self.type())
            player_dict = {
                'name': player.name,
                'ID': i
            }
            self.game_state['players'].append(player_dict)
        self.game_state['current_phase'] = 'start'
        self.game_state['current_player'] = 0
    
    def round_init(self):
        round_dict = dict()
        for i in range(self.N_PLAYERS):
            round_dict[i] = {
                'played': False
            }
        return round_dict
    
    def notify_players(self):
        for p in self.players:
            p.notify(self.game_state)
    
    def game_over(self):
        for p in self.players:
            p.game_over(self.game_state)
    
    def give_hands(self):
        # Deal starting hands to players
        for p in self.players:
            hand = self.deck.deal(self.HAND_SIZE)
            p.get_hand(hand)
        print("Players drawing the starter cards")
        
    def draw(self) -> bool:
        # Draw one card for each player
        for i in range(self.N_PLAYERS):
            index = (self.starting_player + i) % self.N_PLAYERS
            p = self.players[index]
            card = self.deck.deal(1)
            if not card:
                return False
            p.get_card(card[0])
        print("Players drawing one card each")
        return True

    def last_round_over(self) -> bool:
        # Check if the last round is over (i.e., if a player has an empty hand)
        return self.players[0].is_empty_hand()
    
    def play_round(self):
        # Start a new round
        self.game_state['current_round'] += 1
        self.game_state['rounds'][self.game_state['current_round']] = self.round_init()
        
        print(f"{GREEN_BG}Round start{END}")
        table = []
        
        # Each player plays one card
        for i in range(self.N_PLAYERS):
            index = (self.starting_player + i) % self.N_PLAYERS
            self.game_state['current_player'] = index
            self.notify_players()
            p = self.players[index]
            print(f"{BLUE}{p}{END}'s turn: {p.print_hand()}")
            card = p.play_card(self.game_state)
            if card == self.briscola:
                self.game_state['partner'] = index
            self.game_state['rounds'][self.game_state['current_round']][index]['played'] = True
            self.game_state['rounds'][self.game_state['current_round']][index].update(card.get_card_state())
            table.append(card)
        
        # Print the cards on the table
        print(f"{GREEN}Table{END}: {[ str(c) for c in table ]}")
        
        # Check the winner of the round
        index = self.check_round_winner(table)
        p = (self.starting_player + index) % self.N_PLAYERS
        self.game_state['rounds'][self.game_state['current_round']]['winner'] = p
        print(f"{BLUE}{self.players[p]}{GREEN} wins the round{END}")
        
        # The winner gets the cards on the table
        self.players[p].win_turn(table)
        self.starting_player = p
        
        self.game_state['current_player'] = None
        self.notify_players()
        if self.wait:
            time.sleep(2)
        
        # Draw one card for each player
        self.draw()
    
    def check_round_winner(self, table: list) -> int:
        briscola_played = False
        
        # Check which card wins the round
        winning = 0
        for i in range(len(table)):
            c = table[i]
            if c.suit == self.briscola.suit and not briscola_played:
                briscola_played = True
                winning = i
            elif c.suit == table[winning].suit and c.rank > table[winning].rank:
                winning = i
            
        return winning
    
    def play(self) -> Player:
        pass
    
    def end_phase(self):
        self.game_state['current_phase'] = 'end'
        
        # check winner
        players_point = [p.count_points() for p in self.players]
        
        print(f"Players points: {BLUE}{[str(p) + ': ' + str(players_point[i]) for i, p in enumerate(self.players)]}{END}")
        
        self.game_state['points'] = { str(i): str(players_point[i]) for i in range(self.N_PLAYERS) }
        
        teams_point = [sum([players_point[j] for j in self.teams_index[i]]) for i in range(2)]
        print(f"Teams points: {BLUE}{[str([str(self.players[p]) for p in self.teams_index[i]]) + ': ' + str(teams_point[i]) for i in range(2)]}{END}")
        
        max_value = max(teams_point)
        max_index = teams_point.index(max_value)
        
        # Check if it's a tie
        if max_value == 60:
            self.game_state['winner'] = None
            self.game_state['loser'] = None
            print(f"{GREEN_BG}It's a TIE!!{END}")
            return
        else:
            # Print the winning team
            self.game_state['winner'] = self.teams_index[max_index]
            self.game_state['loser'] = self.teams_index[(max_index + 1) % 2]
            self.score = [1 if i in self.teams_index[max_index] else -1 for i in range(self.N_PLAYERS)]
            if hasattr(self, 'bidder'):
                if self.bidder in self.teams_index[max_index]:
                    self.score[self.bidder] = 2 if self.partner != self.bidder else 4
                else:
                    self.score[self.bidder] = -2 if self.partner != self.bidder else -4
            
            print(f"{BLUE}{[str(self.players[i]) for i in self.teams_index[max_index]]}{END}{GREEN_BG} wins the game with {max_value} points{END}")
        
        self.game_state['score'] = { str(i): str(self.score[i]) for i in range(self.N_PLAYERS) }
        
        self.game_over()
        
    def game_phase(self):
        self.game_state['current_phase'] = 'game'
        
        self.starting_player = 0
        self.game_state['current_player'] = self.starting_player
        self.game_state['current_round'] = 0
        self.game_state['rounds'] = dict()
        
        # play all the rounds
        while not self.last_round_over():
            self.play_round()