from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5")

settings = Settings()

if not settings.openai_api_key:
    raise RuntimeError("Missing OPENAI_API_KEY. Copy .env.example to .env and set your key.")
