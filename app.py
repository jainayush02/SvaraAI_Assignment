import torch
import re
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "E:\PROJECTS\SvaraAI – Assignment\svara_reply_classifier"
DEVICE = "cpu"

print("Loading model and tokenizer")

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    model.to(DEVICE)
    model.eval()
    print("Model and tokenizer loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# Initialize the FastAPI app
app = FastAPI(title="SvaraAI Reply Classifier API")

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: str
    confidence: float

def clean_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"plz", "please", text)
    text = re.sub(r"schdule", "schedule", text)
    text = re.sub(r"intrested", "interested", text)
    text = re.sub(r"\s+", " ", text)
    return text

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Takes a JSON with a 'text' field and returns a classification label
    [cite_start]and confidence score[cite: 1].
    """
    cleaned_text = clean_text(request.text)

    inputs = tokenizer(cleaned_text, return_tensors="pt", padding=True, truncation=True).to(DEVICE)
    #inference
    with torch.no_grad():
        logits = model(**inputs).logits

    probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]
    confidence = probabilities.max().item()
    prediction_id = probabilities.argmax().item()
    label = model.config.id2label[prediction_id]

    return PredictResponse(label=label, confidence=confidence)

@app.get("/")
def read_root():
    return {"message": "Welcome! The reply classifier API is running."}