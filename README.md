# Guessing Game

This is a simple guessing game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals.
3. **Play the game:** Players take turns hiding a marker under a cup while opponents have to guess under which cup the marker lies. The first player to guess correctly three times wins!

**Technologies used:**
* Python
* Sockets

# Project Statement of Work (SOW)

### Team:
**Filip Lewulis & Corey Valentine**

### Project Objective:
**Create a visual CLI game of chance where the first player to correctly guess the location of the marker hidden by the other player to win.**

---

### Scope:

#### Inclusions:
- Host server initiating game upon 2 or more players joining
- Game timeout upon 1 or few players after 1 minute
- Random dealer assignment
- Point tracking and and game win after 3 correct guesses
- Dealer marker selection
- Player cup selection
- Player timeout
- Connection error messages

#### Exclusions:
- Usability on Windows OS
- User login information

---

### Deliverables:
- Python script
- List of additional libraries
- Final documentation and presentation

---

### Timeline:

#### Key Milestones:
- Client server with dealer assignment by October 6
- Marker and cup selection input and messages by October 20
- Interface, help menu, and ASCII art by November 3
- Point system and win state by November 17
- Error handling and final testing by December 6

#### Task Breakdown:
- server.py game instance [1 hr]
- client.py connection [1hr]
- marker/cup selection input and error handling [1 hr]
- ASCII render [0.5 hr]
- Dealer assignment [0.5 hr]
- Point tracking system and game reset [1 hr]
- Help menu [0.5 hr]
- Player timeout [0.5 hr]
- Connection error messages [1 hr]

---

### Technical Requirements:

#### Hardware:
- 1GB hard disk, 1GB RAM, 320x480 screen or better

#### Software:
- The game will utilize the Python socket and threading libraries.
- The built-in terminal and IDE terminal will be the game interface.

---

### Assumptions:
- All transmissions utilize TCP.
- There is only one server that players can join.
- By default the number of cup options is 3.

---

### Roles and Responsibilities:
- Corey is responsible as QA tester and board chairman.
- Filip is responsible as art director and project manager.

---

### Communication Plan:
- Communication of updates and decisions will be done via Discord, with text messaging and Canvas as a backup means.

---

### Additional Notes:
- If time permits, communications will be encrypted between each client and the server
