import socket
import logging
import json
import os
import argparse
import threading

class TCPClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.game_state = None
        self.running = True

        self._setup_logging()
        self.connect_to_server()

    def _setup_logging(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(filename='logs/client.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.server_port))
            logging.info(f"Connected to {self.server_ip}:{self.server_port}")
            threading.Thread(target=self.listen_for_messages, daemon=True).start()
        except Exception as e:
            logging.error(f"Error connecting to server: {e}")

    def listen_for_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                self._handle_server_response(json.loads(message))
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
                self.running = False

    def _handle_server_response(self, response):
        if response["type"] == "game_state":
            self.game_state = response["state"]
            self.display_game_state()
        elif response["type"] == "join_ack":
            print(response["message"])

    def send_message(self, message):
        try:
            self.client_socket.send(json.dumps(message).encode())
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def make_move(self):
        position = int(input("Enter position (1-3): "))
        self.send_message({"type": "move", "position": position})

    def display_game_state(self):
        print("\nGame State:")
        print(json.dumps(self.game_state, indent=4))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Client for Multiplayer Game")
    parser.add_argument("-i", "--ip", type=str, required=True, help="Server IP address")
    parser.add_argument("-p", "--port", type=int, required=True, help="Server port")
    args = parser.parse_args()

    client = TCPClient(server_ip=args.ip, server_port=args.port)
    client.send_message({"type": "join"})

    while client.running:
        command = input("Enter 'move' to make a move, or 'quit' to exit: ").strip().lower()
        if command == "move":
            client.make_move()
        elif command == "quit":
            client.running = False
            client.send_message({"type": "quit"})
