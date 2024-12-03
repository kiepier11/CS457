import socket
import threading
import logging
import json
import os
import argparse


class TCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.player_id = None
        self.game_state = {"players": {}}
        self.running = True

        self._setup_logging()
        self.connect_to_server()

    def _setup_logging(self):
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(filename="logs/client.log", level=logging.DEBUG,
                            format="%(asctime)s - %(levelname)s - %(message)s")

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            logging.info(f"Connected to {self.server_ip}:{self.server_port}")
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
        except Exception as e:
            logging.error(f"Error connecting to server: {e}")
            print("Failed to connect to the server. Please check the connection details.")

    def listen_for_messages(self):
        buffer = ""
        while self.running:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    logging.warning("Disconnected from server.")
                    self.running = False
                    break
                buffer += data
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                self._handle_server_response(json.loads(message))
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
                self.running = False

    def _handle_server_response(self, response):
        if response["type"] == "join_ack":
            self.player_id = response["player_id"]
            print(response["message"])
        elif response["type"] == "game_state":
            self.game_state = response["state"]
            self.display_game_state()
        elif response["type"] == "message":
            print(response["message"])
            if response["message"] == f"Player {self.player_id} wins!":
                print("You win!")
            elif response["message"] == f"Player {(self.player_id + 1)%2} wins!":
                print("You lose!")

    def send_message(self, message):
        try:
            self.client_socket.send(json.dumps(message).encode())
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def play_turn(self):
        if not self.game_state:
            print("Game state not available yet. Please wait.")
            return

        print(f"Player ID: {self.player_id}, Current Turn: {self.game_state['turn']}, Current Hider: {self.game_state['current_hider']}")

        # Determine if it's the player's turn
        if self.game_state["turn"] % 4 < 2 and self.player_id == 1 or \
        self.game_state["turn"] % 4 >= 2 and self.player_id == 2:
            # Hider Role
            if self.game_state["current_hider"] == self.player_id:
                position = int(input("Choose a position to hide the marker (0-2): "))
                self.send_message({"type": "hide", "position": position})
            else:  # Guesser Role
                position = int(input("Guess the position of the marker (0-2): "))
                self.send_message({"type": "guess", "position": position})
        else:
            print("Waiting for the other player to make their move.")
            return

    def display_game_state(self):
        print("\nGame State:")
        print(f"Turn: Player {1 if self.game_state['turn'] % 4 in [1, 2] else 2}")
        print(f"Scores: {self.game_state['scores']}")
        print()

    def close_connection(self):
        self.running = False
        self.client_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Client for Multiplayer Game")
    parser.add_argument("-i", "--ip", type=str, required=True, help="Server IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server port")
    args = parser.parse_args()

    client = TCPClient(server_ip=args.ip, server_port=args.port)

    while client.running:
        if len(client.game_state["players"]) == 2:
            command = input("Enter 'play' to make a move, or 'quit' to exit\n").strip().lower()
            if command == "play":
                client.play_turn()
            elif command == "quit":
                client.running = False
                client.send_message({"type": "quit"})
