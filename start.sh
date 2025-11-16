#!/usr/bin/env bash
set -euo pipefail

echo "Starting FastAPI backend server..."

# Start the FastAPI backend
exec uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
