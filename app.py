
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import re

app = FastAPI(
    title="AI Text Detector",
    description="AI writing analysis API",
    version="2.0"
)

# Allow Google Sites and browser-based frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=50000)
    grade: str = "6"


@app.get("/")
def home():
    return {
        "message": "AI Text Detector API is running!",
        "version": "2.0"
    }


@app.get("/health")
def health():
    return {"status": "online"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    text = request.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Please enter some text."
        )

    # Split text into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    # Extract words
    words = re.findall(r"\b[\w']+\b", text)

    word_count = len(words)
    sentence_count = len(sentences)

    # Average sentence length
    average_sentence_length = (
        word_count / sentence_count
        if sentence_count else 0
    )

    # Vocabulary diversity
    unique_words = len(set(
        word.lower() for word in words
    ))

    vocabulary_diversity = (
        unique_words / word_count
        if word_count else 0
    )

    # Sentence length statistics
    sentence_lengths = [
        len(re.findall(r"\b[\w']+\b", sentence))
        for sentence in sentences
    ]

    shortest_sentence = (
        min(sentence_lengths)
        if sentence_lengths else 0
    )

    longest_sentence = (
        max(sentence_lengths)
        if sentence_lengths else 0
    )

    return {
        "grade": request.grade,

        "statistics": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "unique_words": unique_words,
            "average_sentence_length": round(
                average_sentence_length, 2
            ),
            "vocabulary_diversity": round(
                vocabulary_diversity, 3
            ),
            "shortest_sentence": shortest_sentence,
            "longest_sentence": longest_sentence
        },

        # These remain unavailable until real models
        # have been trained and independently validated.
        "ai_score": None,
        "humanizer_score": None,

        "model_status": "not_trained",

        "warning": (
            "Writing statistics cannot establish "
            "whether text was written by AI or a human."
        )
    }
