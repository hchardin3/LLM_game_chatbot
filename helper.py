import json
import os
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from prompts import world_structure_types
from typing import Literal

llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.9)

def save_world(world_data, filename="fantasy_world.json"):
    """Saves the generated world as a JSON file."""
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
        print("1111111111111111111111111111111111111")
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

        print("222222222222222222222222222222222222")

        for action in history:
            messages.append({"role": "assistant", "content": action[0]})
            messages.append({"role": "user", "content": action[1]})

        print("333333333333333333333333333333333333333")

        messages.append({"role": "user", "content": message})

        print("44444444444444444444444444444444")

        response = llm.invoke("\n".join([msg["content"] for msg in messages]))

        print("jjjjjjjjjjjjjjjjjjj     ", type(response.content.strip()))

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
    Then describe where they start and what they see around them."""

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
        "world": world["name"],
        world_structure_types[game_type][0]: kingdom["name"],
        world_structure_types[game_type][1]: town["name"],
        "start": start,
        "inventory": [],
        "quests": [],
        "hp": 100,
        "stamina": 100,
    }