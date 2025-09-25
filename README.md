# Medical Assistant Chatbot — Sprint 2 Starter (Beginner Friendly)

This starter helps you complete **Sprint 2 (AI Integration & Core Logic)** step‑by‑step.

## What you will build
1) `/chat` endpoint that answers medical questions using **RAG** (Retrieval Augmented Generation) with citations and a safety disclaimer.  
2) `/upload` endpoint that accepts **CSV or FHIR JSON** lab results and returns per‑test interpretation.

> ⚠️ This project is for learning. It **does not provide medical advice**.

---

## Prerequisites (install once)
- Python 3.10+  
- Node not required for this sprint (frontend in Sprint 3).  
- Create a virtual environment (Windows PowerShell example):
  ```powershell
  cd backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

## Configure environment
1. Copy `.env.example` to `.env` and fill values (you can put placeholders for now):
   ```bash
   cp backend/app/config/.env.example backend/app/config/.env
   ```

2. If you do not have Azure yet, **no problem**—you can run local stubs that mimic Azure. When you get Azure credentials later, just update `.env`.

## Run the API (dev mode)
```bash
cd backend
uvicorn app.main:app --reload
```
Open: http://127.0.0.1:8000/docs

## Try it quickly
- **Chat**: use the `/chat` endpoint in Swagger UI with `{"message":"What are warning signs of heart attack?"}`  
- **Upload CSV**: pick `backend/app/tests/data/sample_labs.csv`  
- **Upload FHIR**: pick `backend/app/tests/data/sample_fhir_bundle.json`

## Next steps (Day-by-day)
**Day 1–2**: (a) skim KB files in `app/kb/`, (b) run `scripts/ingest_kb.py` (uses a local in‑memory index), (c) test `/chat`.  
**Day 3–4**: add simple content safety + disclaimer (already scaffolded in `services/generation.py`).  
**Day 5–7**: finish CSV/FHIR parsing + unit conversions in `labs/evaluator.py`.  
**Day 8–10**: add tests in `app/tests/`, tweak prompts, and polish outputs.

When you’re ready for real Azure Search & Azure OpenAI, open `app/config/settings.py` and switch `USE_AZURE=False` → `True`, then fill `.env` with real credentials (notes inside).
