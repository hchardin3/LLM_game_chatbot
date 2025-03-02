# **AI RPG Chatbot Game** 🎭🗡️

This project is an **interactive text-based role-playing game (RPG)** powered by **Gradio** and **OpenAI's GPT-4 Turbo**. The AI acts as a **game master**, dynamically generating story progressions based on player input.

---

## **🚀 Features**
- 🧙 **AI-Powered Storytelling** – The game evolves based on your choices.
- 🏰 **Fully Customizable Worlds** – The game world is loaded from a JSON file.
- 🎮 **Gradio-Based Interface** – Easy-to-use web UI.
- 🌍 **Dynamic Game State** – The game adapts to your actions.
- 💾 **Persistent World Data** – Saves game state in JSON.
- 🛑 **Content Moderation** – `moderation_safety.py` ensures safe interactions.

---

## **🛠️ Installation & Setup**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-repo/GameChatBot.git
cd GameChatBot
```

### 2️⃣ Set Up a Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up API Keys
Create a .env file and add:
```sh
OPENAI_API_KEY=your_openai_api_key
```
Or, modify config.py to include your OpenAI API key directly.

---

## 🎮 How to Run the Game

    - 1. **Run the python script**:

```sh
python3 main.py
```

    - 2. **Wait for the Gradio link** (appears in the terminal):
``` sh
* Running on local URL:  http://0.0.0.0:7860
* Running on public URL: https://xxxxx.gradio.live
```

    - 3. **Click on the URL** to open the game UI in your browser.
    - 4. **Start playing!** Type "start game" in the chat to begin your adventure.

---

## 🌍 How to Generate a New World
If you want to create a brand-new world, run:

```sh
python3 world_creation.py
```

This will generate a new game world JSON file inside shared_data/.

---

## 🛑 Moderation & Safety

The moderation_safety.py script ensures that users cannot send harmful, offensive, or policy-violating messages.
This system can be customized to fit different moderation policies.