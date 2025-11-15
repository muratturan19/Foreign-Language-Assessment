#!/bin/bash

# Local Development Setup Script for Foreign Language Assessment Platform
# This script checks for required dependencies and sets up the development environment

set -e

echo "================================================"
echo "Foreign Language Assessment - Local Setup"
echo "================================================"
echo ""

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check for FFmpeg
echo "Checking for FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n 1)
    print_success "FFmpeg is installed: $FFMPEG_VERSION"
else
    print_error "FFmpeg is NOT installed"
    echo ""
    echo "FFmpeg is required for audio file processing."
    echo "Please install FFmpeg using one of the following methods:"
    echo ""

    # Detect OS and provide appropriate installation instructions
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Ubuntu/Debian:"
        echo "    sudo apt-get update && sudo apt-get install -y ffmpeg"
        echo ""
        echo "  Fedora/CentOS/RHEL:"
        echo "    sudo dnf install ffmpeg"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  macOS (Homebrew):"
        echo "    brew install ffmpeg"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        echo "  Windows (Chocolatey):"
        echo "    choco install ffmpeg"
        echo ""
        echo "  Windows (Manual):"
        echo "    1. Download from https://ffmpeg.org/download.html"
        echo "    2. Extract to C:\\ffmpeg"
        echo "    3. Add C:\\ffmpeg\\bin to PATH"
    fi
    echo ""
    print_warning "Please install FFmpeg and run this script again"
    exit 1
fi

# Check for Python
echo "Checking for Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python is installed: $PYTHON_VERSION"
else
    print_error "Python 3 is NOT installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

# Check for Node.js
echo "Checking for Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js is installed: $NODE_VERSION"
else
    print_error "Node.js is NOT installed"
    echo "Please install Node.js 18.x or higher"
    exit 1
fi

# Check for npm
echo "Checking for npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm is installed: v$NPM_VERSION"
else
    print_error "npm is NOT installed"
    echo "Please install npm (comes with Node.js)"
    exit 1
fi

echo ""
echo "================================================"
echo "Setting up environment files..."
echo "================================================"
echo ""

# Setup .env files
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        print_success "Created .env from .env.example"
        print_warning "Please edit .env and configure your settings"
    else
        print_warning ".env.example not found, skipping .env creation"
    fi
else
    print_success ".env already exists"
fi

if [ ! -f "frontend/.env" ]; then
    if [ -f "frontend/.env.example" ]; then
        cp frontend/.env.example frontend/.env
        print_success "Created frontend/.env from frontend/.env.example"
        print_warning "Please edit frontend/.env and configure your settings"
    else
        print_warning "frontend/.env.example not found, skipping frontend/.env creation"
    fi
else
    print_success "frontend/.env already exists"
fi

echo ""
echo "================================================"
echo "Installing backend dependencies..."
echo "================================================"
echo ""

# Setup Python virtual environment
if [ ! -d "backend/.venv" ]; then
    print_warning "Creating Python virtual environment..."
    cd backend
    python3 -m venv .venv
    cd ..
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate venv and install dependencies
print_warning "Installing Python packages..."
source backend/.venv/bin/activate
pip install -q --upgrade pip
pip install -q -r backend/requirements.txt
print_success "Backend dependencies installed"

echo ""
echo "================================================"
echo "Installing frontend dependencies..."
echo "================================================"
echo ""

cd frontend
npm install
cd ..
print_success "Frontend dependencies installed"

echo ""
echo "================================================"
print_success "Setup completed successfully!"
echo "================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your environment variables:"
echo "   - Edit .env (backend configuration)"
echo "   - Edit frontend/.env (frontend configuration)"
echo "   - Make sure APP_SECRET_TOKEN matches in both files"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   source .venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3. Start the frontend (in a new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open http://localhost:5173 in your browser"
echo ""
