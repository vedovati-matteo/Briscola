
from briscola.briscola_chiamata import BriscolaChiamata
from briscola.briscola_2p import Briscola2P
from briscola.briscola_4p import Briscola4P
from player.console_player import ConsolePlayer
from player.random_player import RandomPlayerWait, RandomPlayer
from player.client_player import ClientPlayer

p0 = RandomPlayer("MinnieAI")
p1 = ConsolePlayer("Pippo")
p2_client = ClientPlayer("Paperino", "localhost", 8000)
p2_client.connect()
p2 = RandomPlayer("PaperinoAI")
p3 = RandomPlayer("PlutoAI")
p4 = RandomPlayerWait("TopolinoAI")

print("All connected, Starting game...")

briscola = Briscola4P([p0, p1, p2_client, p3], wait=False)
briscola.play()
