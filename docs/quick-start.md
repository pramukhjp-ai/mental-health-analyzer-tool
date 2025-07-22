# 🚀 Quick Start Guide

## Get the Mental Health Analyzer Running in 5 Minutes!

### Prerequisites
- Python 3.8 or higher
- A modern web browser
- Basic command line knowledge

### Step 1: Clone and Setup
```bash
# Navigate to the project directory
cd mental-health-analyzer-tool

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
# Start the main application
python app.py
```

The app will start on `http://127.0.0.1:5000`

### Step 3: Run the Documentation Server (Optional)
```bash
# In a new terminal, start the docs server
python docs_server.py
```

Documentation will be available at `http://127.0.0.1:8000`

### Step 4: Test the Application

1. **Open your browser** and go to `http://127.0.0.1:5000`
2. **Try the Text Analysis**: Type some text like "I feel really happy today!" 
3. **Test Voice Recording**: Click the microphone button and say something
4. **Upload an Image**: Use the facial analysis tab to upload a photo with a face

### What You Can Do

🔍 **Text Analysis**
- Analyzes sentiment, emotions, and mental health indicators in text
- Uses NLTK, TextBlob, and VADER sentiment analysis
- Try positive/negative text to see different results

🎙️ **Voice Analysis** 
- Records audio and analyzes voice patterns
- Extracts MFCC features and voice characteristics
- Detects stress indicators in speech

📸 **Facial Expression Analysis**
- Detects faces in images using OpenCV
- Analyzes facial expressions and emotions
- Provides insights into visual emotional cues

### Common Issues

**Port Already in Use?**
```bash
# Kill any existing Flask processes
pkill -f python
# Or specify a different port
python app.py --port 5001
```

**Missing Dependencies?**
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt
```

**Virtual Environment Issues?**
```bash
# Remove and recreate venv
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Next Steps
- 📖 Read the [Technology Stack](tech-stack) to understand what technologies are used
- 🏗️ Check out [System Architecture](architecture) to see how components work together  
- 💻 Explore [Backend Logic](backend-logic) to understand the Python code
- 🎨 Learn about [Frontend Logic](frontend-logic) for the JavaScript and UI

### Learning Path for Students

1. **Start Here**: Understand the basic Flask application structure
2. **Text Analysis**: Learn NLP concepts and sentiment analysis
3. **Voice Processing**: Explore audio processing with Librosa
4. **Computer Vision**: Understand facial detection with OpenCV
5. **Full Stack**: See how frontend and backend communicate

**Ready to dive deeper?** Use the navigation menu to explore specific topics! 