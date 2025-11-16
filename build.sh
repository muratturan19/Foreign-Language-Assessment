#!/usr/bin/env bash
set -euo pipefail

echo "======================================"
echo "Installing FFmpeg for audio processing"
echo "======================================"
# Install FFmpeg system package (required for audio conversion)
apt-get update && apt-get install -y ffmpeg

echo "======================================"
echo "Installing Python dependencies"
echo "======================================"
# Upgrade pip and install Python dependencies
python -m pip install --upgrade pip
python -m pip install --requirement backend/requirements.txt

echo "======================================"
echo "Building frontend"
echo "======================================"
# Install frontend dependencies (including devDependencies for build)
npm install --prefix frontend --production=false

# Build frontend with Render's auto-generated URL
# RENDER_EXTERNAL_URL is automatically available during build
export VITE_API_BASE_URL=${RENDER_EXTERNAL_URL:-http://localhost:8000}
npm run build --prefix frontend

echo "======================================"
echo "Build completed successfully!"
echo "======================================"
