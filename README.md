# Vertex AI GenAI Project: Intelligent Product Review Analyzer

A complete, production-ready Generative AI application built with **Google Cloud Vertex AI (Gemini)** that analyzes product reviews and generates actionable insights.

## 🚀 Project Overview

This application allows users to paste a product review and instantly receive:

- **Sentiment Analysis** (Positive / Neutral / Negative + confidence)
- **Key Strengths** extracted from the review
- **Key Weaknesses / Complaints**
- **Concise Summary**
- **Suggested Customer Support Reply** (professional & empathetic)

### Architecture

```
User (Browser)
    ↓
Frontend (HTML + JS)
    ↓
Cloud Run (FastAPI Backend)
    ↓
Vertex AI Gemini 1.5 / 2.0 Flash
```

### Tech Stack

| Component       | Technology                  |
|-----------------|-----------------------------|
| Backend         | FastAPI (Python)            |
| AI Model        | Vertex AI Gemini            |
| Deployment      | Cloud Run                   |
| Frontend        | Vanilla HTML/CSS/JS         |
| Container       | Docker                      |
| Auth (optional) | API Key / IAM               |

---

## 📁 Project Structure

```
vertex-ai-genai-project/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   └── index.html           # Beautiful single-page UI
├── scripts/
│   └── deploy.sh            # One-click deploy to Cloud Run
├── docs/
│   └── Project_Explanation.pdf
├── README.md
└── .gitignore
```

---

## 🛠️ Local Development Setup

### Prerequisites

- Python 3.10+
- Google Cloud Project with Vertex AI API enabled
- `gcloud` CLI installed and authenticated
- Docker (for container testing)

### 1. Clone & Setup

```bash
cd vertex-ai-genai-project/backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
MODEL_NAME=gemini-1.5-flash-001
```

### 3. Authenticate with Google Cloud

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 4. Enable Required APIs

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 5. Run Locally

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Open: http://localhost:8080

---

## ☁️ Deploy to Google Cloud Run

### Quick Deploy

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh YOUR_PROJECT_ID us-central1
```

Or manually:

```bash
cd backend
gcloud run deploy review-analyzer \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars PROJECT_ID=YOUR_PROJECT_ID,LOCATION=us-central1 \
  --memory 1Gi \
  --cpu 1
```

---

## 🔑 Important Notes

1. **Cost Control**: Gemini Flash is very cheap. Still set budget alerts in GCP.
2. **Authentication**: For production, remove `--allow-unauthenticated` and use IAM or API keys.
3. **Model**: You can switch to `gemini-1.5-pro` or newer models by changing `MODEL_NAME`.
4. **Free Tier**: New GCP accounts get $300 credits. Vertex AI has free tier usage.

---

## 📸 Features Showcase

- Clean, modern responsive UI
- Real-time analysis with loading state
- Structured JSON response from Gemini
- Error handling & validation
- Ready for Cloud Run (serverless, auto-scaling)

---

## 📄 Documentation

See `docs/Project_Explanation.pdf` for:
- Detailed architecture
- Step-by-step implementation
- Learning outcomes
- Interview talking points
- Cost estimation
- Future enhancements

---

## 🛡️ License

MIT License – Feel free to use in your portfolio and interviews.

**Built for learning Google Cloud + Generative AI with Vertex AI.**
