from abc import ABC
from deck.card import Card, Rank, Suit
from briscola.briscola_type import BriscolaType
from enum import Enum
from typing import Tuple

class PlayerRole(Enum):
    UNKNOWN = 0
    BIDDER = 1
    NON_BIDDER = 2
    PARTNER = 3
    
class PlayerTeam(Enum):
    TEAM_1 = 1
    TEAM_2 = 2

class Player(ABC):
    def __init__(self, name: str):
        # Initialize the player's hand, pile, and name
        super().__init__()
        self.hand = []
        self.pile = []
        self.name = name
        self.ID = None
        self.role = None
        
    def __str__(self) -> str:
        # Return the player's name as a string
        return f"{self.name}"

    def set_id_type(self, ID: int, game_type: BriscolaType):
        # Set the player's ID and game type
        self.ID = ID
        if game_type == BriscolaType.CHIAMATA:
            self.role = PlayerRole.UNKNOWN
        else:
            if ID % 2 == 0:
                self.role = PlayerTeam.TEAM_1
            else:
                self.role = PlayerTeam.TEAM_2

    def full_game_state(self, game_state: dict) -> dict:
        full_game_state = game_state
        self_game_state = {
            'player': self.ID,
            'role': self.role.value,
            'hand': [],
        }
        
        for card in self.hand:
            self_game_state['hand'].append(card.get_card_state())
        
        full_game_state.update(self_game_state)
        
        return full_game_state

    def notify(self, game_state: dict):
        # Notify the player of the current game state
        pass
    
    def select_card(self, game_state: dict) -> int:
        # Abstract method for selecting a card to play
        pass

    def bid(self, game_state: dict) -> Tuple[Rank, Suit]:
        # Abstract method for making a bid
        pass

    def play_card(self, game_state: dict) -> Card:
        # Select a card to play from the player's hand, remove it from the hand, and return it
        i = self.select_card(game_state)
        card = self.hand[i]
        self.hand.remove(card)
        print(f"{card} played")
        return card
    
    def game_over(self, game_state: dict) -> None:
        pass
    
    def get_hand(self, hand: list):
        # Set the player's hand to the specified list of cards
        self.hand = hand
    
    def get_card(self, card: Card):
        # Add the specified card to the player's hand
        self.hand.append(card)
            
    def win_turn(self, cards: list):
        # Add the specified list of cards to the player's pile
        self.pile.extend(cards)
        
    def is_empty_hand(self) -> bool:
        # Check if the player's hand is empty
        return not self.hand
    
    def count_points(self) -> int:
        # Calculate the total point value of the cards in the player's pile
        tot_value = 0
        for c in self.pile:
            tot_value += c.value()
        return tot_value
    
    def has_card(self, card: Card) -> bool:
        # Check if the player's hand contains the specified card
        print(self.print_hand())
        return card in self.hand
    
    def print_hand(self) -> str:
        # Return a string representation of the player's hand
        return f"{[ str(c) for c in self.hand ]}"
    