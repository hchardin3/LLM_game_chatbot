import gradio as gr
from utils.helper import load_world, save_world, generate_game_state, run_action
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from config import OPENAI_API_KEY, WORLD_FILE_PATH, SAVED_WORLD_PATH
from moderation_safety import is_safe

demo = None

def start_game(main_loop, share=False):
    global demo
    # If demo is already running, close it first
    if demo is not None:
        demo.close()

    demo = gr.ChatInterface(
        main_loop,
        chatbot=gr.Chatbot(height=250, placeholder="Type 'start game' to begin"),
        textbox=gr.Textbox(placeholder="What do you do next?", container=False, scale=7),
        title="AI RPG",
        # description="Ask Yes Man any question",
        theme="soft",
        examples=["Look around", "Continue the story"],
        cache_examples=False,
        # retry_btn="Retry",
        # undo_btn="Undo",
        # clear_btn="Clear",
                           )
    demo.launch(share=share, server_name="0.0.0.0")

# Define the main game loop
def main_loop(player_input, history, game_state):
    """Main game loop handling player input and game progression."""
    
    if not is_safe(player_input):
        return "⚠️ Your message was flagged as inappropriate. Please try again."

    try:
        return run_action(player_input, history, game_state)
    except Exception as e:
        return f"⚠️ An error occurred: {str(e)}"

# **Launch the game UI**
if __name__ == "__main__":
    # Load the world data
    game_state = generate_game_state(WORLD_FILE_PATH)
    start_game(lambda msg, hist: main_loop(msg, hist, game_state), share=True)
