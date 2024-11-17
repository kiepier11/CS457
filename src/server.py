import socket
import threading
import logging
import os
import json
import argparse

class TCPServer:
    def __init__(self, host='0.0.0.0', port=12345, max_clients=5):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.clients = []  # List of (socket, player_id)
        self.game_state = {"players": {}, "turn": None, "moves": []}
        self.player_count = 0

        self._setup_logging()
        self.server_socket = self._create_server_socket()

    def _setup_logging(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(filename='logs/server.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def _create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.max_clients)
        logging.info(f"Server started on {self.host}:{self.port}")
        return server_socket

    def handle_client(self, client_socket, client_address):
        self.player_count += 1
        player_id = self.player_count
        self.clients.append((client_socket, player_id))
        self.game_state["players"][player_id] = {"id": player_id, "address": client_address}

        logging.info(f"Client {client_address} connected as Player {player_id}.")
        self._broadcast_state()

        try:
            while True:
                message = self._receive_message(client_socket, client_address)
                if message is None:
                    break
                self._process_message(client_socket, player_id, message)
        except Exception as e:
            logging.error(f"Error with client {client_address}: {e}")
        finally:
            self._close_client_connection(client_socket, client_address, player_id)

    def _receive_message(self, client_socket, client_address):
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                return None
            return json.loads(message)
        except Exception as e:
            logging.error(f"Error receiving message from {client_address}: {e}")
            return None

    def _send_message(self, client_socket, message):
        try:
            client_socket.send(json.dumps(message).encode())
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def _broadcast_state(self):
        """Broadcast the updated game state to all connected clients."""
        state_message = {"type": "game_state", "state": self.game_state}
        for client_socket, _ in self.clients:
            self._send_message(client_socket, state_message)

    def _process_message(self, client_socket, player_id, message):
        message_type = message.get("type")
        if message_type == "join":
            logging.info(f"Player {player_id} joined.")
        elif message_type == "move":
            position = message.get("position")
            logging.info(f"Player {player_id} made a move: {position}")
            self.game_state["moves"].append({"player": player_id, "position": position})
            self.game_state["turn"] = (player_id % self.player_count) + 1
            self._broadcast_state()
        elif message_type == "quit":
            logging.info(f"Player {player_id} quit.")
            self._close_client_connection(client_socket, None, player_id)

    def _close_client_connection(self, client_socket, client_address, player_id):
        client_socket.close()
        self.clients = [c for c in self.clients if c[0] != client_socket]
        if player_id in self.game_state["players"]:
            del self.game_state["players"][player_id]
        self._broadcast_state()
        logging.info(f"Player {player_id} disconnected.")

    def start(self):
        logging.info("Starting server...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Server for Multiplayer Game")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port to bind the server")
    args = parser.parse_args()

    server = TCPServer(port=args.port)
    server.start()
