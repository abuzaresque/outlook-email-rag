# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(var_name, default=None):
    """Fetches environment variables safely."""
    value = os.getenv(var_name, default)
    if value is None:
        raise EnvironmentError(f"Missing environment variable: {var_name}")
    return value

GROQ_API_KEY = get_env_variable("GROQ_API_KEY", "")