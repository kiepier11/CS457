import socket
import logging
import json
import os

class TCPClient:
    """A simple TCP Client to communicate with the TCP Server."""

    def __init__(self, server_ip='127.0.0.1', server_port=12345):
        self.server_ip = server_ip
        self.server_port = server_port
        self.username = "player1"
        self.current_guess = 0

        self._setup_logging()
        self.client_socket = self._create_client_socket()

    def _setup_logging(self):
        """Set up logging to file for client events and errors."""
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(filename='logs/client.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def _create_client_socket(self):
        """Create and connect the client socket to the server."""
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
        """Send a message to the server."""
        if not self.client_socket:
            logging.error("No connection to the server.")
            return

        try:
            self.client_socket.send(json.dumps(message).encode())
            response = self._receive_message()
            print(f"Server response: {response}")
        except BrokenPipeError:
            logging.error("Connection lost during communication.")
        except socket.error as e:
            logging.error(f"Communication error: {e}")

    def _receive_message(self):
        """Receive a message from the server."""
        try:
            response = self.client_socket.recv(1024).decode()
            return json.loads(response)
        except Exception as e:
            logging.error(f"Error receiving message: {e}")
            return None

    def close_connection(self):
        """Close the connection to the server."""
        if not self.client_socket:
            logging.error("No connection to close.")
            return

        try:
            self.client_socket.close()
            logging.info("Connection closed.")
            print("Connection closed.")
        except socket.error as e:
            logging.error(f"Failed to close connection: {e}")

    def make_guess(self):
        """Prompt the user for a guess and send the message to the server."""
        self.current_guess = int(input('Pick a cup [1], [2], [3]: '))
        guess_message = {"type": "move", "guess": self.current_guess}
        self.send_message(guess_message)

    def join_game(self):
        """Send a join request to the server."""
        join_message = {"type": "join", "username": self.username}
        self.send_message(join_message)

    def quit_game(self):
        """Send a quit message to the server."""
        quit_message = {"type": "quit", "username": self.username}
        self.send_message(quit_message)
        self.close_connection()

# Example usage
if __name__ == "__main__":
    SERVER_IP = '127.0.0.1'
    SERVER_PORT = 12345

    client = TCPClient(server_ip=SERVER_IP, server_port=SERVER_PORT)

    if client.client_socket:  # Proceed if connected successfully
        client.join_game()
        client.make_guess()
        client.quit_game()
