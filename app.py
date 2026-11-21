from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="AI Text Detector API")


class AnalyzeRequest(BaseModel):
    text: str
    grade: str = "6"


@app.get("/")
def home():
    return {"message": "AI Text Detector API is running!"}


@app.get("/health")
def health():
    return {"status": "online"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    text = request.text.strip()

    if not text:
        return {"error": "No text provided"}

    # Split the text into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # Split into words
    words = re.findall(r"\b[\w']+\b", text)

    # Calculate basic writing statistics
    word_count = len(words)
    sentence_count = len(sentences)

    avg_sentence_length = (
        word_count / sentence_count if sentence_count else 0
    )

    unique_words = len(set(w.lower() for w in words))

    vocabulary_ratio = (
        unique_words / word_count if word_count else 0
    )

    return {
        "grade": request.grade,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_sentence_length": round(avg_sentence_length, 2),
        "vocabulary_diversity": round(vocabulary_ratio, 3),
        "status": "analysis_complete",
        "warning": "Writing statistics are not proof of AI or human authorship."
    }
