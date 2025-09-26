from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from .config.settings import settings
from .services.retrieval import InMemoryRetriever
from .services.generation import generate_answer_with_disclaimer, generate_patient_answer
from .labs.evaluator import parse_csv_bytes, parse_fhir_bytes, normalize_and_score

app = FastAPI(title="Medical Assistant Chatbot (Sprint 2 Starter)" )

retriever = InMemoryRetriever()  # local stub index

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    # 1) retrieve KB passages
    docs = retriever.retrieve(req.message, k=settings.TOP_K)
    # 2) generate answer from docs (local simple generator with disclaimer)
    result = generate_answer_with_disclaimer(req.message, docs, temperature=settings.TEMPERATURE)
    return result

@app.post("/patient-chat")
async def patient_chat(req: ChatRequest):
    result = generate_patient_answer(
        req.message, temperature=settings.TEMPERATURE
    )
    return {"answer": result}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file.content_type == "text/csv":
        records = parse_csv_bytes(await file.read()) 
    else:
        records = parse_fhir_bytes(await file.read())

    scored = normalize_and_score(records)

    if scored["flagged"]:
        summary_text = "The following results are outside normal ranges:\n" + "\n".join(scored["flagged"])
        explanation = generate_patient_answer(summary_text, temperature=settings.TEMPERATURE)
    else:
        explanation = "All uploaded results appear within the normal reference ranges. " \
                      "This is not a diagnosis. Please consult a healthcare provider."

    return {
        "summary": scored["per_test"],
        "explanation": explanation,
        "disclaimer": scored["disclaimer"]
    }

