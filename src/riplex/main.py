import os
from fastapi import FastAPI
from riplex.schemas.research import RequestResearch
from dotenv import load_dotenv
from riplex.services.agent import run_agent

load_dotenv()

app = FastAPI(title="Research Agent APIs")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/research")
def research(request : RequestResearch):
    return {
     "question": request.question,
     "answer": run_agent(request.question),
    }


