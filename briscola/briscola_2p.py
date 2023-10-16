from briscola.briscola import Briscola, BriscolaType
from player.player import Player, PlayerTeam
from constants import *

class Briscola2P(Briscola):
    N_PLAYERS = 2
    HAND_SIZE = 3
    
    def __init__(self, players, wait: bool = False):
        # Check if the number of players is 2
        if (len(players) != self.N_PLAYERS):
            raise ValueError(f"Number of players given not 2.")
        # Call the constructor of the parent class
        super().__init__(players, wait)
        
    def type(self) -> BriscolaType:
        return BriscolaType.TWO_P
    
    def play(self) -> Player:
        # Divide the players into two teams
        self.teams_index = [[0], [1]]
        
        # Print game start message and list of players
        print(f"{GREEN}Game started{END} with players: {[str(p) for p in self.players]}")
        
        # Shuffle the deck
        self.deck.shuffle()
        print(f"Deck shuffled")
        
        # Show the briscola card
        self.briscola = self.deck.showBriscola()
        print(f"Briscola: {YELLOW}{self.briscola}{END}")
        
        # Set the starting player to player 0
        self.starting_player = 0
        
        # Give each player their starting hand
        self.give_hands()
        
        # --> Game phase
        self.game_phase()

        # --> End phase
        print(f"{RED}Game finished{END}")
        self.end_phase()
        
        """
        # Count the points for each player and print the results
        players_point = [p.count_points() for p in self.players]
        print(f"Players points: {BLUE}{[f'{p}: {players_point[i]}' for i, p in enumerate(self.players)]}{END}")
        
        # Determine the winner and print the result
        max_value = max(players_point)
        max_index = players_point.index(max_value)
        if max_value == 60:
            print(f"{GREEN_BG}It's a TIE!!{END}")
            return None
        else:
            print(f"{BLUE}{self.players[max_index]}{END}{GREEN_BG} wins the game with {max_value} points{END}")
        """
        # Return the winning player
        return self.score