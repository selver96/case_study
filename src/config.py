from dotenv import load_dotenv
import os

# Load variables from .env into environment
load_dotenv()

# Access the variables
PORT = int(os.getenv("PORT", 8000))  # fallback to 8000 if not set
DEBUG = os.getenv("DEBUG", "False") == "True"
DB_URL = os.getenv("DB_URL", "postgresql://user:password@postgres:5432/case_study")