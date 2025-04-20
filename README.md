# 🧠 Advanced Tic Tac Toe – Pygame Edition

A fun and strategic twist on the classic Tic Tac Toe game, built using **Pygame**. This version introduces a new rule:  
> **Each player can only have 3 active moves on the board.**  
Once a player places a 4th move, their oldest move disappears, adding an exciting rotating mechanic to the game!

---

## 🎮 Features

- Classic 3x3 Tic Tac Toe board.
- Queue-based mechanics (max 3 marks per player).
- Animated menu and end screens.
- Turn-based logic (X starts first).
- Win detection based only on current marks.
- Visual distinction for "oldest" pieces (faded color).

---

## 🛠 Requirements

Make sure you have **Python 3** and **Pygame** installed:

```bash
pip install -r requirements.txt
```

## 🚀 How to Run

run :

```bash
python advanced_tic_tac_toe.py
```

## 🧩 Game Mechanics

* Player X (Player 1) and Player O (Player 2) take turns.
* Each player's moves are tracked using a queue (collections.deque).
* Once a player places their 4th move, their oldest move disappears.
* A player wins if they have 3 active marks in a line (row, column, or diagonal).
* The oldest move is visually faded to indicate it's next to disappear.

## 🖥 Interface Guide

* Menu Screen:
    * Play: Starts the game.
    * Exit: Closes the window.
* Game Screen:
    * Click on any empty cell to place your mark.
    * Marks will fade when they're the oldest and ready to be popped.
    * Game ends when someone wins.
* End Screen:
    * Displays the winner (Player 1 or Player 2).
    * Play Again: Restarts the game.
    * Main Menu: Returns to the main screen.

## 🤖 Future Improvements: AI Agent Integration

To make the game even more exciting, a future version could include an **AI agent opponent**. This agent could analyze the board and make moves using reasoning and strategy. Here are a few ideas for implementing it:

### 🔧 LLM-Powered Agent (with CrewAI or AutoGen)

- Integrate an intelligent agent using frameworks like [**CrewAI**](https://github.com/joaomdmoura/crewai) or [**AutoGen**](https://github.com/microsoft/autogen).
- These frameworks allow LLM-backed agents to take actions in a structured environment.
- The agent would receive the current board state and respond with the best move based on its reasoning.
- Great for simulating a conversational or "thinking" opponent.

### 🧠 How it Might Work
- The game engine sends the board (as a string or JSON) to the agent.
- The agent interprets the state and returns a move (e.g., row and column).
- The agent could optionally explain its thinking process to the player.

## Author
Developed with ❤️ by [Ali FAHS](https://github.com/fahsAli)