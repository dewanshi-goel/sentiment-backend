# backend1/main1.py
import nltk_download

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import json
import os


nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "FastAPI Sentiment Analyzer is running!"}

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "null"],  # include 'null' for local file testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#path to user data JSON file
USERS_FILE="users.json"

class TextRequest(BaseModel):
    text: str

class LoginRequest(BaseModel):
    email:str
    password:str

@app.post("/analyze")
def analyze_sentiment(request: TextRequest):
    scores = sia.polarity_scores(request.text)
    sentiment = "Positive" if scores['compound'] > 0 else "Negative" if scores['compound'] < 0 else "Neutral"
    return {"scores": scores, "overall": sentiment}

# Login endpoint
@app.post("/login")
def login(request: LoginRequest):
    if not os.path.exists(USERS_FILE):
        raise HTTPException(status_code=500, detail="User database not found")

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if request.email in users and users[request.email] == request.password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    