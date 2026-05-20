from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import joblib
import requests

from bs4 import BeautifulSoup

from dotenv import load_dotenv

import google.generativeai as genai

# -----------------------------
# LOAD ENV VARIABLES
# -----------------------------
load_dotenv()

# -----------------------------
# CONFIGURE GEMINI
# -----------------------------
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini_model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

# -----------------------------
# LOAD ML MODEL & VECTORIZER
# -----------------------------
model = joblib.load(
    "models/fake_job_model.pkl"
)

vectorizer = joblib.load(
    "models/vectorizer.pkl"
)

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI()

# -----------------------------
# ENABLE CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# REQUEST MODEL
# -----------------------------
class JobInput(BaseModel):

    text: str | None = None

    url: str | None = None

# -----------------------------
# SCAM KEYWORDS
# -----------------------------
scam_keywords = {
    "registration fee": 30,
    "payment required": 25,
    "easy money": 20,
    "work from home": 10,
    "whatsapp": 25,
    "no experience": 15,
    "guaranteed income": 30,
    "quick money": 25,
    "urgent hiring": 10,
    "no interview": 20,
    "investment required": 35,
    "limited seats": 10,
    "earn daily": 20,
}

# -----------------------------
# SCRAPE JOB FROM URL
# -----------------------------
def extract_job_from_url(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        paragraphs = soup.find_all("p")

        text = " ".join(
            [p.get_text() for p in paragraphs]
        )

        # fallback
        if len(text.strip()) < 50:

            text = soup.get_text()

        return text[:10000]

    except Exception as e:

        print("SCRAPING ERROR:", e)

        return None

# -----------------------------
# GEMINI AI EXPLANATION
# -----------------------------
def generate_ai_explanation(
    job_text,
    prediction,
    flags
):

    try:

        prompt = f"""
        Analyze this job posting.

        Job Posting:
        {job_text}

        Prediction:
        {prediction}

        Scam Flags:
        {flags}

        Explain:
        - why this posting may be suspicious
        - scam indicators
        - safety advice

        Keep response concise and professional.
        """

        response = gemini_model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print("GEMINI ERROR:", e)

        if prediction == "Fake Job":

            return (
                "This posting appears suspicious because it contains "
                "possible scam indicators such as payment requests "
                "or unrealistic promises."
            )

        else:

            return (
                "This posting appears relatively safe based on current analysis."
            )

# -----------------------------
# HOME ROUTE
# -----------------------------
@app.get("/")
def home():

    return {
        "message": "JobShield AI Backend Running"
    }

# -----------------------------
# PREDICT ROUTE
# -----------------------------
@app.post("/predict")
def predict_job(job: JobInput):

    # -----------------------------
    # HANDLE URL INPUT
    # -----------------------------
    if job.url:

        extracted_text = extract_job_from_url(
            job.url
        )

        if not extracted_text:

            return {
                "error": "Could not extract job posting from URL"
            }

        text = extracted_text.lower()

    else:

        if not job.text:

            return {
                "error": "No job text provided"
            }

        text = job.text.lower()

    # -----------------------------
    # VECTORIZE TEXT
    # -----------------------------
    transformed_text = vectorizer.transform(
        [text]
    )

    # -----------------------------
    # ML PREDICTION
    # -----------------------------
    prediction = model.predict(
        transformed_text
    )[0]

    probabilities = model.predict_proba(
        transformed_text
    )[0]

    ml_confidence = round(
        float(max(probabilities)) * 100,
        2
    )

    # -----------------------------
    # RULE-BASED SCORING
    # -----------------------------
    rule_score = 0

    detected_flags = []

    for keyword, score in scam_keywords.items():

        if keyword in text:

            rule_score += score

            detected_flags.append(keyword)

    # cap at 100
    rule_score = min(rule_score, 100)

    # -----------------------------
    # FINAL HYBRID SCORE
    # -----------------------------
    final_score = (
        (ml_confidence * 0.7) +
        (rule_score * 0.3)
    )

    if (
        prediction == 1
        and (
            rule_score >= 20
            or ml_confidence >= 95
        )
    ):

        final_prediction = "Fake Job"

    else:

        final_prediction = "Real Job"

    # -----------------------------
    # AI EXPLANATION
    # -----------------------------
    ai_explanation = generate_ai_explanation(
        text,
        final_prediction,
        detected_flags
    )

    # -----------------------------
    # RETURN RESPONSE
    # -----------------------------
    return {

        "prediction": final_prediction,

        "ml_confidence": ml_confidence,

        "rule_score": rule_score,

        "final_confidence": round(
            final_score,
            2
        ),

        "detected_flags": detected_flags,

        "ai_explanation": ai_explanation
    }