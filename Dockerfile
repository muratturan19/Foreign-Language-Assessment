# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Install system dependencies including FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy frontend package files
COPY frontend/package*.json frontend/
WORKDIR /app/frontend
RUN npm ci --only=production

# Copy all application files
WORKDIR /app
COPY . .

# Build frontend
WORKDIR /app/frontend
RUN npm run build

# Set working directory back to app root
WORKDIR /app

# Create directories for data persistence
RUN mkdir -p backend/audio_files backend/reports

# Expose port (Render provides this via $PORT env var)
EXPOSE 8000

# Start command - use environment variable PORT from Render
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
