from player.player import Player
from deck.card import Rank, Suit

from typing import Tuple

class ConsolePlayer(Player):
    def select_card(self, game_state: dict) -> int:
        # Print the player's hand and prompt the user to select a card to play
        str_hand = self.get_str_hand()
        print(str_hand)
        n_card = input("select one card: ")
        n_card = int(n_card)
        return n_card - 1
    
    def bid(self, game_state: dict) -> Tuple[Rank, Suit]:
        # Print the player's hand and prompt the user to make a bid
        str_hand = self.get_str_hand()
        print(str_hand)
        bid = input("bid (ACE, THREE, KING, KNIGHT, KNAVE, SEVEN, SIX, FIVE, FOUR, TWO or PASS): ")
        bid = bid.upper()
        if bid == "PASS":
            return None, None
        suit = input("suit (COINS, CUPS, SWORDS, CLUBS): ")
        suit = suit.upper()
        return Rank[bid], Suit[suit]
    
    def get_str_hand(self) -> str:
        # Return a string representation of the player's hand
        str_hand = "|"
        for i in range(len(self.hand)):
            str_hand = str_hand + " " + str(i+1) + ". " +  str(self.hand[i]) + " |"
        return str_hand