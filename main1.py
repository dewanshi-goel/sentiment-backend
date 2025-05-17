# backend(dew)/main1.py
import nltk_download

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "FastAPI Sentiment Analyzer is running!"}

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_sentiment(request: TextRequest):
    scores = sia.polarity_scores(request.text)
    sentiment = "Positive" if scores['compound'] > 0 else "Negative" if scores['compound'] < 0 else "Neutral"
    return {"scores": scores, "overall": sentiment}
