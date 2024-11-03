import socket
import threading
import logging
import os
import random
import json


class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345, max_clients=5, timeout=60):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.timeout = timeout
        self.clients = []
        self.game_state = {"turn": None, "positions": {}, "players": []}
        self.current_turn = 0  # To manage turns

        self._setup_logging()
        self.server_socket = self._create_server_socket()

    def _setup_logging(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(filename='logs/server.log', level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def _create_server_socket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(self.timeout)
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.max_clients)
        print(f"Server started on {self.host}:{self.port}")
        logging.info(f"Server started on {self.host}:{self.port}")
        return server_socket

    def handle_client(self, client_socket, client_address):
        logging.info(f"Client {client_address} connected.")
        print(f"Client {client_address} connected.")
        player_id = len(self.clients) + 1  # Unique player ID
        self.clients.append((client_socket, player_id))
        self.game_state["players"].append({"id": player_id, "address": client_address})

        # If this is the first player, they get the first turn
        if self.current_turn == 0:
            self.current_turn = player_id
            self.game_state["turn"] = player_id

        try:
            while True:
                message = self._receive_message(client_socket)
                if message is None:
                    break
                self._process_message(client_socket, player_id, message)

        except (ConnectionResetError, socket.timeout) as e:
            self._handle_client_error(e, client_address)
        finally:
            self._close_client_connection(client_socket, client_address, player_id)

    def _receive_message(self, client_socket):
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                return None
            return json.loads(message)
        except Exception as e:
            logging.error(f"Error receiving message: {e}")
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
            self._handle_join(client_socket, player_id, message)
        elif message_type == "move":
            self._handle_move(client_socket, player_id, message)
        elif message_type == "quit":
            self._handle_quit(client_socket, player_id, message)
        elif message_type == "chat":
            self._handle_chat(player_id, message)

    def _handle_join(self, client_socket, player_id, message):
        username = message.get("username")
        response = {"type": "join_ack", "message": f"Welcome {username}!", "player_id": player_id}
        self._send_message(client_socket, response)
        self._broadcast_state()

    def _handle_move(self, client_socket, player_id, message):
        if self.game_state["turn"] != player_id:
            self._send_message(client_socket, {"type": "error", "message": "Not your turn!"})
            return

        position = message.get("position")
        self.game_state["positions"][player_id] = position  # Record the move
        self._advance_turn()  # Move to the next player's turn
        self._broadcast_state()

    def _handle_quit(self, client_socket, player_id, message):
        username = message.get("username")
        response = {"type": "quit_ack", "message": f"Goodbye {username}!"}
        self._send_message(client_socket, response)
        self._close_client_connection(client_socket, client_address=None, player_id=player_id)

    def _handle_chat(self, player_id, message):
        chat_message = {"type": "chat", "player_id": player_id, "message": message.get("message")}
        for client_socket, _ in self.clients:
            self._send_message(client_socket, chat_message)

    def _advance_turn(self):
        player_ids = [player["id"] for player in self.game_state["players"]]
        current_index = player_ids.index(self.current_turn)
        next_index = (current_index + 1) % len(player_ids)
        self.current_turn = player_ids[next_index]
        self.game_state["turn"] = self.current_turn

    def _close_client_connection(self, client_socket, client_address=None, player_id=None):
        client_socket.close()
        self.clients = [(sock, pid) for sock, pid in self.clients if pid != player_id]
        self.game_state["players"] = [p for p in self.game_state["players"] if p["id"] != player_id]
        logging.info(f"Player {player_id} disconnected.")
        print(f"Player {player_id} disconnected.")
        self._broadcast_state()

    def start(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
            except socket.timeout:
                logging.error("Server timed out waiting for a connection.")
                print("Server timed out waiting for a connection.")


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 12345
    MAX_CLIENTS = 5
    TIMEOUT = 60

    server = TCPServer(host=HOST, port=PORT, max_clients=MAX_CLIENTS, timeout=TIMEOUT)
    server.start()
