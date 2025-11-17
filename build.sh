#!/bin/bash
set -e

echo "Installing FFmpeg (static binary)..."
mkdir -p /opt/render/project/.ffmpeg
cd /opt/render/project/.ffmpeg
wget -q https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
tar xf ffmpeg-release-amd64-static.tar.xz --strip-components=1
rm ffmpeg-release-amd64-static.tar.xz
export PATH="/opt/render/project/.ffmpeg:$PATH"
echo "FFmpeg installed: $(ffmpeg -version | head -1)"

cd /opt/render/project/src

echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "Installing frontend dependencies..."
cd frontend
npm ci

echo "Building frontend..."
npm run build

echo "Build completed successfully!"
