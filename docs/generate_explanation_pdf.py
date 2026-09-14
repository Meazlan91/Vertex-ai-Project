#!/usr/bin/env python3
"""Generate Project Explanation PDF for Vertex AI GenAI Project"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Preformatted, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

PRIMARY = HexColor("#1a73e8")
DARK = HexColor("#202124")
SECONDARY = HexColor("#5f6368")
SUCCESS = HexColor("#0f9d58")
LIGHT_BG = HexColor("#f8f9fa")
CODE_BG = HexColor("#f1f3f4")

def create_styles():
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='MainTitle', fontSize=22, textColor=PRIMARY,
        alignment=TA_CENTER, spaceAfter=8, fontName='Helvetica-Bold', leading=26
    ))
    styles.add(ParagraphStyle(
        name='SubTitle', fontSize=12, textColor=SECONDARY,
        alignment=TA_CENTER, spaceAfter=20, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        name='Section', fontSize=14, textColor=PRIMARY,
        spaceBefore=18, spaceAfter=8, fontName='Helvetica-Bold'
    ))
    styles.add(ParagraphStyle(
        name='Body', fontSize=10, textColor=DARK,
        alignment=TA_JUSTIFY, spaceAfter=8, leading=14, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        name='BulletText', fontSize=10, textColor=DARK,
        leftIndent=15, spaceAfter=4, leading=13, fontName='Helvetica'
    ))
    styles.add(ParagraphStyle(
        name='CodeBlock', fontSize=8, fontName='Courier',
        backColor=CODE_BG, leftIndent=5, rightIndent=5,
        spaceBefore=4, spaceAfter=8, leading=11
    ))
    styles.add(ParagraphStyle(
        name='Small', fontSize=9, textColor=SECONDARY,
        spaceAfter=6, leading=12
    ))
    styles.add(ParagraphStyle(
        name='Highlight', fontSize=10, textColor=DARK,
        backColor=HexColor("#e8f0fe"), borderPadding=6,
        spaceBefore=6, spaceAfter=8, leading=13
    ))
    return styles

def build_pdf():
    doc = SimpleDocTemplate(
        "/home/workdir/artifacts/vertex-ai-genai-project/docs/Project_Explanation.pdf",
        pagesize=A4,
        rightMargin=0.7*inch,
        leftMargin=0.7*inch,
        topMargin=0.6*inch,
        bottomMargin=0.5*inch
    )
    styles = create_styles()
    story = []

    # Title
    story.append(Spacer(1, 30))
    story.append(Paragraph("Vertex AI GenAI Project", styles['MainTitle']))
    story.append(Paragraph("Intelligent Product Review Analyzer", styles['MainTitle']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "A complete, portfolio-ready Generative AI application using Google Cloud Vertex AI (Gemini)",
        styles['SubTitle']
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceBefore=5, spaceAfter=15))

    # 1. Project Overview
    story.append(Paragraph("1. Project Overview", styles['Section']))
    story.append(Paragraph(
        "This project is a full-stack Generative AI application that uses <b>Google Cloud Vertex AI Gemini</b> "
        "to analyze product reviews and generate structured, actionable insights. It is designed to be "
        "production-ready, easily deployable to <b>Cloud Run</b>, and excellent for portfolios and interviews.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>What the application does:</b> A user pastes a product review → the system returns Sentiment, "
        "Confidence score, Summary, Key Strengths, Key Weaknesses, and a professional Suggested Customer Support Reply.",
        styles['Body']
    ))

    # 2. Architecture
    story.append(Paragraph("2. System Architecture", styles['Section']))
    story.append(Paragraph(
        "The architecture follows a clean, modern serverless pattern:",
        styles['Body']
    ))
    story.append(Paragraph("• <b>Frontend</b>: Single-page application (HTML + CSS + Vanilla JS) served by the backend.", styles['BulletText']))
    story.append(Paragraph("• <b>Backend</b>: FastAPI (Python) running on Cloud Run.", styles['BulletText']))
    story.append(Paragraph("• <b>AI Layer</b>: Vertex AI Gemini (gemini-1.5-flash recommended for speed & cost).", styles['BulletText']))
    story.append(Paragraph("• <b>Deployment</b>: Fully containerized, auto-scaling, pay-per-use on Cloud Run.", styles['BulletText']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>Request Flow:</b> Browser → Cloud Run (FastAPI) → Vertex AI Gemini → Structured JSON → Beautiful UI",
        styles['Highlight']
    ))

    # 3. Key Features
    story.append(Paragraph("3. Key Features", styles['Section']))
    features = [
        "Sentiment Analysis (Positive / Neutral / Negative) with confidence score",
        "Automatic extraction of Strengths and Weaknesses",
        "Concise natural language summary of the review",
        "AI-generated professional customer support reply",
        "Modern, responsive UI with loading states and error handling",
        "Health check endpoint for Cloud Run readiness probes",
        "Forced JSON output from Gemini for reliable structured responses",
        "Easy one-command deployment script"
    ]
    for f in features:
        story.append(Paragraph(f"• {f}", styles['BulletText']))

    # 4. Tech Stack
    story.append(Paragraph("4. Technology Stack", styles['Section']))
    
    data = [
        ['Layer', 'Technology'],
        ['Backend Framework', 'FastAPI + Uvicorn'],
        ['AI / LLM', 'Vertex AI Gemini 1.5 Flash / Pro'],
        ['SDK', 'google-cloud-aiplatform'],
        ['Frontend', 'HTML5 + CSS3 + Vanilla JavaScript'],
        ['Container', 'Docker'],
        ['Deployment', 'Google Cloud Run'],
        ['CI/CD Ready', 'Cloud Build + Source Deploy'],
        ['Configuration', 'python-dotenv + Environment Variables'],
    ]
    table = Table(data, colWidths=[2.2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.4, HexColor("#dadce0")),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_BG),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))

    # 5. Prompt Engineering
    story.append(Paragraph("5. Prompt Engineering Highlights", styles['Section']))
    story.append(Paragraph(
        "One of the most important parts of any GenAI project is the prompt. In this project we use:",
        styles['Body']
    ))
    story.append(Paragraph("• A clear <b>system prompt</b> that defines the role (Customer Experience Analyst).", styles['BulletText']))
    story.append(Paragraph("• Strict <b>JSON schema</b> instruction so the model returns structured data every time.", styles['BulletText']))
    story.append(Paragraph("• Low temperature (0.2) for more deterministic and reliable outputs.", styles['BulletText']))
    story.append(Paragraph("• <b>response_mime_type='application/json'</b> (Gemini feature) to force valid JSON.", styles['BulletText']))
    story.append(Paragraph("• Post-processing to clean markdown fences if the model still adds them.", styles['BulletText']))

    # 6. How to Run
    story.append(Paragraph("6. How to Run the Project", styles['Section']))
    story.append(Paragraph("<b>Local Development:</b>", styles['Body']))
    story.append(Preformatted("""cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # Edit PROJECT_ID
gcloud auth application-default login
uvicorn main:app --reload --port 8080""", styles['CodeBlock']))

    story.append(Paragraph("<b>Deploy to Cloud Run (one command):</b>", styles['Body']))
    story.append(Preformatted("""./scripts/deploy.sh YOUR_GCP_PROJECT_ID us-central1""", styles['CodeBlock']))

    # 7. Learning Outcomes
    story.append(Paragraph("7. What You Learn / Interview Talking Points", styles['Section']))
    story.append(Paragraph("This project demonstrates strong practical skills in:", styles['Body']))
    points = [
        "<b>Vertex AI & Gemini</b> – Calling generative models, prompt design, structured output",
        "<b>FastAPI</b> – Modern Python web APIs, Pydantic validation, CORS, static file serving",
        "<b>Cloud Run</b> – Serverless containers, environment variables, auto-scaling, health checks",
        "<b>Docker</b> – Containerizing a Python application correctly",
        "<b>Prompt Engineering</b> – System prompts, JSON mode, temperature control",
        "<b>Full-stack thinking</b> – Connecting frontend ↔ backend ↔ AI service cleanly",
        "<b>Production readiness</b> – Error handling, logging, configuration management"
    ]
    for p in points:
        story.append(Paragraph(f"• {p}", styles['BulletText']))

    # 8. Cost Estimation
    story.append(Paragraph("8. Cost Estimation (Approximate)", styles['Section']))
    story.append(Paragraph(
        "Gemini 1.5 Flash is extremely cost-effective. For typical portfolio / demo usage:",
        styles['Body']
    ))
    story.append(Paragraph("• A few hundred analyses per month → usually stays within free tier or costs < $1-2.", styles['BulletText']))
    story.append(Paragraph("• Cloud Run with min-instances=0 → pay only when requests come in.", styles['BulletText']))
    story.append(Paragraph("• Always set a <b>budget alert</b> in Google Cloud Console.", styles['BulletText']))

    # 9. Future Enhancements
    story.append(Paragraph("9. Possible Future Enhancements", styles['Section']))
    enhancements = [
        "Store analysis history in Firestore or Cloud SQL",
        "Add user authentication (Firebase Auth / Identity Platform)",
        "Batch analysis of multiple reviews (CSV upload)",
        "Support for multiple languages",
        "Fine-tune or use grounding with your own product documents (RAG)",
        "Add evaluation metrics (how accurate is the sentiment?)",
        "Stream responses using Gemini streaming API",
        "Multi-turn conversation (chat about the review)"
    ]
    for e in enhancements:
        story.append(Paragraph(f"• {e}", styles['BulletText']))

    # 10. Conclusion
    story.append(Paragraph("10. Conclusion", styles['Section']))
    story.append(Paragraph(
        "This project is intentionally designed to be <b>complete, clean, and interview-ready</b>. "
        "It shows that you can take a real business problem (understanding customer feedback at scale), "
        "solve it using modern Generative AI on Google Cloud, and deliver a polished full-stack application.",
        styles['Body']
    ))
    story.append(Paragraph(
        "You can confidently put this on your resume / GitHub and talk about architecture decisions, "
        "prompt engineering choices, cost optimization, and deployment strategy in interviews.",
        styles['Body']
    ))

    story.append(Spacer(1, 25))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=5, spaceAfter=10))
    story.append(Paragraph(
        "Project created for learning Google Cloud + Generative AI with Vertex AI • Ready for portfolio use",
        styles['SubTitle']
    ))

    doc.build(story)
    print("PDF generated successfully!")

if __name__ == "__main__":
    build_pdf()
