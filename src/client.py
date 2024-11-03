import socket
import logging
import json
import os

class TCPClient:
    def __init__(self, server_ip='127.0.0.1', server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = "player1"
        self.player_id = None
        self.game_state = None

        self._setup_logging()
        self.client_socket = self._create_client_socket()

    def _setup_logging(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(filename='logs/client.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def _create_client_socket(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.server_ip, self.server_port))
            logging.info(f"Connected to {self.server_ip}:{self.server_port}")
            print(f"Connected to {self.server_ip}:{self.server_port}")
            return client_socket
        except socket.error as e:
            logging.error(f"Failed to connect to server: {e}")
            print(f"Failed to connect to server: {e}")
            return None

    def send_message(self, message):
        if not self.client_socket:
            logging.error("No connection to the server.")
            return

        try:
            self.client_socket.send(json.dumps(message).encode())
            response = self._receive_message()
            if response:
                self._handle_server_response(response)
        except (BrokenPipeError, socket.error) as e:
            logging.error(f"Communication error: {e}")

    def _receive_message(self):
        try:
            response = self.client_socket.recv(1024).decode()
            return json.loads(response)
        except Exception as e:
            logging.error(f"Error receiving message: {e}")
            return None

    def close_connection(self):
        if not self.client_socket:
            logging.error("No connection to close.")
            return

        try:
            self.client_socket.close()
            logging.info("Connection closed.")
            print("Connection closed.")
        except socket.error as e:
            logging.error(f"Failed to close connection: {e}")

    def join_game(self):
        join_message = {"type": "join", "username": self.username}
        self.send_message(join_message)

    def make_guess(self):
        if self.game_state and self.game_state["turn"] == self.player_id:
            position = int(input('Pick a cup [1], [2], [3]: '))
            guess_message = {"type": "move", "position": position}
            self.send_message(guess_message)
        else:
            print("It's not your turn yet!")

    def _handle_server_response(self, response):
        if response["type"] == "game_state":
            self.game_state = response["state"]
            self.display_game_state()
        elif response["type"] == "join_ack":
            self.player_id = response["player_id"]
            print(f"Welcome {self.username}, your player ID is {self.player_id}.")
        elif response["type"] == "chat":
            print(f"[Player {response['player_id']}]: {response['message']}")
        elif response["type"] == "error":
            print(response["message"])

    def display_game_state(self):
        print("\nCurrent Game State:")
        print(f"Turn: Player {self.game_state['turn']}")
        print("Positions:", self.game_state["positions"])
        print("Players:", [p["id"] for p in self.game_state["players"]])
        print()

    def chat(self, message):
        chat_message = {"type": "chat", "message": message}
        self.send_message(chat_message)

# Example usage
if __name__ == "__main__":
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 12345

    client = TCPClient(server_ip=SERVER_IP, server_port=SERVER_PORT)

    if client.client_socket:
        client.join_game()
        client.make_guess()  # To make a move
        client.chat("Hello, everyone!")  # To send a chat message
