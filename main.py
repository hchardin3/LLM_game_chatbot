import gradio as gr
from backend.helper import *
from backend.engine import *
from backend.world_creation import generate_world

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
                world_name_input = gr.Textbox(label="World Name (Optional)")
                custom_instruction = gr.Textbox(label="Custom Instructions/Original Concept for Your World (Optional)")

                num_factions = gr.Number(value=3, label="Number of Factions (3 by default)", minimum=2, maximum=5)
                num_subfactions = gr.Number(value=3, label="Number of Subfactions per Factions (3 by default)", minimum=1, maximum=5)
                num_npcs = gr.Number(value=3, label="Number of NPCs in each Subfaction (3 by default)", minimum=2, maximum=5)
                    

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

        # ✅ Corrected Generate Button Function
        def create_new_world_ui(template, world_name, custom_prompt, nbr_factions, nbr_subfactions, nbr_npcs):
            world_data = generate_world(template, world_name, custom_prompt, nbr_factions, nbr_subfactions, nbr_npcs)
            save_world(world_data, os.path.join(WORLD_FOLDER, f"{world_data['name']}.json"))
            updated_list_worlds = list_worlds()
            return f"New world '{world_data['name']}' created!", updated_list_worlds, world_data
        
        generate_btn.click(
            create_new_world_ui, 
            inputs=[template_dropdown, world_name_input, custom_instruction, num_factions, num_subfactions, num_subfactions], 
            outputs=[game_state_display, world_dropdown, game_state_store]
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

