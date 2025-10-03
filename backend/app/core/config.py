import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/chatbot"
    SECRET_KEY: str = "supersecretkey"
    BLOB_CONNECTION_STRING: str = ""
    AZURE_TENANT_ID: str = ""
    AZURE_CLIENT_ID: str = ""
    AZURE_CLIENT_SECRET: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
