from constants import *

import socket
import json
import time


class Client:
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        while not self.connect():
            time.sleep(1)
        self.hadle_messages()
    
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print(BLUE + self.name + END + " connected to the server.")
            return True
        except Exception as e:
            print(RED + self.name + END + " failed to connect to the server: " + str(e) + ".")
        
        return False
    
    def send(self, msg):
        try:
            self.socket.sendall(msg.encode())
        except Exception as e:
            print(RED + self.name + END + " failed to send message to the server: " + str(e) + ".")
    
    def receive(self):
        try:
            msg = self.socket.recv(4096)
            return msg.decode().rstrip()
        except Exception as e:
            print(RED + self.name + END + " failed to receive message from the server: " + str(e) + ".")
            return None
        
    def disconnect(self):
        self.socket.close()
        print(BLUE + self.name + END + " disconnected from the server.")
    
    def hadle_messages(self):
        try:
            while True:
                msg = self.receive()
                if not msg:
                    break
                
                with open('log.txt', 'a') as f:
                    f.write(msg + "\n")
                
                msg = json.loads(msg)
                response = None
                if msg['message_type'] == 'game_state_update':
                    self.game_state_update(msg['data'])
                elif msg['message_type'] == 'bid':
                    response = self.bid(msg['data'])
                    response = {
                        "message_type": "bid",
                        "data": response
                    }
                elif msg['message_type'] == 'play_card':
                    response = self.play_card(msg['data'])
                    response = {
                        "message_type": "play_card",
                        "data": response
                    }
                elif msg['message_type'] == 'game_over':
                    self.game_over(msg['data'])
                else:
                    print(RED + self.name + END + " received unknown message type: " + msg['message_type'])
                
                if response:
                    self.send(json.dumps(response))
                    
        except KeyboardInterrupt:
            print(BLUE + self.name + END + " disconnected from the server due to user interruption.")
        #except Exception as e:
        #    print(RED + self.name + END + " encountered an error: " + str(e) + ".")
        finally:
            self.disconnect()
            
    def game_state_update(self, game_state: dict) -> None:
        pass
    
    def bid(self, game_state: dict) -> dict:
        pass
    
    def play_card(self, game_state: dict) -> dict:
        pass
    
    def game_over(self, game_state: dict) -> None:
        pass

"""
class Client:
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def run(self):
        self.connect()
        self.hadle_messages()
    
    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"{BLUE}{self.name}{END} connected to the server.")
        except Exception as e:
            print(f"{RED}{self.name}{END} failed to connect to the server: {str(e)}.")
    
    def send(self, msg):
        try:
            self.socket.sendall(msg.encode())
        except Exception as e:
            print(f"{RED}{self.name}{END} failed to send message to the server: {str(e)}.")
    
    def receive(self):
        try:
            msg = self.socket.recv(4096)
            return msg.decode().rstrip()
        except Exception as e:
            print(f"{RED}{self.name}{END} failed to receive message from the server: {str(e)}.")
            return None
        
    def disconnect(self):
        self.socket.close()
        print(f"{BLUE}{self.name}{END} disconnected from the server.")
    
    def hadle_messages(self):
        try:
            while True:
                msg = self.receive()
                if not msg:
                    break
                
                with open('log.txt', 'a') as f:
                    f.write(f"{msg}\n")
                
                msg = json.loads(msg)
                response = None
                if msg['message_type'] == 'game_state_update':
                    self.game_state_update(msg['data'])
                elif msg['message_type'] == 'bid':
                    response = self.bid(msg['data'])
                    response = {
                        "message_type": "bid",
                        "data": response
                    }
                elif msg['message_type'] == 'play_card':
                    response = self.play_card(msg['data'])
                    response = {
                        "message_type": "play_card",
                        "data": response
                    }
                elif msg['message_type'] == 'game_over':
                    self.game_over(msg['data'])
                else:
                    print(f"{RED}{self.name}{END} received unknown message type: {msg['message_type']}")
                
                if response:
                    self.send(json.dumps(response))
                    
        except KeyboardInterrupt:
            print(f"{BLUE}{self.name}{END} disconnected from the server due to user interruption.")
        #except Exception as e:
        #    print(f"{RED}{self.name}{END} encountered an error: {str(e)}.")
        finally:
            self.disconnect()
    
    def game_state_update(self, game_state: dict) -> None:
        pass
    
    def bid(self, game_state: dict) -> dict:
        pass
    
    def play_card(self, game_state: dict) -> dict:
        pass
    
    def game_over(self, game_state: dict) -> None:
        pass
"""