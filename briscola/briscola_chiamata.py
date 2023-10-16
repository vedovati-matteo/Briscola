from briscola.briscola import Briscola, BriscolaType
from deck.card import Card
from player.player import PlayerRole
from constants import *
from typing import Tuple
import time

class BriscolaChiamata(Briscola):
    N_PLAYERS = 5
    HAND_SIZE = 8
    
    def __init__(self, players, wait: bool = False):
        if (len(players) != self.N_PLAYERS):
            raise ValueError(f"Number of players given not 5.")
        super().__init__(players, wait)
    
    def type(self) -> BriscolaType:
        return BriscolaType.CHIAMATA
    
    def draw(self) -> bool:
        return False
    
    def bidding_phase(self) -> Tuple[int, Card]:
        self.game_state['current_phase'] = 'bidding'
        self.game_state['bid_history'] = []
        
        still_bidding = [True] * self.N_PLAYERS
        lowest_bid = None
        lowest_bid_suit = None

        # Circular bidding
        i = 0
        while sum(still_bidding) > 1:
            
            if not still_bidding[i]:
                i = (i + 1) % self.N_PLAYERS
                continue
            
            self.game_state['current_player'] = i
            self.notify_players()
            
            bid, suit = self.players[i].bid(self.game_state)
            if not bid:
                still_bidding[i] = False
                print(f"{BLUE}{self.players[i]}{END} passed")
                self.game_state['bid_history'].append({
                    'player': i,
                    'bid': 'PASS',
                })
            elif lowest_bid is None or bid < lowest_bid:
                lowest_bid = bid
                lowest_bid_suit = suit
                self.game_state['bid_history'].append({
                    'player': i,
                    'bid': bid.name,
                })
                print(f"{BLUE}{self.players[i]}{END} bid {bid.name}")
            else:
                still_bidding[i] = False
                self.game_state['bid_history'].append({
                    'player': i,
                    'bid': 'PASS',
                })
                print(f"{BLUE}{self.players[i]}{END} bid too high, passed")
            
            i = (i + 1) % self.N_PLAYERS

        self.game_state['current_player'] = None
        
        index_bidder = still_bidding.index(True) if True in still_bidding else None
        if index_bidder is None: # if no one bid
            return None, None

        print(f"{BLUE}{self.players[index_bidder]}{END} won the bid with {GREEN}{lowest_bid}{END}")

        briscola = Card(lowest_bid, lowest_bid_suit)

        self.game_state['bidder'] = index_bidder
        self.game_state['briscola'] = briscola.get_card_state()
        
        print(f"Briscola: {YELLOW}{briscola}{END}")

        self.notify_players()
        if self.wait:
            time.sleep(2)
        return index_bidder, briscola
    
    def play(self):
        print(f"{GREEN}Game started{END} with players: {[str(p) for p in self.players]}")
        
        self.deck.shuffle()
        print(f"Deck shuffled")
        
        # each player draw the starting hand
        self.give_hands()
        
        self.notify_players()
        
        # --> Bidding phase
        print(f"{GREEN_BG}Bidding phase{END}")
        self.bidder, self.briscola = self.bidding_phase()
        
        # if no one bid end game
        if not self.bidder: # TODO handle end game early in client
            print(f"{GREEN_BG}No one bid{END}")
            return None
        
        # Find the partner of the bidder
        self.partner = [i for i, value in enumerate(self.players) if value.has_card(self.briscola)][0]
        
        # Divide the players into two teams and assign the roles
        self.players[self.bidder].role = PlayerRole.BIDDER
        if self.bidder == self.partner:
            self.teams_index = [[self.bidder], [i for i in range(self.N_PLAYERS) if i != self.bidder]]
        else:
            self.players[self.partner].role = PlayerRole.PARTNER
            self.teams_index = [[self.bidder, self.partner], [i for i in range(self.N_PLAYERS) if i not in [self.bidder, self.partner]]]
        
        for p in self.teams_index[1]:
            self.players[p].role = PlayerRole.NON_BIDDER
            
        self.game_state['partner'] = None
        
        # --> Game phase
        print(f"{GREEN_BG}Game phase{END}")
        self.game_phase()
        
        # --> End Phase
        print(f"{RED}Game finished{END}")
        self.end_phase()
        
        return self.score
    
    