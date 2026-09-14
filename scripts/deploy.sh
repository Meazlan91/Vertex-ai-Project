#!/bin/bash
set -e

# Usage: ./scripts/deploy.sh PROJECT_ID [REGION]

PROJECT_ID=${1:-""}
REGION=${2:-"us-central1"}
SERVICE_NAME="review-analyzer"

if [ -z "$PROJECT_ID" ]; then
  echo "Usage: ./scripts/deploy.sh YOUR_PROJECT_ID [REGION]"
  echo "Example: ./scripts/deploy.sh my-gcp-project us-central1"
  exit 1
fi

echo "============================================"
echo " Deploying Vertex AI Review Analyzer"
echo " Project : $PROJECT_ID"
echo " Region  : $REGION"
echo "============================================"

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "→ Enabling required APIs..."
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  --quiet

# Deploy using Cloud Run source-based deployment
echo "→ Deploying to Cloud Run (this may take 2-4 minutes)..."

cd "$(dirname "$0")/../backend"

gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "PROJECT_ID=$PROJECT_ID,LOCATION=$REGION,MODEL_NAME=gemini-1.5-flash-001" \
  --memory 1Gi \
  --cpu 1 \
  --timeout 60 \
  --min-instances 0 \
  --max-instances 10 \
  --quiet

echo ""
echo "============================================"
echo " Deployment successful!"
echo "============================================"
echo ""
echo "Service URL:"
gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)'
echo ""
echo "Test the API:"
echo "curl -X POST \$(gcloud run services describe $SERVICE_NAME --region $REGION --format='value(status.url)')/api/analyze \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"review_text\": \"Great product, battery lasts forever!\"}'"
echo ""
