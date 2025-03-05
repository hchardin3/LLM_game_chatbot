import json
import os
from langchain_openai import ChatOpenAI
from backend.prompts import world_structure_types
from typing import Literal
from backend.world_creation import generate_world
from backend.config import WORLD_FOLDER, OPENAI_API_KEY
from backend.moderation_safety import is_safe
from backend.helper import *


llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.9)

def run_action(message: str, history, game_state: dict, game_type: Literal["Fantasy", "Sci-Fi", "Cyberpunk"] = "Fantasy"):
    print("type of message ", type(message))
    print("type of history ", type(history))
    print("type of game_state ", type(game_state))
    print("type of game_type ", type(game_type))
    try:
        if(message == 'randomstartmessagethatIcannotcopy'):
            print("Start game...")
            return game_state['start']

        system_prompt = """You are an AI Game master. Your job is to write what \
                        happens next in a player's adventure game.\
                        Instructions: \
                        You must on only write 1-3 sentences in response. \
                        Always write in second person present tense. \
                        Ex. (You look north and see...)"""
        
        # Ensure game_state is valid
        world_info = f"""
        World: {game_state.get('world', 'Unknown')}
        {world_structure_types[game_type][0]}: {game_state.get(world_structure_types[game_type][0], 'Unknown')}
        {world_structure_types[game_type][1]}: {game_state.get(world_structure_types[game_type][0], 'Unknown')}
        Your Character: {game_state.get('character', 'Unknown')}
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": world_info}
        ]

        for action in history:
            messages.append({"role": "assistant", "content": action[0]})
            messages.append({"role": "user", "content": action[1]})

        messages.append({"role": "user", "content": message})

        response = llm.invoke("\n".join([msg["content"] for msg in messages]))

        return response.content.strip() if response else "Error: No response generated."

    except Exception as e:
        print(f"���️ Error occurred while running action: {str(e)}")
        return f"⚠️ Error: {str(e)}"


def generate_game_state(world: dict, game_type: Literal["Fantasy", "Sci-Fi", "Cyberpunk"] = "Fantasy"):
    """Generate the initial game state based on the world data."""
    
    print(world_structure_types[game_type][0])
    print(world.keys())

    # Extract the character, kingdom, and town data
    kingdom = next(iter(world[world_structure_types[game_type][0]].values()))
    town = next(iter(kingdom[world_structure_types[game_type][1]].values()))
    character = next(iter(town['npcs'].values()))

    # Generate the starting text for the game
    system_prompt = """You are an AI Game master. Your job is to create a 
    start to an adventure based on the world a player is playing as. 
    Instructions:
    You must only use 2-4 sentences.
    Write in second person. For example: "You are Jack."
    Write in present tense. For example: "You stand at..."
    First describe the character and their backstory.
    Then describe where they start and what they see around them.
    At the end, you have to subtly direct the player towards his first quest so that he can start his adventure. 
    For example: "Your teacher tasks you to deliver this message to the headmaster of the school."
    """

    world_info = f"""
    World: {world}
    {world_structure_types[game_type][0]}: {kingdom}
    {world_structure_types[game_type][1]}: {town}
    Your Character: {character}
    "inventory": [],
    "quests": [],
    "hp": 100,
    "stamina": 100,
    """

    start_response = llm.invoke(f"{system_prompt}\n{world_info}\nYour Start:")

    # Ensure the response is valid
    start = start_response.content.strip() if start_response else "Error: No start text generated."

    return {
        "world": world,
        world_structure_types[game_type][0]: kingdom["name"],
        world_structure_types[game_type][1]: town["name"],
        "start": start,
        "inventory": [],
        "quests": [],
        "hp": 100,
        "stamina": 100,
    }

def start_game(world_data):
    """Initialize game state and return necessary UI updates."""

    if not isinstance(world_data, dict) or "kingdoms" not in world_data:
        return "❌ Error: Invalid world file format. Missing 'kingdoms' key.", None

    # Generate game state
    game_state = generate_game_state(world_data)

    return f"📜 Game started! Current state: {update_game_state(game_state)}", game_state

def list_worlds():
    """Retrieve available world files in the folder."""
    return [f for f in os.listdir(WORLD_FOLDER) if f.endswith(".json")]

def load_selected_world(world_file):
    """Load the selected world and ensure it's returned as a dictionary."""
    world_path = os.path.join(WORLD_FOLDER, world_file)
    
    with open(world_path, "r") as f:
        world_data = load_world(world_path)  # Ensure it is read as a dictionary

    return world_data.get("description", "No description available."), world_data

def update_game_state(game_state):
    """Display inventory, quests, and stats."""
    return f"Inventory: {game_state.get('inventory', 'Unknown')}, Quests: {game_state.get('quests', 'Unknown')}, Stats: HP {game_state.get('hp', 'Unknown')}, Stamina {game_state.get('stamina', 'Unknown')}%"

def main_loop(player_input, history, game_state):
    """Main game loop handling player input and game progression."""
    print("hgggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg...")
    if not is_safe(player_input):
        return "⚠️ Your message was flagged as inappropriate. Please try again."
    try:
        return run_action(player_input, history, game_state)
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"