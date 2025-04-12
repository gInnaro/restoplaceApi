from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/restoplace_db"
    DATABASE_URL: str = os.environ.get("DATABASE_URL")

settings = Settings()