"""
Vertex AI GenAI Project - Intelligent Product Review Analyzer
Backend: FastAPI + Vertex AI Gemini
"""

import os
import json
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Vertex AI
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
PROJECT_ID = os.getenv("PROJECT_ID", "")
LOCATION = os.getenv("LOCATION", "us-central1")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash-001")

# Initialize FastAPI
app = FastAPI(
    title="Product Review Analyzer - Vertex AI",
    description="GenAI-powered product review analysis using Google Cloud Vertex AI Gemini",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend
# When running locally or in container, look for index.html in several places
POSSIBLE_FRONTEND_PATHS = [
    os.path.join(os.path.dirname(__file__), "frontend", "index.html"),
    os.path.join(os.path.dirname(__file__), "frontend_index.html"),
    os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"),
]


# ==================== Pydantic Models ====================

class ReviewRequest(BaseModel):
    review_text: str = Field(..., min_length=10, max_length=5000, description="The product review text to analyze")
    product_name: Optional[str] = Field(None, description="Optional product name for better context")


class AnalysisResponse(BaseModel):
    sentiment: str
    confidence: float
    summary: str
    strengths: list[str]
    weaknesses: list[str]
    suggested_reply: str
    raw_model_output: Optional[dict] = None


# ==================== Vertex AI Initialization ====================

def init_vertex_ai():
    """Initialize Vertex AI with project and location."""
    if not PROJECT_ID:
        logger.warning("PROJECT_ID not set. Vertex AI calls will fail.")
        return False
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        logger.info(f"Vertex AI initialized | Project: {PROJECT_ID} | Location: {LOCATION}")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Vertex AI: {e}")
        return False


# Initialize on startup
vertex_ready = init_vertex_ai()


# ==================== Prompt Engineering ====================

SYSTEM_PROMPT = """You are an expert Customer Experience Analyst and Product Review Specialist.
Your job is to analyze product reviews carefully and return structured, actionable insights.

You must ALWAYS respond with valid JSON only (no markdown, no extra text) using this exact schema:

{
  "sentiment": "Positive" | "Neutral" | "Negative",
  "confidence": 0.0 to 1.0,
  "summary": "A concise 1-2 sentence summary of the review",
  "strengths": ["list", "of", "positive points"],
  "weaknesses": ["list", "of", "complaints or issues"],
  "suggested_reply": "A professional, empathetic, and helpful customer support reply (2-4 sentences)"
}

Guidelines:
- Be objective and fair.
- Extract only real strengths/weaknesses mentioned.
- Confidence should reflect how clear the sentiment is.
- Suggested reply should acknowledge the feedback, thank the customer, and offer help or next steps.
- If the review is mixed, lean towards the overall tone.
"""


def build_user_prompt(review_text: str, product_name: Optional[str] = None) -> str:
    product_context = f"Product: {product_name}\n\n" if product_name else ""
    return f"""{product_context}Please analyze the following product review:

\"\"\"
{review_text}
\"\"\"

Return only the JSON object as specified.
"""


# ==================== Core Analysis Function ====================

def analyze_review_with_gemini(review_text: str, product_name: Optional[str] = None) -> dict:
    """Call Vertex AI Gemini to analyze the review."""
    if not vertex_ready:
        raise HTTPException(
            status_code=500,
            detail="Vertex AI is not properly configured. Please set PROJECT_ID environment variable."
        )

    try:
        model = GenerativeModel(MODEL_NAME)

        generation_config = GenerationConfig(
            temperature=0.2,          # Low temperature for more consistent structured output
            top_p=0.8,
            top_k=40,
            max_output_tokens=1024,
            response_mime_type="application/json"  # Force JSON output
        )

        full_prompt = SYSTEM_PROMPT + "\n\n" + build_user_prompt(review_text, product_name)

        response = model.generate_content(
            full_prompt,
            generation_config=generation_config
        )

        # Parse the JSON response
        result_text = response.text.strip()
        
        # Clean possible markdown fences
        if result_text.startswith("```json"):
            result_text = result_text[7:]
        if result_text.startswith("```"):
            result_text = result_text[3:]
        if result_text.endswith("```"):
            result_text = result_text[:-3]
        result_text = result_text.strip()

        result = json.loads(result_text)
        return result

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse model JSON: {e}\nRaw: {response.text if 'response' in locals() else 'N/A'}")
        raise HTTPException(status_code=500, detail="Model returned invalid JSON. Please try again.")
    except Exception as e:
        logger.error(f"Vertex AI error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calling Vertex AI: {str(e)}")


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """Serve the frontend HTML."""
    for path in POSSIBLE_FRONTEND_PATHS:
        if os.path.exists(path):
            return FileResponse(path)
    return {
        "message": "Product Review Analyzer API is running",
        "docs": "/docs",
        "health": "/health",
        "note": "Frontend HTML not found. API is still fully functional at /api/analyze"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {
        "status": "healthy",
        "vertex_ai_ready": vertex_ready,
        "project_id": PROJECT_ID,
        "model": MODEL_NAME,
        "location": LOCATION
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_review(request: ReviewRequest):
    """
    Analyze a product review using Vertex AI Gemini.
    
    Returns structured insights: sentiment, strengths, weaknesses, summary, and suggested reply.
    """
    logger.info(f"Analyzing review (length={len(request.review_text)})")

    result = analyze_review_with_gemini(
        review_text=request.review_text,
        product_name=request.product_name
    )

    # Validate and normalize response
    sentiment = result.get("sentiment", "Neutral")
    if sentiment not in ["Positive", "Neutral", "Negative"]:
        sentiment = "Neutral"

    confidence = float(result.get("confidence", 0.5))
    confidence = max(0.0, min(1.0, confidence))

    return AnalysisResponse(
        sentiment=sentiment,
        confidence=confidence,
        summary=result.get("summary", ""),
        strengths=result.get("strengths", []),
        weaknesses=result.get("weaknesses", []),
        suggested_reply=result.get("suggested_reply", ""),
        raw_model_output=result
    )


@app.get("/api/info")
async def api_info():
    """Return basic API and model information."""
    return {
        "project": "Vertex AI Product Review Analyzer",
        "model": MODEL_NAME,
        "location": LOCATION,
        "framework": "FastAPI + Vertex AI SDK"
    }


# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
