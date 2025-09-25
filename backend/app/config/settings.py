from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load .env file from the same folder
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class Settings(BaseModel):
    # --- Azure (optional) ---
    USE_AZURE: bool = os.getenv("USE_AZURE", "False").lower() == "true"
    AZURE_OPENAI_ENDPOINT: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY: str | None = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_DEPLOYMENT: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    AZURE_SEARCH_ENDPOINT: str | None = os.getenv("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_API_KEY: str | None = os.getenv("AZURE_SEARCH_API_KEY")
    AZURE_SEARCH_INDEX: str = os.getenv("AZURE_SEARCH_INDEX", "medkb")

    # --- Mistral API ---
    USE_MISTRAL: bool = os.getenv("USE_MISTRAL", "False").lower() == "true"
    MISTRAL_API_KEY: str | None = os.getenv("MISTRAL_API_KEY")
    MISTRAL_MODEL: str = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

    # --- Local Ollama ---
    USE_LOCAL: bool = os.getenv("USE_LOCAL", "False").lower() == "true"
    LOCAL_MODEL: str = os.getenv("LOCAL_MODEL", "mistral")
    LOCAL_URL: str = os.getenv("LOCAL_URL", "http://localhost:11434/api/generate")

    # --- General settings ---
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))
    TOP_K: int = int(os.getenv("TOP_K", "5"))

    # --- Retrieval (FAISS) ---
    USE_FAISS: bool = os.getenv("USE_FAISS", "False").lower() == "true"
    EMBED_MODEL: str = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "backend/app/vector.index")
    FAISS_META_PATH: str = os.getenv("FAISS_META_PATH", "backend/app/vector_meta.jsonl")


settings = Settings()
