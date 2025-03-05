import gradio as gr
from backend.helper import *
from backend.engine import *

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

