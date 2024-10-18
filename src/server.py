import socket
import threading
import logging
import os
import random

class TCPServer:
    """A simple TCP Server that can handle multiple clients."""

    def __init__(self, host='127.0.0.1', port=12345, max_clients=5, timeout=60):
        """Initialize the server with given host, port, max clients, and timeout."""
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.timeout = timeout
        self.message = {}
        self.ball_location = 0
        self.scores = {}

        self._setup_logging()
        self.server_socket = self._create_server_socket()

    def _setup_logging(self):
        """Set up logging to file for server events and errors."""
        os.makedirs('logs', exist_ok=True)  # Create logs directory if it doesn't exist
        logging.basicConfig(
            filename='logs/server.log', level=logging.DEBUG,  # Logs are stored in the logs directory
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _create_server_socket(self):
        """Create and configure the server socket."""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(self.timeout)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.max_clients)
        print(f"Server started on {self.host}:{self.port} "
              f"with max clients: {self.max_clients}")
        logging.info(f"Server started on {self.host}:{self.port}")
        return server_socket

    def handle_client(self, client_socket, client_address):
        """Handle communication with a connected client."""
        logging.info(f"Client {client_address} connected.")
        self.scores[client_address] = 0
        print(f"Client {client_address} connected.")

        try:
            while True:
                message = self._receive_message(client_socket, client_address)
                if message is None:
                    break
                self._send_message(client_socket, f"Message received: {message}")

        except (ConnectionResetError, socket.timeout) as e:
            self._handle_client_error(e, client_address)
        finally:
            self._close_client_connection(client_socket, client_address)

    def _receive_message(self, client_socket, client_address):
        """Receive message from client and log it."""
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                logging.info(f"Client {client_address} disconnected.")
                return None
            print(f"Received from {client_address}: {message}")
            self.message = message
        except Exception as e:
            logging.error(f"Error receiving message from {client_address}: {e}")
            return None

    def _send_message(self, client_socket):
        """Send a message to the client."""
        try:
            client_socket.send(self.message.encode())
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def _handle_client_error(self, error, client_address):
        """Handle errors related to client connection."""
        if isinstance(error, ConnectionResetError):
            logging.error(f"Connection reset by client {client_address}")
        elif isinstance(error, socket.timeout):
            logging.error(f"Client {client_address} timed out")
        print(f"Error with client {client_address}: {error}")

    def _close_client_connection(self, client_socket, client_address):
        """Close the client socket and log the disconnection."""
        client_socket.close()
        logging.info(f"Client {client_address} disconnected.")
        print(f"Client {client_address} disconnected.")

    def start(self):
        """Start the server and accept incoming client connections."""
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                ).start()
            except socket.timeout:
                logging.error("Server timed out waiting for a connection.")
                print("Server timed out waiting for a connection.")
            except Exception as e:
                logging.error(f"Error accepting connection: {e}")
                print(f"Error accepting connection: {e}")

    def pick_random(self):
        """Pick random ball location between 1 and 3"""
        self.ball_location = random.randrange(1,4)
        
    def round_start_msg(self):
        """Round start message"""
        self.message = {'start': True}

    def answer_msg(self):
        """Ball location message"""
        self.message = {'answer': self.ball_location}

    def winner_msg(self, client):
        """Round end message with player score"""
        self.message = {'start': False, 'score': self.scores[client]}

# Example usage
if __name__ == "__main__":
    # Configuration values can be easily changed
    HOST = '127.0.0.1'
    PORT = 12345
    MAX_CLIENTS = 5
    TIMEOUT = 60

    server = TCPServer(host=HOST, port=PORT, max_clients=MAX_CLIENTS, timeout=TIMEOUT)
    server.start()
