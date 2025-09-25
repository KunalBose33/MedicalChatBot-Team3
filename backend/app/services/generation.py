import requests
from mistralai import Mistral
from app.config.settings import settings

DISCLAIMER = (
    "This information is educational and not a diagnosis. "
    "If symptoms are severe or worsening, seek urgent medical care."
)

def generate_answer_with_disclaimer(prompt: str, context: str, temperature: float = 0.2) -> str:
    """
    Generate an answer using:
    - Local Ollama if USE_LOCAL=True
    - Mistral API if USE_MISTRAL=True
    - Fallback: return raw context
    Always appends disclaimer for safety.
    Temperature is passed through if the backend supports it.
    """
    try:
        # ---- Local Ollama ----
        if settings.USE_LOCAL:
            payload = {
                "model": settings.LOCAL_MODEL,
                "prompt": f"Context:\n{context}\n\nQuestion: {prompt}\nAnswer:",
                "stream": False,
                "options": {"temperature": temperature},
            }
            resp = requests.post(settings.LOCAL_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return f"{data.get('response','').strip()}\n\n{DISCLAIMER}"

        # ---- Mistral API ----
        if settings.USE_MISTRAL and settings.MISTRAL_API_KEY:
            client = Mistral(api_key=settings.MISTRAL_API_KEY)
            resp = client.chat.complete(
                model=settings.MISTRAL_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful medical assistant. Use provided context only.",
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {prompt}",
                    },
                ],
                temperature=temperature,
            )
            return f"{resp.choices[0].message['content'].strip()}\n\n{DISCLAIMER}"

        # ---- Fallback ----
        return f"(LLM fallback) Based on context:\n{context[:500]}...\n\n{DISCLAIMER}"

    except Exception as e:
        return f"(LLM error fallback: {str(e)})\nContext:\n{context[:500]}...\n\n{DISCLAIMER}"


def generate_patient_answer(prompt: str, temperature: float = 0.2) -> str:
    """
    LLM-only mode for patient questions (no retrieval).
    Generates simple, layman's explanations.
    Always appends disclaimer.
    """
    patient_context = (
        "You are a friendly medical assistant for patients. "
        "Answer clearly and simply in layman's terms. "
        "Do not use overly technical language."
    )
    return generate_answer_with_disclaimer(prompt, patient_context, temperature=temperature)