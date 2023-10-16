from briscola.briscola import Briscola, BriscolaType
from constants import *
from player.player import Player, PlayerTeam
from typing import List

class Briscola4P(Briscola):
    N_PLAYERS = 4
    HAND_SIZE = 3
    
    def __init__(self, players, wait: bool = False):
        if (len(players) != self.N_PLAYERS):
            raise ValueError(f"Number of players given not 4.")
        super().__init__(players, wait)
        
    def type(self) -> BriscolaType:
        return BriscolaType.FOUR_P
    
    def play(self) -> List[Player]:
        # Divide players into two teams
        teams = [[self.players[0], self.players[2]], [self.players[1], self.players[3]]]
        # Indexes of players in each team
        self.teams_index = [[0, 2], [1, 3]]

        # Print the players in the game
        print(f"Game started with players: {[str(player) for player in self.players]}")

        # Shuffle the deck
        self.deck.shuffle()
        print("Deck shuffled")

        # Show the briscola card
        self.briscola = self.deck.showBriscola()
        print(f"Briscola: {YELLOW}{self.briscola}{END}")

        self.starting_player = 0

        # each player draw the starting hand
        self.give_hands()

        # --> Game phase
        self.game_phase()

        # --> End phase
        print(f"{RED}Game finished{END}")
        self.end_phase()

        """
        # check winner
        players_points = [player.count_points() for player in self.players]
        print(f"Players points: {[f'{str(player)}: {points}' for player, points in zip(self.players, players_points)]}")

        teams_points = [sum(players_points[i:j]) for i, j in teams_index]
        print(f"Teams points: {[f'{[str(player) for player in team]}: {points}' for team, points in zip(teams, teams_points)]}")

        max_value = max(teams_points)
        max_index = teams_points.index(max_value)

        if max_value == 60:
            print("It's a TIE!!")
            return None
        else:
            winning_team = teams[max_index]
            print(f"{[str(player) for player in winning_team]} wins the game with {max_value} points")
        """
        return self.score