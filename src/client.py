import socket
import logging
import json
import os
import time


class TCPClient:
    def __init__(self, server_ip='127.0.0.1', server_port=12345, retry_attempts=5, retry_delay=2):
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = "player1"
        self.player_id = None
        self.game_state = None
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.connected = False

        self._setup_logging()
        self.connect_to_server()

    def _setup_logging(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(filename='logs/client.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def connect_to_server(self):
        attempts = 0
        while attempts < self.retry_attempts and not self.connected:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.server_ip, self.server_port))
                logging.info(f"Connected to {self.server_ip}:{self.server_port}")
                print(f"Connected to {self.server_ip}:{self.server_port}")
                self.connected = True
            except socket.error as e:
                logging.error(f"Connection attempt {attempts + 1} failed: {e}")
                print(f"Connection attempt {attempts + 1} failed, retrying...")
                attempts += 1
                time.sleep(self.retry_delay)

        if not self.connected:
            logging.error("Failed to connect to server after multiple attempts.")
            print("Failed to connect to server after multiple attempts.")

    def send_message(self, message):
        if not self.connected:
            logging.error("Not connected to server.")
            return

        try:
            self.client_socket.send(json.dumps(message).encode())
            response = self._receive_message()
            if response:
                self._handle_server_response(response)
        except (BrokenPipeError, socket.error) as e:
            logging.error(f"Communication error: {e}")
            self.connected = False
            self.reconnect()

    def _receive_message(self):
        try:
            response = self.client_socket.recv(1024).decode()
            if response:
                return json.loads(response)
            return None
        except (json.JSONDecodeError, socket.error) as e:
            logging.error(f"Error receiving message: {e}")
            self.connected = False
            self.reconnect()
            return None

    def reconnect(self):
        logging.info("Attempting to reconnect...")
        self.connect_to_server()

    def close_connection(self):
        if self.client_socket:
            try:
                self.client_socket.close()
                logging.info("Connection closed.")
                print("Connection closed.")
            except socket.error as e:
                logging.error(f"Failed to close connection: {e}")
            finally:
                self.connected = False

    def join_game(self):
        if self.connected:
            join_message = {"type": "join", "username": self.username}
            self.send_message(join_message)

    def make_guess(self):
        if self.connected:
            position = int(input('Pick a cup [1], [2], [3]: '))
            guess_message = {"type": "move", "position": position}
            self.send_message(guess_message)

    def _handle_server_response(self, response):
        if response["type"] == "join_ack":
            print(response["message"])
        elif response["type"] == "move_ack":
            print(response["message"])
        elif response["type"] == "quit_ack":
            print(response["message"])


# Example usage
if __name__ == "__main__":
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 12345

    client = TCPClient(server_ip=SERVER_IP, server_port=SERVER_PORT)

    if client.connected:
        client.join_game()
        while client.connected:
            command = input("Enter 'move' to make a guess or 'quit' to exit: ").strip().lower()
            if command == "move":
                client.make_guess()
            elif command == "quit":
                client.close_connection()
                break
            else:
                print("Invalid command. Please enter 'move' or 'quit'.")

