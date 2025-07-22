#!/bin/bash

# 📚 Mental Health Analyzer - Documentation Server Launcher
# =========================================================
# 
# This script starts the documentation server for the Mental Health Analyzer project.
# It handles environment setup, dependency checking, and launches the server.
#
# Usage: ./start_docs_server.sh [port]
# Default port: 8000

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_PORT=8000
PORT=${1:-$DEFAULT_PORT}
VENV_DIR="venv"
DOCS_SERVER_SCRIPT="docs_server.py"

# Function to print colored output
print_status() {
    echo -e "${BLUE}📚 [DOCS]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ [SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️  [WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}❌ [ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to detect Python command
detect_python() {
    if command_exists python3; then
        echo "python3"
    elif command_exists python; then
        echo "python"
    else
        return 1
    fi
}

# Header
echo "🧠 Mental Health Analyzer - Documentation Server"
echo "================================================="
echo ""

# Check if we're in the right directory
if [[ ! -f "$DOCS_SERVER_SCRIPT" ]]; then
    print_error "docs_server.py not found in current directory!"
    print_status "Please run this script from the project root directory."
    exit 1
fi

# Detect Python
print_status "Detecting Python installation..."
PYTHON_CMD=$(detect_python)
if [[ $? -ne 0 ]]; then
    print_error "Python not found! Please install Python 3.8+ first."
    print_status "Visit: https://python.org/downloads/"
    exit 1
fi

print_success "Found Python: $PYTHON_CMD"

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
print_status "Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [[ -d "$VENV_DIR" ]]; then
    print_status "Virtual environment found at: $VENV_DIR"
    
    # Activate virtual environment
    if [[ -f "$VENV_DIR/bin/activate" ]]; then
        print_status "Activating virtual environment..."
        source "$VENV_DIR/bin/activate"
    elif [[ -f "$VENV_DIR/Scripts/activate" ]]; then
        print_status "Activating virtual environment (Windows)..."
        source "$VENV_DIR/Scripts/activate"
    else
        print_warning "Virtual environment activation script not found"
    fi
else
    print_warning "Virtual environment not found at: $VENV_DIR"
    print_status "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    
    # Activate newly created virtual environment
    if [[ -f "$VENV_DIR/bin/activate" ]]; then
        source "$VENV_DIR/bin/activate"
    elif [[ -f "$VENV_DIR/Scripts/activate" ]]; then
        source "$VENV_DIR/Scripts/activate"
    fi
    
    print_success "Virtual environment created and activated"
fi

# Check if requirements are installed
print_status "Checking dependencies..."
if ! $PYTHON_CMD -c "import flask, markdown, pygments" >/dev/null 2>&1; then
    print_warning "Some dependencies are missing. Installing from requirements.txt..."
    
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found!"
        print_status "Installing minimal dependencies for docs server..."
        pip install flask markdown pygments
    fi
else
    print_success "All dependencies are available"
fi

# Check if port is available
if command_exists lsof; then
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $PORT is already in use!"
        print_status "Trying to find an available port..."
        
        # Find next available port
        for ((test_port=PORT+1; test_port<=PORT+10; test_port++)); do
            if ! lsof -Pi :$test_port -sTCP:LISTEN -t >/dev/null 2>&1; then
                PORT=$test_port
                print_success "Found available port: $PORT"
                break
            fi
        done
        
        if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
            print_error "No available ports found in range ${DEFAULT_PORT}-$((DEFAULT_PORT+10))"
            exit 1
        fi
    fi
fi

# Create docs directory structure if it doesn't exist
if [[ ! -d "docs" ]]; then
    print_status "Creating docs directory structure..."
    mkdir -p docs/static docs/templates
fi

# Set environment variables for the docs server
export DOCS_PORT=$PORT
export FLASK_ENV=development

# Start the documentation server
print_status "Starting documentation server on port $PORT..."
print_status "Server will be available at: http://127.0.0.1:$PORT"
print_status "Press Ctrl+C to stop the server"
echo ""

# Launch the server with error handling
if $PYTHON_CMD "$DOCS_SERVER_SCRIPT" --port "$PORT"; then
    print_success "Documentation server stopped gracefully"
else
    exit_code=$?
    print_error "Documentation server failed with exit code: $exit_code"
    
    if [[ $exit_code -eq 1 ]]; then
        print_status "Common fixes:"
        print_status "  1. Check if all dependencies are installed: pip install -r requirements.txt"
        print_status "  2. Ensure you're in the project root directory"
        print_status "  3. Check if port $PORT is available"
        print_status "  4. Try running with a different port: ./start_docs_server.sh 8001"
    fi
    
    exit $exit_code
fi 