import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/health")
def health():
    return {"message":"Server is healthy!"}

@app.get("/research")
def research():
    return {
        "message": "Research endpoint is working",
        "api_key_loaded": GROQ_API_KEY,
    }