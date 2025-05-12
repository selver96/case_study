from dotenv import load_dotenv
import os

load_dotenv()

PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False") == "True"
DB_URL = os.getenv("DB_URL", "postgresql://user:password@postgres:5432/case_study")