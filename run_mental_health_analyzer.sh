#!/bin/bash

# Mental Health Analyzer - Complete Setup and Run Script
# This script handles everything: setup, dependencies, port cleanup, and running the app

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
DEFAULT_PORT=5000
FALLBACK_PORT=5001
APP_NAME="Mental Health Analyzer"
VENV_DIR="venv"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║           🧠 Mental Health Analyzer Setup 🧠            ║"
    echo "║                Complete Setup & Run Script               ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_final_success() {
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║  🎉 Mental Health Analyzer is RUNNING! 🎉              ║"
    echo "║                                                          ║"
    echo "║  🌐 Open your browser and go to:                        ║"
    echo "║     http://127.0.0.1:${SELECTED_PORT}                               ║"
    echo "║     http://localhost:${SELECTED_PORT}                               ║"
    echo "║                                                          ║"
    echo "║  💡 Features available:                                  ║"
    echo "║     • Text Sentiment Analysis                            ║"
    echo "║     • Voice Emotion Analysis                             ║"
    echo "║     • Facial Expression Analysis                        ║"
    echo "║     • Combined Mental Health Assessment                  ║"
    echo "║                                                          ║"
    echo "║  ⏹️  Press Ctrl+C to stop the server                    ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to kill processes on ports
kill_port_processes() {
    local port=$1
    print_status "Checking for existing processes on port $port..."
    
    # Try multiple methods to kill processes on the port
    if command_exists lsof; then
        local pids=$(lsof -ti:$port 2>/dev/null || true)
        if [ ! -z "$pids" ]; then
            print_warning "Found existing processes on port $port. Stopping them..."
            echo "$pids" | xargs kill -9 2>/dev/null || true
            sleep 1
            print_success "Processes on port $port stopped ✓"
        fi
    fi
    
    # Alternative method using netstat and ps
    if command_exists netstat && command_exists ps; then
        local pids=$(netstat -tlnp 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1 2>/dev/null || true)
        if [ ! -z "$pids" ]; then
            echo "$pids" | xargs kill -9 2>/dev/null || true
            sleep 1
        fi
    fi
    
    # Kill any python processes that might be running Flask
    pkill -f "python.*app.py" 2>/dev/null || true
    pkill -f "flask.*run" 2>/dev/null || true
    
    print_success "Port cleanup completed ✓"
}

# Function to check if port is available
is_port_available() {
    local port=$1
    if command_exists nc; then
        ! nc -z 127.0.0.1 $port 2>/dev/null
    elif command_exists telnet; then
        ! timeout 1 telnet 127.0.0.1 $port 2>/dev/null | grep -q "Connected"
    elif command_exists lsof; then
        ! lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1
    else
        # Fallback: assume available
        true
    fi
}

# Function to find available port
find_available_port() {
    print_status "Finding available port..."
    
    # Try default port first
    if is_port_available $DEFAULT_PORT; then
        SELECTED_PORT=$DEFAULT_PORT
        print_success "Port $DEFAULT_PORT is available ✓"
        return 0
    fi
    
    # Try fallback port
    if is_port_available $FALLBACK_PORT; then
        SELECTED_PORT=$FALLBACK_PORT
        print_success "Port $FALLBACK_PORT is available ✓"
        return 0
    fi
    
    # Try other ports
    for port in {5002..5010}; do
        if is_port_available $port; then
            SELECTED_PORT=$port
            print_success "Port $port is available ✓"
            return 0
        fi
    done
    
    print_error "No available ports found in range 5000-5010"
    exit 1
}

# Function to check Python version
check_python_requirements() {
    print_status "Checking Python requirements..."
    
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi

    # Check Python version
    PYTHON_VERSION=$(${PYTHON_CMD} -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>/dev/null || echo "0.0")
    REQUIRED_VERSION="3.8"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
        print_success "Python ${PYTHON_VERSION} detected ✓"
    else
        print_error "Python ${PYTHON_VERSION} is installed, but version 3.8+ is required."
        exit 1
    fi
    
    # Check if pip is available
    if ! command_exists pip && ! ${PYTHON_CMD} -m pip --version >/dev/null 2>&1; then
        print_error "pip is not installed. Please install pip first."
        exit 1
    fi
    print_success "pip detected ✓"
}

# Function to setup virtual environment
setup_virtual_environment() {
    print_status "Setting up Python virtual environment..."
    
    # Remove existing venv if it exists and has issues
    if [ -d "$VENV_DIR" ]; then
        print_status "Checking existing virtual environment..."
        if ! source "$VENV_DIR/bin/activate" 2>/dev/null || ! python -c "import flask" 2>/dev/null; then
            print_warning "Existing virtual environment has issues. Recreating..."
            rm -rf "$VENV_DIR"
        else
            print_success "Existing virtual environment is functional ✓"
            return 0
        fi
    fi
    
    # Create new virtual environment
    print_status "Creating fresh virtual environment..."
    ${PYTHON_CMD} -m venv "$VENV_DIR" || {
        print_error "Failed to create virtual environment"
        exit 1
    }
    
    print_success "Virtual environment created ✓"
}

# Function to activate virtual environment
activate_virtual_environment() {
    print_status "Activating virtual environment..."
    
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source "$VENV_DIR/Scripts/activate"
    else
        source "$VENV_DIR/bin/activate"
    fi
    
    # Verify activation
    if [ "$VIRTUAL_ENV" != "" ]; then
        print_success "Virtual environment activated ✓"
    else
        print_error "Failed to activate virtual environment"
        exit 1
    fi
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Upgrade pip first
    python -m pip install --upgrade pip setuptools wheel 2>/dev/null || {
        print_warning "Failed to upgrade pip, but continuing..."
    }
    
    # Install core dependencies first
    print_status "Installing core packages..."
    python -m pip install Flask Werkzeug || {
        print_error "Failed to install Flask"
        exit 1
    }
    
    # Install analysis dependencies
    print_status "Installing analysis packages..."
    python -m pip install numpy scikit-learn nltk textblob vaderSentiment || {
        print_error "Failed to install core analysis packages"
        exit 1
    }
    
    # Install optional packages (don't fail if these don't work)
    print_status "Installing optional packages..."
    python -m pip install pandas matplotlib seaborn 2>/dev/null || print_warning "Some optional packages failed to install"
    python -m pip install soundfile librosa 2>/dev/null || print_warning "Audio packages failed to install (voice analysis may not work)"
    python -m pip install opencv-python Pillow 2>/dev/null || print_warning "Computer vision packages failed to install (facial analysis may not work)"
    
    print_success "Dependencies installation completed ✓"
}

# Function to setup NLTK data
setup_nltk_data() {
    print_status "Setting up NLTK data..."
    
    python -c "
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    print('NLTK data downloaded successfully')
except:
    print('NLTK data download failed, but continuing...')
" 2>/dev/null || print_warning "NLTK data setup had issues, but app should still work"
    
    print_success "NLTK data setup completed ✓"
}

# Function to verify project structure
verify_project_structure() {
    print_status "Verifying project structure..."
    
    local required_files=("app.py" "templates/index.html" "static/js/app.js" "static/js/recorder.js" "questions/questions.json")
    local missing_files=()
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        print_error "Missing required files:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi
    
    print_success "Project structure verified ✓"
}

# Function to test app before starting
test_app() {
    print_status "Testing application..."
    
    # Quick syntax check
    python -c "
import sys
sys.path.insert(0, '.')
try:
    import app
    print('App syntax check passed')
except Exception as e:
    print(f'App syntax error: {e}')
    sys.exit(1)
" || {
        print_error "Application has syntax errors"
        exit 1
    }
    
    print_success "Application test passed ✓"
}

# Function to open browser
open_browser() {
    local url="http://127.0.0.1:${SELECTED_PORT}"
    
    # Wait a moment for server to start
    sleep 2
    
    # Try to open browser automatically
    if command_exists open; then
        # macOS
        open "$url" >/dev/null 2>&1 &
    elif command_exists xdg-open; then
        # Linux
        xdg-open "$url" >/dev/null 2>&1 &
    elif command_exists start; then
        # Windows
        start "$url" >/dev/null 2>&1 &
    else
        print_status "Please open your browser manually and go to: $url"
    fi
}

# Function to start the application
start_application() {
    print_status "Starting Mental Health Analyzer..."
    
    # Set the port environment variable
    export PORT=$SELECTED_PORT
    
    # Start the application in background briefly to test
    print_status "Performing startup test..."
    timeout 5 python app.py >/dev/null 2>&1 &
    local test_pid=$!
    
    # Wait a moment and check if it started successfully
    sleep 2
    if kill -0 $test_pid 2>/dev/null; then
        # Kill the test process
        kill $test_pid 2>/dev/null || true
        wait $test_pid 2>/dev/null || true
        print_success "Startup test successful ✓"
    else
        print_error "Application failed to start during test"
        exit 1
    fi
    
    # Show success message
    print_final_success
    
    # Open browser
    open_browser &
    
    # Start the application for real
    print_status "Starting server (Press Ctrl+C to stop)..."
    echo ""
    python app.py
}

# Function to cleanup on exit
cleanup() {
    print_status "Cleaning up..."
    # Kill any background processes
    jobs -p | xargs -r kill 2>/dev/null || true
    print_success "Cleanup completed. Thank you for using Mental Health Analyzer!"
}

# Trap cleanup function on script exit
trap cleanup EXIT INT TERM

# Main execution function
main() {
    print_header
    
    # Change to script directory
    cd "$(dirname "$0")"
    
    print_status "Starting complete setup and run process..."
    
    # Kill any existing processes on common ports
    kill_port_processes $DEFAULT_PORT
    kill_port_processes $FALLBACK_PORT
    
    # Find available port
    find_available_port
    
    # Check requirements
    check_python_requirements
    
    # Setup virtual environment
    setup_virtual_environment
    
    # Activate virtual environment
    activate_virtual_environment
    
    # Install dependencies
    install_dependencies
    
    # Setup NLTK data
    setup_nltk_data
    
    # Verify project structure
    verify_project_structure
    
    # Test application
    test_app
    
    print_success "Setup completed successfully! 🎉"
    echo ""
    
    # Start the application
    start_application
}

# Check if we're in the right directory
if [ ! -f "app.py" ] && [ ! -f "requirement.md" ]; then
    print_error "This doesn't appear to be the Mental Health Analyzer directory."
    print_error "Please run this script from the project root directory."
    exit 1
fi

# Run main function
main "$@" 