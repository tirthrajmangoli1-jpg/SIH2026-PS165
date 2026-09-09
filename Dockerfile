# Multi-stage Dockerfile for OIL SIF-Sentinel
# Smart India Hackathon: PS 165
# Single Unified Container (Frontend + Backend + NLP Engine)

FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.9-slim AS backend-runner
WORKDIR /app

# Install system dependencies for scientific libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/app ./app
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    pydantic \
    sqlalchemy \
    spacy \
    faiss-cpu \
    hdbscan \
    scikit-learn \
    numpy

# Download spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy built frontend from stage 1 into the location expected by main.py
COPY --from=frontend-builder /app/frontend/dist /frontend/dist

# Expose unified port 8000
EXPOSE 8000

ENV HOST=0.0.0.0
ENV PORT=8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
