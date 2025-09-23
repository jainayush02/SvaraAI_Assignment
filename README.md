# SvaraAI - Reply Classification Assignment

This repository contains my submission for the SvaraAI AI/ML Engineer Internship assignment.

The project implements a full pipeline to classify email replies into **positive**, **negative**, and **neutral** categories.

## Project Structure

-   `notebook.ipynb`: Contains the core ML/NLP pipeline (Part A).
-   `app.py`: A FastAPI application to serve the best-performing model (DistilBERT) via a `/predict` endpoint.
-   `answers.md`: Contains short answers to the reasoning questions (Part C).
-   `requirements.txt`: Lists all the necessary Python packages.
-   `svara_reply_classifier/`: The directory containing the saved, fine-tuned model.

## How to Run the API

### 1. Setup

First, clone the repository. It is recommended to use a virtual environment:

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required dependencies
pip install -r requirements.txt

uvicorn app:app --reload


Invoke-WebRequest -Uri '[http://127.0.0.1:8000/predict](http://127.0.0.1:8000/predict)' `
  -Method POST `
  -Headers @{'Content-Type' = 'application/json'} `
  -Body '{"text": "This sounds great, let''s talk!"}'
