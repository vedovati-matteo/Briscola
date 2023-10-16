from deck.card import Card, Rank, Suit
from player.player import Player
from constants import *

from typing import Tuple
import socket
import json

class ClientPlayer(Player):
    def __init__(self, name, host, port):
        super().__init__(name)
        self.host = host
        self.port = port
        self.socket = None
    
    def notify(self, game_state: dict):
        g = self.full_game_state(game_state)
        msg = {
            "message_type": "game_state_update",
            "data": g
        }
        self.send(json.dumps(msg))
    
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)  # Listen for one incoming connection
            print(f"Wating for connection on {self.host}:{self.port}")
            client_socket, client_address = self.socket.accept()  # Wait for a client to connect
            self.socket = client_socket
            print(f"Connected to {client_address}")
        except Exception as e:
            print(f"Error connecting to server: {e}")
    
    def send(self, msg):
        try:
            msg = msg.ljust(4096, ' ')
            self.socket.send(msg.encode())
        except Exception as e:
            print(f"Failed to send data: {str(e)}")
    
    def receive(self):
        try:
            data = self.socket.recv(1024).decode()
            return data
        except Exception as e:
            print(f"Failed to receive data: {str(e)}")
    
    def close(self):
        if self.socket:
            self.socket.close()
            print("Connection closed.")
    
    def bid(self, game_state: dict) -> Tuple[Rank, Suit]:
        g = self.full_game_state(game_state)
        msg = {
            "message_type": "bid",
            "data": g
        }
        self.send(json.dumps(msg))
        
        data = self.receive()
        data = json.loads(data)
        
        if not data['data']['pass']:
            c = Card.from_card_state(data['data']['card'])
            return c.rank, c.suit
            
        return None, None
    
    def select_card(self, game_state: dict) -> int:
        g = self.full_game_state(game_state)
        msg = {
            "message_type": "play_card",
            "data": g
        }
        self.send(json.dumps(msg))
        
        data = self.receive()
        data = json.loads(data)
        
        c = Card.from_card_state(data['data']['card'])
        return self.hand.index(c)
    
    def game_over(self, game_state: dict) -> None:
        g = self.full_game_state(game_state)
        msg = {
            "message_type": "game_over",
            "data": g
        }
        self.send(json.dumps(msg))