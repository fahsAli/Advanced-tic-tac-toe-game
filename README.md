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


## 🎮 Advanced Tic Tac Toe - With AI Support (CrewAI + Ollama)

This is a feature-rich version of Tic Tac Toe including:
- Player vs Player mode
- Player vs AI mode with LLM-based decision-making
- Unique gameplay: each player is limited to 3 pieces on the board

### 📦 Requirements:
- Python
- Pygame
- CrewAI
- LangChain
- Ollama running locally with a compatible model (e.g., llama3)

### 🧠 AI Integration:
The AI opponent uses the CrewAI framework to analyze the current board and suggest the optimal move.
You need to have Ollama running locally with the model pulled to use AI mode.

### 🔧 Setup Instructions:
1. Install Python dependencies:
```bash
   pip install -r requirements.txt
```

2. Install Ollama (macOS/Linux/Windows):
   https://ollama.com/download

3. Pull the LLM model (we use llama3 in this script):
```bash
   ollama pull llama3.2
```
    Or you can modify the `MODEL` variable if using another supported model:
    MODEL = "llama3"  # or "mistral" / "gemma" etc.

4. Run Ollama server in background:
```bash
   ollama run llama3.2
```

5. Run the game:
```bash
   python tic_tac_toe_ai.py
```


### 💡 Tip:
- If Ollama is not running or the model isn't found, the game will automatically fall back to a basic rule-based AI opponent.
- The AI can only play as "O" and goes second.
- When playing AI mode, it thinks in real-time and returns its move based on current game state.

### 🔍 LLM-Based Agent Logic (CrewAI):
- Takes the board state as input
- Uses reasoning to pick the best move: win, block, center, corners, etc.
- Response format: JSON like { "row": 1, "col": 2 }

Enjoy the game!

## Author
Developed with ❤️ by [Ali FAHS](https://github.com/fahsAli)