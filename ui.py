import os
import json
import gradio as gr
from helper import load_world, save_world, generate_game_state, run_action
from world_creation import generate_world
from config import WORLD_FILE_PATH, SAVED_WORLD_PATH, WORLD_FOLDER
from moderation_safety import is_safe


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

def create_new_world(template, custom_prompt):
    """Generate a new world based on a template or custom input."""
    world_data = generate_world(template, custom_prompt)
    save_world(world_data, os.path.join(WORLD_FOLDER, f"{world_data['name']}.json"))
    return f"New world '{world_data['name']}' created!", list_worlds(), world_data

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

def launch_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# 🌍 AI RPG - World Selection")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📂 Load Existing World")
                world_dropdown = gr.Dropdown(list_worlds(), label="Available Worlds")
                world_description = gr.Textbox(label="World Description", interactive=False)
                load_btn = gr.Button("Load World")
            
            with gr.Column():
                gr.Markdown("### 🏗️ Generate a New World")
                template_dropdown = gr.Dropdown(["Fantasy", "Sci-Fi", "Cyberpunk"], label="Select Template")
                custom_prompt = gr.Textbox(label="Custom World Description (Optional)")
                generate_btn = gr.Button("Generate World")

        # ✅ Use gr.State to store actual game data
        game_state_store = gr.State(value={})  # Holds actual game state
        game_state_display = gr.Textbox(label="📜 Game State", interactive=False)

        start_game_btn = gr.Button("▶ Start Game")

        # ✅ Chat Interface (shouldn't be returned dynamically)
        chat_interface = gr.ChatInterface(
            fn=lambda msg, hist: "Game not started yet. Load a world and click 'Start Game'!",  # Default placeholder
            chatbot=gr.Chatbot(),
            textbox=gr.Textbox()
        )

        # ✅ Corrected Load Button Function
        def load_selected_world_ui(world_file):
            world_desc, world_data = load_selected_world(world_file)
            return world_desc, world_data  # Send dictionary to `game_state_store`

        load_btn.click(
            load_selected_world_ui, 
            inputs=[world_dropdown], 
            outputs=[world_description, game_state_store]
        )

        # ✅ Corrected Start Game Handling
        def start_game_ui(world_data):
            if not world_data:
                return "❌ Error: No world data loaded!", None

            game_state_text, game_state = start_game(world_data)

            # ✅ Update chat function dynamically instead of creating a new ChatInterface
            chat_interface.fn = lambda msg, hist: main_loop(msg, hist, game_state)

            first_message = run_action("randomstartmessagethatIcannotcopy", [], game_state)

            return game_state_text, game_state, [(None, first_message)]

        start_game_btn.click(
            start_game_ui,
            inputs=[game_state_store],  
            outputs=[game_state_display, game_state_store, chat_interface.chatbot]
        )



    demo.launch(share=True)



if __name__ == "__main__":
    launch_ui()

