import socket
import threading
import logging
import os
import json

class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345, max_clients=5, timeout=300):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.timeout = timeout
        self.clients = []
        self.player_count = 0  # Track the number of players

        self._setup_logging()
        self.server_socket = self._create_server_socket()

    def _setup_logging(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(filename='logs/server.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def _create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allows reuse of the address
        server_socket.settimeout(self.timeout)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.max_clients)
        logging.info(f"Server started on {self.host}:{self.port}")
        return server_socket

    def handle_client(self, client_socket, client_address):
        self.player_count += 1  # Increment player count
        player_id = self.player_count  # Assign a unique player ID
        logging.info(f"Client {client_address} connected as Player {player_id}.")

        # Send the player ID to the client on join
        join_ack = {"type": "join_ack", "player_id": player_id, "message": f"Welcome, Player {player_id}!"}
        self._send_message(client_socket, join_ack)

        try:
            while True:
                message = self._receive_message(client_socket, client_address)
                if message is None:
                    break  # Client disconnected or message was empty
                self._process_message(client_socket, player_id, message)
        except Exception as e:
            logging.error(f"Error with client {client_address}: {e}")
        finally:
            self._close_client_connection(client_socket, client_address)

    def _receive_message(self, client_socket, client_address):
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                logging.info(f"Client {client_address} disconnected.")
                return None
            logging.info(f"Received from {client_address}: {message}")
            return json.loads(message)
        except (json.JSONDecodeError, ConnectionResetError, socket.error) as e:
            logging.error(f"Error receiving message from {client_address}: {e}")
            return None

    def _send_message(self, client_socket, message):
        try:
            client_socket.send(json.dumps(message).encode())
        except (BrokenPipeError, socket.error) as e:
            logging.error(f"Error sending message: {e}")

    def _process_message(self, client_socket, player_id, message):
        message_type = message.get("type")
        if message_type == "join":
            logging.info(f"Player {player_id} joined the game.")
            # No need to respond since join_ack was already sent on connect
        elif message_type == "move":
            position = message.get("position")
            logging.info(f"Player {player_id} made a move to position {position}")
            # Process move logic here
            response = {"type": "move_ack", "message": f"Move received for Player {player_id}", "position": position}
            self._send_message(client_socket, response)
        elif message_type == "quit":
            logging.info(f"Player {player_id} quit the game.")
            response = {"type": "quit_ack", "message": f"Goodbye, Player {player_id}!"}
            self._send_message(client_socket, response)

    def _close_client_connection(self, client_socket, client_address):
        client_socket.close()
        self.clients = [c for c in self.clients if c[0] != client_socket]
        logging.info(f"Client {client_address} disconnected.")

    def start(self):
        logging.info("Starting server...")
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
            except socket.timeout:
                logging.info("Server timed out waiting for a connection.")

if __name__ == "__main__":
    server = TCPServer()
    server.start()
