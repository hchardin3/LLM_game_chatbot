import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# File Paths
WORLD_FOLDER = "worlds/"
WORLD_FILE_PATH = "worlds/generated_world.json"
SAVED_WORLD_PATH = "worlds/YourWorld_L1.json"
    