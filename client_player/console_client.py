from client_player.client import Client
from constants import *

class ConsoleClient(Client):
    def __init__(self, name, host, port):
        super().__init__(name, host, port)
    
    def game_state_update(self, game_state: dict):
        pass
    
    def bid(self, game_state: dict) -> dict:
        print(f"{BLUE}{self.name}{END}'s turn to bid.")
        print(f"Your hand: {game_state['hand']}")
        print(f"Last bid: {game_state['bid_history'][-1]}")
        rank = input("Choose a Rank or PASS: ")
        if rank == 'PASS':
            return {
                "pass": True
            }
        suit = input("Choose a Suit: ")
        return {
            "pass": False,
            "card": {
                "rank": rank,
                "suit": suit
            }
        }
    
    def play_card(self, game_state: dict) -> dict:
        print(f"{BLUE}{self.name}{END}'s turn to play a card.")
        print(f"Your hand: {game_state['hand']}")
        i = input(f"Choose a card (indexs 0 to {len(game_state['hand']) - 1}): ")
        card = game_state['hand'][int(i)]
        return {
            "card": card
        }
    
    def game_over(self, game_state: dict) -> None:
        print(f"Playes scores: {game_state['score']}")
        if game_state['winner'] is None:
            print(f"Game ended in a tie.")
        else:
            print(f"Winner: {game_state['winner']}")
        