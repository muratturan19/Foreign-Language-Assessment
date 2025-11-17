#!/bin/bash
set -e

echo "============================================"
echo "🔧 BUILD SCRIPT STARTED"
echo "============================================"
echo "Current directory: $(pwd)"
echo "Current user: $(whoami)"
echo "============================================"

echo "📦 Installing FFmpeg (static binary)..."
mkdir -p /opt/render/project/.ffmpeg
cd /opt/render/project/.ffmpeg
echo "  ↳ Downloading FFmpeg from johnvansickle.com..."
wget -q https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
echo "  ↳ Extracting FFmpeg..."
tar xf ffmpeg-release-amd64-static.tar.xz --strip-components=1
rm ffmpeg-release-amd64-static.tar.xz
export PATH="/opt/render/project/.ffmpeg:$PATH"
echo "  ✅ FFmpeg installed: $(ffmpeg -version | head -1)"
echo ""

cd /opt/render/project/src

echo "🐍 Installing backend dependencies..."
pip install -r backend/requirements.txt
echo "  ✅ Backend dependencies installed"
echo ""

echo "📦 Installing frontend dependencies..."
cd frontend
npm ci
echo "  ✅ Frontend dependencies installed"
echo ""

echo "🏗️  Building frontend..."
npm run build
echo "  ✅ Frontend build completed"
echo ""

echo "============================================"
echo "✅ BUILD COMPLETED SUCCESSFULLY!"
echo "============================================"
