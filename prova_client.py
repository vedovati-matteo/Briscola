#from client_player.clientGUI import GUIClient
from client_player.console_client import ConsoleClient

if __name__ == "__main__":
    #client = GUIClient("Paperino", "localhost", 8000)
    #client.run()
    
    client = ConsoleClient("Paperino", "localhost", 8000)
    client.run()