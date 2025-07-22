# 🛠️ Development Setup Guide

## Complete Development Environment Setup

This guide will help you set up a complete development environment for the Mental Health Analyzer project, perfect for learning and extending the codebase.

## 🎯 Prerequisites

### Required Software
- **Python 3.8+** - [Download from python.org](https://python.org/downloads/)
- **Git** - [Download from git-scm.com](https://git-scm.com/downloads)
- **Code Editor** - VS Code, PyCharm, or Cursor (recommended)
- **Modern Web Browser** - Chrome, Firefox, or Safari

### System Requirements
- **RAM**: Minimum 4GB, recommended 8GB+
- **Storage**: At least 2GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

## 📥 Project Setup

### 1. Clone the Repository
```bash
# Clone the project
git clone <repository-url>
cd mental-health-analyzer-tool

# Or if you have the project files locally
cd mental-health-analyzer-tool
```

### 2. Python Environment Setup
```bash
# Check Python version
python --version  # Should be 3.8 or higher

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
which python  # Should point to venv/bin/python
```

### 3. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list

# If you get any errors, try upgrading pip first:
pip install --upgrade pip
```

### 4. Download Required Data
```bash
# Download NLTK data (required for text analysis)
python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
print('NLTK data downloaded successfully!')
"
```

## 🧪 Verify Installation

### Test Basic Setup
```bash
# Create and run a simple test
cat > test_setup.py << EOF
#!/usr/bin/env python3
"""Test script to verify all dependencies are working"""

def test_imports():
    try:
        import flask
        print("✅ Flask imported successfully")
        
        import nltk
        print("✅ NLTK imported successfully")
        
        import textblob
        print("✅ TextBlob imported successfully")
        
        import librosa
        print("✅ Librosa imported successfully")
        
        import cv2
        print("✅ OpenCV imported successfully")
        
        import numpy
        print("✅ NumPy imported successfully")
        
        print("\n🎉 All dependencies are working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
EOF

# Run the test
python test_setup.py
```

### Test Core Functionality
```bash
# Test text analysis
python -c "
from analysis.text_analysis import TextAnalyzer
analyzer = TextAnalyzer()
result = analyzer.analyze('I feel great today!')
print('Text analysis working:', 'sentiment' in result)
"

# Test voice analysis (if audio files are available)
python -c "
try:
    from analysis.voice_analysis import VoiceAnalyzer
    print('Voice analysis module loaded successfully')
except Exception as e:
    print('Voice analysis test skipped:', e)
"
```

## 🚀 Running the Application

### Start the Main Application
```bash
# Run the Flask app
python app.py

# You should see:
# Running on http://127.0.0.1:5000
# Press CTRL+C to quit
```

### Start the Documentation Server
```bash
# In a new terminal, activate the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the docs server
python docs_server.py

# You should see:
# Documentation starting on http://127.0.0.1:8000
```

### Test in Browser
1. **Main App**: Open `http://127.0.0.1:5000`
2. **Documentation**: Open `http://127.0.0.1:8000`
3. **Test Features**:
   - Try text analysis with "I feel amazing today!"
   - Test voice recording (allow microphone access)
   - Upload a sample image for facial analysis

## 🔧 IDE Configuration

### VS Code Setup
```json
// .vscode/settings.json
{
    "python.pythonPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "files.associations": {
        "*.py": "python",
        "*.html": "html",
        "*.js": "javascript"
    },
    "emmet.includeLanguages": {
        "javascript": "javascriptreact"
    }
}
```

### Recommended VS Code Extensions
```bash
# Install useful extensions
code --install-extension ms-python.python
code --install-extension ms-python.flake8
code --install-extension esbenp.prettier-vscode
code --install-extension bradlc.vscode-tailwindcss
code --install-extension formulahendry.auto-rename-tag
```

### PyCharm Configuration
1. **Open Project**: File → Open → Select project folder
2. **Configure Interpreter**: Settings → Project → Python Interpreter → Add → Existing Environment → Select `venv/bin/python`
3. **Enable Git**: VCS → Enable Version Control Integration
4. **Run Configuration**: Add new Flask run configuration pointing to `app.py`

## 🗂️ Development Workflow

### Project Structure Understanding
```
mental-health-analyzer-tool/
├── 📱 Frontend Files
│   ├── templates/index.html      # Main UI template
│   ├── static/css/style.css      # Styling
│   └── static/js/               # JavaScript logic
│       ├── app.js               # Main application
│       ├── recorder.js          # Audio recording
│       └── voiceRecorder.js     # Enhanced voice features
│
├── 🧠 Backend Files  
│   ├── app.py                   # Flask web server
│   ├── analysis/                # ML analysis modules
│   │   ├── text_analysis.py     # NLP processing
│   │   ├── voice_analysis.py    # Audio processing
│   │   └── facial_analysis.py   # Computer vision
│   └── utils/                   # Helper functions
│
├── 📚 Documentation
│   ├── docs/                    # Documentation files
│   └── docs_server.py           # Documentation server
│
├── 📋 Configuration
│   ├── requirements.txt         # Python dependencies
│   ├── questions/questions.json # Mental health questions
│   └── README.md               # Project overview
│
└── 🧪 Testing
    └── test_setup.py           # Setup verification
```

### Git Workflow
```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial project setup"

# Create development branch
git checkout -b feature/my-feature

# Make changes and commit regularly
git add .
git commit -m "Add new feature: describe what you added"

# Push to remote (if using GitHub/GitLab)
git push origin feature/my-feature
```

### Development Commands
```bash
# Start development servers (in separate terminals)
# Terminal 1: Main application
python app.py

# Terminal 2: Documentation
python docs_server.py

# Terminal 3: Development commands
# Install new package
pip install package-name
pip freeze > requirements.txt  # Update requirements

# Run tests
python test_setup.py

# Check code style
flake8 analysis/ --max-line-length=88
black analysis/  # Auto-format code
```

## 🐛 Debugging Setup

### Python Debugging
```python
# Add to your code for debugging
import pdb; pdb.set_trace()  # Python debugger breakpoint

# Or use logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Flask Debug Mode
```python
# In app.py, enable debug mode
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

# This enables:
# - Automatic reload on code changes
# - Detailed error pages
# - Interactive debugger in browser
```

### Browser Developer Tools
```javascript
// Add to JavaScript for debugging
console.log('Debug info:', variable);
console.error('Error:', error);
debugger;  // Browser breakpoint

// Test API calls in browser console
fetch('/analyze_text', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: 'test'})
}).then(r => r.json()).then(console.log);
```

## 📦 Package Management

### Adding New Dependencies
```bash
# Install a new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# For development-only packages
pip install package-name
# Add to requirements-dev.txt instead
```

### Managing Dependencies
```bash
# Check for outdated packages
pip list --outdated

# Upgrade specific package
pip install --upgrade package-name

# Upgrade all packages (be careful!)
pip install --upgrade -r requirements.txt
```

## 🌍 Environment Variables

### Create .env file
```bash
# Create environment configuration
cat > .env << EOF
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Application Settings
MAX_CONTENT_LENGTH=16777216  # 16MB
UPLOAD_FOLDER=/tmp/mental_health_analyzer

# Documentation Settings
DOCS_PORT=8000

# ML Model Settings
MODEL_CACHE_SIZE=100
AUDIO_SAMPLE_RATE=22050
EOF
```

### Load Environment Variables
```python
# In app.py, add environment loading
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16777216))
```

## 🔧 Troubleshooting

### Common Issues and Solutions

**Port Already in Use**
```bash
# Find and kill process using port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
python app.py --port 5001
```

**Virtual Environment Issues**
```bash
# Recreate virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**NLTK Data Missing**
```bash
# Re-download NLTK data
python -c "
import nltk
nltk.download('all')
"
```

**Permission Errors**
```bash
# On macOS/Linux, fix permissions
chmod +x run_mental_health_analyzer.sh

# On Windows, run as administrator or check antivirus
```

**Import Errors**
```bash
# Check if you're in the right directory
pwd

# Check if virtual environment is activated
which python

# Reinstall problematic packages
pip uninstall package-name
pip install package-name
```

## 🎯 Development Best Practices

### Code Organization
- **Follow PEP 8**: Python style guidelines
- **Use Type Hints**: Make code more readable
- **Write Docstrings**: Document your functions
- **Separate Concerns**: Keep logic in appropriate modules

### Testing Strategy
- **Write Unit Tests**: Test individual functions
- **Integration Tests**: Test component interactions
- **Manual Testing**: Test UI functionality
- **Error Testing**: Test error handling

### Performance Tips
- **Profile Your Code**: Use `cProfile` for bottlenecks
- **Cache Expensive Operations**: Use `@lru_cache`
- **Optimize Database Queries**: If you add a database
- **Minimize Bundle Size**: For frontend assets

**Development Environment Ready! 🎉**

You now have a complete development setup for learning and extending the Mental Health Analyzer. 

**Next Steps:**
- 📖 Read [Backend Logic](backend-logic) to understand the Python code
- 🎨 Explore [Frontend Logic](frontend-logic) to learn the JavaScript
- 🏗️ Check [System Architecture](architecture) to see how it all fits together
- 🚀 Start building your own features! 