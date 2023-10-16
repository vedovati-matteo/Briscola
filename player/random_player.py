import random
from deck.card import Rank, Suit
from player.player import Player
from typing import Tuple
import time

class RandomPlayer(Player):
    def bid(self, game_state: dict) -> Tuple[Rank, Suit]:
        # Always pass on making a bid
        return None, None
    
    def select_card(self, game_state: dict) -> int:
        # Select a random card from the player's hand to play
        return random.randint(0, len(self.hand)-1)
    
class RandomPlayerWait(Player):
    def bid(self, game_state: dict) -> Tuple[Rank, Suit]:
        # Always pass on making a bid
        time.sleep(2)
        return None, None
    
    def select_card(self, game_state: dict) -> int:
        # Select a random card from the player's hand to play
        time.sleep(2)
        return random.randint(0, len(self.hand)-1)