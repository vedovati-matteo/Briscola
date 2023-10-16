from client_player.client import Client
from GUI.GUI import GUI
import multiprocessing

class GUIClient(Client):
    def __init__(self, name, host, port):
        super().__init__(name, host, port)
        
        self.gui_request_queue = multiprocessing.Queue()
        self.gui_response_queue = multiprocessing.Queue()
        
        self.gui = GUI(self.gui_request_queue, self.gui_response_queue)
        
        # Create and start the GUI process
        self.gui_process = multiprocessing.Process(target=self.gui.run)
        self.gui_process.start()
        
    def game_state_update(self, game_state: dict) -> None:
        self.gui_request_queue.put(("game_state", game_state))
        print("game_state_update")
    
    def bid(self, game_state: dict) -> dict:
        self.gui_request_queue.put(("bid", game_state))
        print("bid request")
        
        response = self.gui_response_queue.get()
        return response
    
    def play_card(self, game_state: dict) -> dict:
        self.gui_request_queue.put(("play_card", game_state))
        
        response = self.gui_response_queue.get()
        return response
    
    def game_over(self, game_state: dict) -> None:
        self.gui_request_queue.put(("game_over", game_state))