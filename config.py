import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# File Paths
WORLD_FILE_PATH = "shared_data/generated_world.json"
SAVED_WORLD_PATH = "shared_data/YourWorld_L1.json"
    