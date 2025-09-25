import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# This line loads the environment variables from your .env file
load_dotenv()

class Settings(BaseSettings):
    # These values will be read from the environment or use the default
    DB_SERVER: str = os.getenv("DB_SERVER", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "firearm")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PORT: str = os.getenv("DB_PORT", "5432")

    # These secrets are read directly from the environment
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()