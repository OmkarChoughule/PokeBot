<h1 align="center">
  🧠 PokéBot - Your Smart Pokémon Chatbot 💬
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Pokémon-AI%20Bot-red?style=for-the-badge&logo=pokemon&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Flask-Chat%20API-green?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Frontend-Vanilla%20JS-yellow?style=for-the-badge&logo=javascript" />
</p>

---

### ⚡ Features

> Ask questions, compare stats, or discover surprises — this chatbot knows over 800 Pokémon upto Sun and Moon!

🧠 Natural language support using spaCy  
⚡ Fuzzy matching with RapidFuzz (e.g., "peekachu" still finds Pikachu)  
🎨 Renders official & shiny Pokémon artwork  
📊 Stat comparison between two Pokémon  
🛡️ Weaknesses, resistances & immunities  
🧪 Includes abilities, descriptions & generation info  
🌐 CORS enabled, works with any frontend

---

### 💻 Demo

<div align="center">
  <img src="https://media.tenor.com/f77lmzB5FgkAAAAC/pokeball.gif" width="100" />
</div>

> Coming soon: Hosted demo! 🎉

---

### 🚀 Getting Started

#### 1️⃣ Backend Setup

```bash
git clone https://github.com/yourusername/pokemon-chatbot
cd pokemon-chatbot
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
