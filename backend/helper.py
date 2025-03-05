import json
import os
from langchain_openai import ChatOpenAI
from backend.config import OPENAI_API_KEY


llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.9)

def save_world(world_data, filename=None):
    """Saves the generated world as a JSON file."""
    if not filename:
        filename = f"{world_data['name']}.json"
    with open(filename, 'w') as f:
        json.dump(world_data, f, indent=4)
    print(f"✅ World saved to {filename}")

def load_world(filename="Nomadia.json"):
    """Loads a previously saved fantasy world from a JSON file."""
    
    if not os.path.exists(filename):
        print(f"❌ Error: File '{filename}' not found!")
        return None

    with open(filename, 'r', encoding="utf-8") as f:
        world_data = json.load(f)

    # Check if the loaded data is actually a string and needs another JSON decode
    if isinstance(world_data, str):  
        try:
            world_data = json.loads(world_data)  # Convert JSON string to dict
        except json.JSONDecodeError:
            print("❌ Error: JSON inside the file is malformed!")
            return None

    if not isinstance(world_data, dict):
        print(f"❌ Error: Unexpected data type {type(world_data)} in '{filename}'")
        return None

    print(f"🌍 Loaded world: {world_data['name']}")
    return world_data



