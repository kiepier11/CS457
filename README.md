Guessing Game

This is a simple multiplayer guessing game implemented using Python and sockets. Players take turns hiding a marker under a "cup," and their opponents must guess the correct position. The first player to guess correctly three times wins!

---

How to Run the Game

Server:
1. Navigate to the directory containing server.py.
2. Start the server by specifying the port:
   python server.py -p <port>
   Example:
   python server.py -p 12345
3. The server will start and wait for clients to connect. 

Client:
1. Navigate to the directory containing client.py.
2. Connect to the server by providing the server's IP and port:
   python client.py -i <server_ip> -p <port>
   Example:
   python client.py -i 127.0.0.1 -p 12345
3. After connecting, follow the prompts to play the game:
   - Enter your guess when it's your turn.
   - Use the command quit to leave the game.

---

Gameplay

Objective: Be the first player to guess the location of the marker three times.

Game Flow:
- Players are assigned unique IDs and take turns guessing the position of a hidden marker.
- The server updates and synchronizes the game state across all connected clients after every move.

Game State Synchronization:
- All clients will receive updates about the current turn, player moves, and the state of the game board.
- The game will automatically announce the winner or notify players of a draw.

Winning: The first player to guess the correct location three times is declared the winner.

---

Features

- Multiplayer Support: Supports multiple clients connecting to a single server.
- Turn-Based Gameplay: Ensures players take turns guessing.
- Real-Time State Updates: Synchronizes the game state across all clients after each move.
- Unique Player Identification: Each player is assigned a unique ID, visible in logs and game state updates.
- Resilient Connections: Handles disconnections gracefully and notifies remaining players.
- Simple CLI Interface: Easy-to-use command-line interface for both server and client.

---

Technologies Used

- Python Libraries:
  - socket: For networking and communication.
  - threading: For handling multiple client connections.
  - json: For message serialization and deserialization.
  - argparse: For handling command-line arguments.
  - logging: For detailed logs.

---

Project Statement of Work (SOW)

Team:
Filip Lewulis & Corey Valentine

Project Objective:
Create a command-line multiplayer game where players compete to guess the location of a hidden marker.

---

Scope

Inclusions:
- Host server initiating the game upon 2 or more players joining.
- Real-time updates for all clients about player moves and game state.
- Random player assignment for the first turn.
- A winning condition (first to 3 correct guesses).
- Resilient connection handling and error messages.

Exclusions:
- Usability on Windows OS only (other platforms not guaranteed).
- Graphical user interface (GUI).

---

Deliverables

- Fully functional server.py and client.py scripts.
- Updated requirements.txt for dependencies.
- Documentation in this README file.

---

Timeline

Key Milestones:
1. Basic Client-Server Communication: By October 6
2. Turn-Based Gameplay & Input Handling: By October 20
3. Game State Synchronization: By November 3
4. Winning Conditions & Game Over Logic: By November 17
5. Final Testing & Error Handling: By December 6

---

Technical Requirements

Hardware:
- 1GB hard disk, 1GB RAM, 320x480 screen or better.

Software:
- Python 3.8 or higher.

---

Assumptions

- All transmissions utilize TCP.
- The server is the single point of truth for the game state.
- The game can have more than two players, but only one player takes a turn at a time.

---

Roles and Responsibilities

- Corey Valentine: QA tester and primary code reviewer.
- Filip Lewulis: Project manager and feature developer.

---

Communication Plan

- Updates and decisions communicated via Discord.
- Backup communication through text messaging and Canvas.

---

Future Enhancements (Optional)

- Add chat functionality for player communication.
- Implement point tracking and statistics for completed games.
- Introduce more game modes or difficulties.

---

Requirements File

To recreate the development environment, use the requirements.txt file:
pip install -r requirements.txt

---

Logs and Debugging

- All server logs are stored in logs/server.log.
- All client logs are stored in logs/client.log.
- Logs include details about player connections, disconnections, and game events.

---
