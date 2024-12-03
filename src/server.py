import socket
import threading
import logging
import os
import json
import argparse


class TCPServer:
    def __init__(self, host="0.0.0.0", port=12345, max_clients=2):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.clients = []
        self.game_state = {"players": {}, "turn": 1, "key_position": None, "scores": {}, "current_hider": 1}
        self.player_count = 0

        self._setup_logging()
        self.server_socket = self._create_server_socket()

    def _setup_logging(self):
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(filename="logs/server.log", level=logging.DEBUG,
                            format="%(asctime)s - %(message)s")

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
        self.game_state["scores"][player_id] = 0

        self._send_message(client_socket, {
            "type": "join_ack",
            "player_id": player_id,
            "message": f"Welcome! You are Player {player_id}."
        })

        logging.info(f"Player {player_id} joined.")
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
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding message from {client_address}: {e}")
            return None

    def _send_message(self, client_socket, message):
        try:
            client_socket.send((json.dumps(message)+"\n").encode())
        except Exception as e:
            logging.error(f"Error sending message: {e}")

    def _broadcast_message(self, message):
        for client_socket, _ in self.clients:
            logging.debug(f"Broadcasting message: {message}")
            try:
                self._send_message(client_socket, {"type": "message", "message": message})
            except Exception as e:
                logging.error(f"Error broadcasting state to a client: {e}")
                self._close_client_connection(client_socket, None, _)

    def _broadcast_state(self):
        state_message = {"type": "game_state", "state": self.game_state}
        for client_socket, _ in self.clients:
            self._send_message(client_socket, state_message)

    def _process_message(self, client_socket, player_id, message):
        message_type = message.get("type")
        if message_type == "hide":
            position = message.get("position")
            self.game_state["key_position"] = position
            self._broadcast_message(f"Player {player_id} has hidden the marker!")
            self._switch_turn()
        elif message_type == "guess":
            guess = message.get("position")
            if guess == self.game_state.get("key_position"):
                self.game_state["scores"][player_id] += 1
                self._broadcast_message(f"Player {player_id} guessed correctly!")
                self._check_winner()
            else:
                self._broadcast_message(f"Player {player_id} guessed incorrectly!")
            self._switch_turn()
        elif message_type == "quit":
            logging.info(f"Player {player_id} quit.")
            self._close_client_connection(client_socket, None, player_id)

    def _switch_turn(self):
        # Alternate hider and guesser roles every other turn
        turn = self.game_state["turn"] + 1
        self.game_state["turn"] = turn
        self.game_state["current_hider"] = 1 if turn % 4 in [1, 2] else 2
        self.game_state["key_position"] = self.game_state["key_position"]
        self._broadcast_state()

    def _check_winner(self):
        for player_id, score in self.game_state["scores"].items():
            if score >= 3:
                print(f"Player {player_id} wins!")
                self._broadcast_message(f"Player {player_id} wins!")
                self._reset_game()

    def _reset_game(self):
        self.game_state["scores"] = {player_id: 0 for player_id in self.game_state["scores"]}
        self.game_state["key_position"] = None
        self.game_state["turn"] = 1
        self.game_state["current_hider"] = 1
        self._broadcast_state()

    def _close_client_connection(self, client_socket, client_address, player_id):
        client_socket.close()
        self.clients = [c for c in self.clients if c[0] != client_socket]
        if player_id in self.game_state["players"]:
            del self.game_state["players"][player_id]
        self._broadcast_message(f"Player {player_id} has disconnected!")
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
