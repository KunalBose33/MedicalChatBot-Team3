import requests
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from app.config.settings import settings

DISCLAIMER = (
    "This information is educational and not a diagnosis. "
    "If symptoms are severe or worsening, seek urgent medical care."
)

# ---- Doctor / Knowledge-base chat ----
def generate_answer_with_disclaimer(prompt: str, context: str, temperature: float = 0.2) -> str:
    """
    Generate an answer using:
    - Local Ollama if USE_LOCAL=True
    - Mistral API if USE_MISTRAL=True
    - Fallback: return raw context
    Always appends disclaimer for safety.
    """
    try:
        # ---- Local Ollama ----
        if getattr(settings, "USE_LOCAL", False):
            payload = {
                "model": settings.LOCAL_MODEL,
                "prompt": f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:",
                "stream": False,
                "options": {"temperature": temperature},
            }
            resp = requests.post(settings.LOCAL_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return f"{data.get('response', '').strip()}\n\n{DISCLAIMER}"

        # ---- Mistral API ----
        if getattr(settings, "USE_MISTRAL", False) and settings.MISTRAL_API_KEY:
            client = MistralClient(api_key=settings.MISTRAL_API_KEY)
            resp = client.chat(
                model=settings.MISTRAL_MODEL,
                messages=[
                    ChatMessage(role="system", content="You are a helpful medical assistant. Use provided context only."),
                    ChatMessage(role="user", content=f"Context:\n{context}\n\nQuestion: {prompt}")
                ],
                temperature=temperature,
            )
            answer = resp.choices[0].message.content
            return f"{answer}\n\n{DISCLAIMER}"

        # ---- Fallback ----
        return f"(LLM fallback) Based on context:\n{context[:500]}...\n\n{DISCLAIMER}"

    except Exception as e:
        return f"(LLM error fallback: {str(e)})\nContext:\n{context[:500]}...\n\n{DISCLAIMER}"


# ---- Patient chat ----
def generate_patient_answer(prompt: str, temperature: float = 0.2) -> str:
    """
    LLM-only mode for patient questions (no retrieval).
    Supports both Ollama and cloud Mistral.
    Generates simple, layman's explanations.
    Always appends disclaimer.
    """
    try:
        # ---- Local Ollama ----
        if getattr(settings, "USE_LOCAL", False):
            payload = {
                "model": settings.LOCAL_MODEL,
                "prompt": f"You are a friendly medical assistant for patients.\n\nQuestion: {prompt}\nAnswer:",
                "stream": False,
                "options": {"temperature": temperature},
            }
            resp = requests.post(settings.LOCAL_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return f"{data.get('response', '').strip()}\n\n{DISCLAIMER}"

        # ---- Cloud Mistral ----
        if getattr(settings, "USE_MISTRAL", False) and settings.MISTRAL_API_KEY:
            client = MistralClient(api_key=settings.MISTRAL_API_KEY)
            resp = client.chat(
                model=settings.MISTRAL_MODEL,
                messages=[
                    ChatMessage(
                        role="system",
                        content="You are a friendly medical assistant for patients. "
                                "Answer clearly and simply in layman's terms."
                    ),
                    ChatMessage(role="user", content=prompt)
                ],
                temperature=temperature,
            )
            answer = resp.choices[0].message.content
            return f"{answer}\n\n{DISCLAIMER}"

        # ---- Fallback ----
        return f"(Patient LLM fallback) Answer: {prompt}\n\n{DISCLAIMER}"

    except Exception as e:
        return f"(Patient LLM error fallback: {str(e)})\n\n{DISCLAIMER}"
