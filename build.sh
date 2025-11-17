#!/bin/bash
set -e

echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "Installing frontend dependencies..."
cd frontend
npm ci --only=production

echo "Building frontend..."
npm run build

echo "Build completed successfully!"
