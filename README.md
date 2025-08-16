# 🏁 AI Checkers Player

An **AI-powered Checkers game agent** built in Python.  
This project allows you to pit different AI strategies against each other (or a human player) and experiment with search algorithms, heuristics, and Monte Carlo ideas.

---

## 📌 Features
- ✔️ Multiple AI strategies (Average AI, Random AI, Manual AI, custom implementations)  
- ✔️ Play **AI vs AI** or **Human vs AI** matches  
- ✔️ Modular design for adding new AIs easily  
- ✔️ Core checkers logic including move validation, jumps, and kinging  
- ✔️ Experimentation with **heuristic search** and **Monte Carlo Tree Search (MCTS)** concepts  

---

## 📂 Project Structure
```
AI-Checkers-Player/
│── Tools/
│   ├── AI_Runner.py        # Main runner for AI matches
│   ├── submission.py       # Entry for custom AI submissions
│   ├── Sample_AIs/         # Example AI implementations
│       ├── Average_AI/     
│       ├── Average_AI_368/ 
│── Documentation/          # Manuals, reports, and slides
│── README.md               # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/arshiya-salehi/AI-Checkers-Player.git
cd AI-Checkers-Player/Tools
```

### 2. Install Requirements
This project runs on **Python 3.8+**.  
If there are dependencies (e.g., `pygame`), install them with:
```bash
pip install -r requirements.txt
```

*(If no requirements file is present, the base Python standard library may be enough.)*

### 3. Run the Game / AI Match
```bash
python AI_Runner.py
```

You’ll be prompted to select which AIs to play (e.g., RandomAI vs AverageAI).

---

## 🧠 Custom AI Development

You can implement your own AI by creating a new class inside `Tools/Sample_AIs/`.  
Steps:
1. Copy an existing AI (e.g., `AverageAI.py`) into a new folder.  
2. Implement your decision-making logic inside the `getMove()` method.  
3. Run the game with your AI against others using `AI_Runner.py`.  

---

## 📜 Documentation
- [General Student Manual](GeneralStudentManual.md)  
- [Final Report](Final%20Report.docx)  
- [MCTS Ideas (PDF)](92-MCTS%20(Checkers)%20Ideas%20(1).pdf)  

---

## 🛠 Tech Stack
- **Language**: Python  
- **Core Concepts**: Minimax, Heuristics, Monte Carlo Tree Search (MCTS)  
- **Environment**: CLI-based simulation (can be extended to GUI with libraries like Pygame)  

---

## 🤝 Contributing
Pull requests are welcome!  
If you’d like to improve heuristics, add new AI strategies, or optimize performance, feel free to fork and submit changes.  

---

## 📄 License
This project is for **educational purposes**.  
Check the repository for specific license terms.  

---

⚡ Built as part of an AI course project to explore intelligent agents and decision-making in board games.  
