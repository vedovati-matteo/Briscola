from enum import Enum


class Suit(Enum):
    # Define the different suits as enum members with string values
    COINS = ('Coins', 1)
    CUPS = ('Cups', 2)
    SWORDS = ('Swords', 0)
    CLUBS = ('Clubs', 3)
    
    def __eq__(self, other) -> bool:
        # Override the equality operator to compare the index of the enum members
        if isinstance(other, Suit):
            return(
                self._member_names_.index(self.name) == self._member_names_.index(other.name)
            )
        return NotImplemented
    
    def __str__(self) -> str:
        # Override the string representation of the enum member to return its string value
        return self.value[0]

class Rank(Enum):
    # Define the different ranks as enum members with tuple values containing the rank name and its value
    ACE = ('Ace', 11, 0)
    THREE = ('3', 10, 2)
    KING = ('King', 4, 12)
    KNIGHT = ('Knight', 3, 11)
    KNAVE = ('Knave', 2, 10)
    SEVEN = ('7', 0, 6)
    SIX = ('6', 0, 5)
    FIVE = ('5', 0, 4)
    FOUR = ('4', 0, 3)
    TWO = ('2', 0, 1)
    
    def __eq__(self, other) -> bool:
        # Override the equality operator to compare the index of the enum members
        if isinstance(other, Rank):
            return(
                self._member_names_.index(self.name) == self._member_names_.index(other.name)
            )
        return NotImplemented
    
    def __gt__(self, other):
        # Override the greater than operator to compare the index of the enum members
        if isinstance(other, Rank):
            return (
                self._member_names_.index(self.name) <
                self._member_names_.index(other.name)
            )
        return NotImplemented
    
    def __lt__(self, other):
        # Override the less than operator to compare the index of the enum members
        if isinstance(other, Rank):
            return (
                self._member_names_.index(self.name) >
                self._member_names_.index(other.name)
            )
        return NotImplemented
    
    def __ge__(self, other):
        # Override the greater than or equal to operator to compare the index of the enum members
        if isinstance(other, Rank):
            return (
                self._member_names_.index(self.name) <=
                self._member_names_.index(other.name)
            )
        return NotImplemented
    
    def __le__(self, other):
        # Override the less than or equal to operator to compare the index of the enum members
        if isinstance(other, Rank):
            return (
                self._member_names_.index(self.name) >=
                self._member_names_.index(other.name)
            )
        return NotImplemented

    def __str__(self) -> str:
        # Override the string representation of the enum member to return its rank name
        return self.value[0]

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        # Initialize the Card object with a rank and a suit
        self.rank = rank
        self.suit = suit
    
    def __eq__(self, other) -> bool:
        # Override the equality operator to compare the rank and suit of the Card objects
        if isinstance(other, Card):
            return(
                self.rank == other.rank and
                self.suit == other.suit
            )
        return NotImplemented
    
    def __str__(self) -> str:
        # Override the string representation of the Card object to return its rank and suit
        return str(self.rank) + " of " + str(self.suit)
    
    def value(self) -> int:
        # Return the value of the Card object's rank
        return self.rank.value[1]
    
    def get_card_state(self) -> dict:
        # Return a dictionary containing the rank and suit of the Card object
        return {
            'rank': self.rank.name,
            'suit': self.suit.name
        }
    
    @staticmethod
    def from_card_state(card_state: dict):
        # Return a Card object from a dictionary containing the rank and suit of the Card object
        return Card(
            rank=Rank[card_state['rank']],
            suit=Suit[card_state['suit']]
        )