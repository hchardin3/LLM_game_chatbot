import json
import os
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=OPENAI_API_KEY, temperature=0.9)

def save_world(world_data, filename="fantasy_world.json"):
    """Saves the generated world as a JSON file."""
    with open(filename, 'w') as f:
        json.dump(world_data, f, indent=4)
    print(f"✅ World saved to {filename}")

def load_world(filename="fantasy_world.json"):
    """Loads a previously saved fantasy world from a JSON file."""
    if not os.path.exists(filename):
        print(f"❌ Error: File '{filename}' not found!")
        return None

    with open(filename, 'r') as f:
        world_data = json.load(f)

    print(f"🌍 Loaded world: {world_data['name']}")
    return world_data


def run_action(message: str, history, game_state: dict):
    try:
        if(message == 'start game'):
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
        Kingdom: {game_state.get('kingdom', 'Unknown')}
        Town: {game_state.get('town', 'Unknown')}
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
        return f"⚠️ Error: {str(e)}"


def generate_game_state(world_file_path: str):
    world = load_world(world_file_path)
    kingdom = next(iter(world['kingdoms'].values()))
    town = next(iter(kingdom['towns'].values()))
    character = next(iter(town['npcs'].values()))

    # Generate the starting text for the game
    system_prompt = """You are an AI Game master. Your job is to create a 
    start to an adventure based on the world, kingdom, town, and character 
    a player is playing as. 
    Instructions:
    You must only use 2-4 sentences.
    Write in second person. For example: "You are Jack."
    Write in present tense. For example: "You stand at..."
    First describe the character and their backstory.
    Then describe where they start and what they see around them."""

    world_info = f"""
    World: {world}
    Kingdom: {kingdom}
    Town: {town}
    Your Character: {character}
    """

    start_response = llm.invoke(f"{system_prompt}\n{world_info}\nYour Start:")

    # Ensure the response is valid
    start = start_response.content.strip() if start_response else "Error: No start text generated."

    game_state = {
        "world": world,
        "kingdom": kingdom,
        "town": town,
        "character": character,
        "start": start
    }

    return game_state