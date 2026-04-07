# env/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN", "")

def validate_config():
    """
    Validate that environment variables are set (optional for fallback mode).
    Note: If HF_TOKEN is empty, the inference script will use deterministic fallback.
    """
    # Config is optional - script can run in fallback mode
    pass
