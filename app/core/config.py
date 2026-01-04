from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os
# Load environment variables from .env
load_dotenv()

# Fetch database variables
USER = os.getenv("dbuser")
PASSWORD = os.getenv("dbpassword")
HOST = os.getenv("dbhost")
PORT = os.getenv("dbport")
DBNAME = os.getenv("dbname")
SECRET = os.getenv("JWT_SECRET")
ALGORITHM=os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "AIgo API"
    VERSION: str = "0.1.0"

    # 개발: http://localhost:7001 (React)
    CORS_ORIGINS: list[str] = ["http://localhost:7001", "http://127.0.0.1:7001", "https://aigo-frontend.vercel.app"]

    # Database connection parameters
    DB_USER: str = USER
    DB_PASSWORD: str = PASSWORD
    DB_HOST: str = HOST
    DB_PORT: str = PORT
    DB_NAME: str = DBNAME

    # JWT
    JWT_SECRET: str = SECRET
    JWT_ALGORITHM: str = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = ACCESS_TOKEN_EXPIRE_MINUTES

settings = Settings()
