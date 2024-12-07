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

Objective:
Be the first player to score 3 points by correctly guessing the location of the hidden marker.

Game Flow:
1. Players are assigned unique IDs upon joining the game.
2. The game alternates between two roles:
   - The hider hides the marker by choosing a position (0-2).
   - The guesser attempts to guess the hidden position.
3. The guesser earns 1 point for each correct guess.
4. Roles switch after each turn, and the game continues until a player scores 3 points.
5. The game automatically announces the winner and resets.

Game State Synchronization:
- The server manages and synchronizes the game state for all connected clients.
- Clients receive updates about the current turn, player moves, and scores after every action.

Winning:
The first player to correctly guess the hidden position three times is declared the winner. After the game ends, players can choose to start a new round or quit.

---

Roadmap

Building on what we have, we would expand the game to allow more than two players to play. The decision for which player the next turn goes to is more complicated than the static arithmetic implemented, since a changing number of players changes the turn number associated with the player hiding the marker. This also requires making a timeout after which a player is removed from the scoreboard for not participating. We would then create a visual UI to animate the act of hiding and revealing a player's guess, as well as celebrating the first to reach the win condition. Lastly, we would allow for the server to host multiple games to allow a new player to select a game where others have not accumulated many points so that the game is fairer.

---

Retrospective

We developed the client-server logic at a good pace using the provided code from the labs. The CLI argument parsing and logging proved to be no issue. We checked every permutation of the game in testing to ensure both clients shared the same state. There was a point where a message could not be correctly decoded on the client side due to timing, so we added a buffer. During presentation, we discovered missing boundary checks for inputs for placing the marker and guessing its location. This could have been checked for by making unit tests to run through the game instead of manually testing the client-server pair. We could have met our goals ahead of each sprint's due date, but overall, progress was timely and decent.

---

Features

- Multiplayer Support: Supports two players connected to a central server.
- Turn-Based Gameplay: Ensures players alternate roles as hider and guesser.
- Real-Time State Updates: Synchronizes game state across all clients after each move.
- Unique Player Identification: Each player is assigned a unique ID, visible in logs and game updates.
- Error Handling: Handles invalid inputs, disconnections, and reconnections gracefully.
- Simple CLI Interface: User-friendly command-line interface for both server and client.

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
- Filip Lewulis
- Corey Valentine

Project Objective:
Create a command-line multiplayer game where players compete to guess the location of a hidden marker.

---

Scope

Inclusions:
- Host server initiating the game upon two players joining.
- Real-time updates for all clients about player moves and game state.
- Turn-based roles for hiding and guessing.
- A winning condition (first to 3 correct guesses).
- Graceful error handling for invalid inputs and disconnections.

Exclusions:
- Usability on platforms other than Windows.
- Graphical user interface (GUI).

---

Deliverables

1. Fully functional server.py and client.py scripts.
2. requirements.txt for environment setup.
3. Detailed documentation in this README file.

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
- The server manages and synchronizes the game state.
- The game can have more than two players in the future, but currently supports only two.

---

Roles and Responsibilities

- Corey Valentine: QA tester and primary code reviewer.
- Filip Lewulis: Project manager and feature developer.

---

Communication Plan

- Updates and decisions communicated via Discord.
- Backup communication through text messaging and Canvas.

---

Logs and Debugging

- All server logs are stored in logs/server.log.
- All client logs are stored in logs/client.log.
- Logs include details about player connections, disconnections, moves, and game events.

---

Error Handling

- Invalid Inputs: Prompts users to re-enter valid values for guesses or marker positions.
- Network Errors: Detects disconnections and ensures the remaining player is notified.
- Game State Integrity: Synchronizes state after any error or unexpected condition.
- Unexpected Behavior: Logs details of issues for debugging and troubleshooting.

---

Integration Testing

1. Test player connection/disconnection scenarios.
2. Simulate a game with valid and invalid inputs to ensure stability.
3. Verify state synchronization across clients during gameplay.
4. Validate end-to-end functionality by completing multiple game rounds.

---

Security/Risk Evaluation

- Potential Risks:
  1. Unauthorized clients attempting to connect.
  2. Players exploiting input mechanisms to disrupt the game.
  3. Data integrity issues if messages are malformed.

- Mitigation:
  1. Add basic authentication or whitelisting of IPs.
  2. Validate all inputs and sanitize messages.
  3. Use checksum or hashing mechanisms to verify message integrity.

---

Example Gameplay

Initial Game State:
Game State:
Turn: Player 1
Scores: {'1': 0, '2': 0}

Player 1 hides the marker:
Choose a position to hide the marker (0-2): 1
Player 1 has hidden the marker!

Player 2 guesses the marker's position:
Enter 'play' to make a move, or 'quit' to exit: play
Guess the position of the marker (0-2): 1
Player 2 guessed correctly!

Updated Scores:
Game State:
Turn: Player 1
Scores: {'1': 0, '2': 1}

---

Requirements File

To recreate the development environment, use the requirements.txt file:
pip install -r requirements.txt

