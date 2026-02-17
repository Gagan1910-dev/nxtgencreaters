# BizForge - AI Branding Automation Platform

## Overview
BizForge is a modern web platform that enables startups to generate a complete brand identity in minutes using Generative AI.
It uses a Python FastAPI backend and a Vanilla JS frontend with Glassmorphism design.

## Features
- **Brand Identity**: Generates unique names and taglines.
- **Visuals**: AI-generated logo concepts.
- **Marketing**: Social media captions and email templates.
- **Analysis**: Sentiment scoring and brand tone analysis.

## Project Structure
```text
bizforge/
├── backend/            # FastAPI Application
│   ├── app/
│   │   ├── main.py     # Entry point
│   │   └── services/   # AI Logic (Mock/Simulated)
│   └── run.py          # Server runner
└── frontend/           # Static Website
    ├── index.html
    ├── css/            # Styling
    └── js/             # Logic
```

## How to Run locally

### 1. Backend Setup
Navigate to the backend folder and install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

Start the server:
```bash
python run.py
```
*Server runs at http://localhost:8000*

### 2. Frontend Setup
You can simply open `frontend/index.html` in your browser.

**Optional**: For a better experience (hot reload), use a simple HTTP server:
```bash
# Open a new terminal in /frontend
python -m http.server 3000
```
Then visit `http://localhost:3000`.

## Configuration
- The backend is currently running in **Simulation Mode** (using placeholders and mock logic).
- To connect real AI models, update `backend/app/services/*.py` with your API keys (IBM Granite, Groq LLaMA, Stability AI).
