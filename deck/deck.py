from deck.card import Card, Suit, Rank
import itertools
import random

class Deck:
    def __init__(self):
        # Create a list of all possible cards in the deck
        self.cards = [Card(rank, suit) for rank, suit in itertools.product(Rank, Suit)]

    def shuffle(self) -> None:
        # Shuffle the deck
        random.shuffle(self.cards)

    def deal(self, num_cards: int = 1) -> list:
        # Deal a specified number of cards from the deck
        if num_cards <= len(self.cards):
            return [self.cards.pop() for _ in range(num_cards)]
        else:
            return None
    
    def empty(self) -> bool:
        # Check if the deck is empty
        return len(self.cards) <= 0
            
    def showBriscola(self) -> Card:
        # Return the first card in the deck (the briscola)
        return self.cards[0]
        
    def __str__(self) -> str:
        # Return a string representation of the deck
        return ', '.join(map(str, self.cards))