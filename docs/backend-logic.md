# 🧠 Backend Logic Explained

## Understanding the Python Backend

The Mental Health Analyzer backend is built with Flask and follows a modular architecture. Let's break down how each component works!

## 📁 Project Structure

```
mental-health-analyzer-tool/
├── app.py                 # Main Flask application
├── analysis/              # Analysis modules
│   ├── text_analysis.py   # Text sentiment analysis
│   ├── voice_analysis.py  # Audio processing
│   └── facial_analysis.py # Computer vision
├── utils/                 # Utility functions
│   └── preprocess.py      # Data preprocessing
├── questions/             # Question templates
│   └── questions.json     # Mental health questions
└── requirements.txt       # Dependencies
```

## 🌐 Main Flask Application (app.py)

### Flask App Setup
```python
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Configure file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
```

**Key Concepts:**
- **Flask**: Lightweight web framework for Python
- **CORS**: Allows frontend to communicate with backend
- **File Upload Limits**: Prevents memory overflow from large files

### Route Handlers

**Text Analysis Route:**
```python
@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    try:
        # Get JSON data from request
        data = request.get_json()
        text = data.get('text', '')
        
        # Input validation
        if not text.strip():
            return jsonify({'error': 'Text is required'}), 400
        
        # Create analyzer instance
        from analysis.text_analysis import TextAnalyzer
        analyzer = TextAnalyzer()
        
        # Perform analysis
        results = analyzer.analyze(text)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

**Key Patterns:**
- **Error Handling**: Try/catch blocks for robust error handling
- **Input Validation**: Check for required fields and data types
- **Modular Design**: Import specific analyzer classes
- **JSON Responses**: Return structured data as JSON

## 📝 Text Analysis Module

### TextAnalyzer Class Structure
```python
class TextAnalyzer:
    def __init__(self):
        """Initialize NLP tools and models"""
        self.sentiment_analyzer = SentimentIntensityAnalyzer()  # VADER
        self.stop_words = set(stopwords.words('english'))
        
    def analyze(self, text):
        """Main analysis method"""
        results = {
            'basic_sentiment': self._get_basic_sentiment(text),
            'vader_sentiment': self._get_vader_sentiment(text),
            'text_statistics': self._get_text_stats(text),
            'mental_health_indicators': self._analyze_mental_health(text)
        }
        return results
```

### Sentiment Analysis Methods

**VADER Sentiment (Social Media Optimized):**
```python
def _get_vader_sentiment(self, text):
    """VADER is great for social media text and informal language"""
    scores = self.sentiment_analyzer.polarity_scores(text)
    return {
        'compound': scores['compound'],    # Overall sentiment (-1 to 1)
        'positive': scores['pos'],        # Positive intensity
        'neutral': scores['neu'],         # Neutral intensity  
        'negative': scores['neg']         # Negative intensity
    }
```

**TextBlob Sentiment (General Purpose):**
```python
def _get_basic_sentiment(self, text):
    """TextBlob for general sentiment analysis"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity      # -1 (negative) to 1 (positive)
    subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
    
    # Classify sentiment
    if polarity > 0.1:
        classification = 'positive'
    elif polarity < -0.1:
        classification = 'negative'
    else:
        classification = 'neutral'
        
    return {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'classification': classification
    }
```

### Mental Health Specific Analysis
```python
def _analyze_mental_health(self, text):
    """Analyze text for mental health indicators"""
    
    # Define keyword categories
    positive_keywords = ['happy', 'joy', 'excited', 'grateful', 'confident']
    negative_keywords = ['sad', 'depressed', 'anxious', 'worried', 'stressed']
    
    # Convert to lowercase and tokenize
    words = word_tokenize(text.lower())
    words = [w for w in words if w not in self.stop_words]
    
    # Count keyword occurrences
    positive_count = sum(1 for word in words if word in positive_keywords)
    negative_count = sum(1 for word in words if word in negative_keywords)
    
    # Calculate mental health score
    total_keywords = positive_count + negative_count
    if total_keywords > 0:
        mental_health_score = (positive_count / total_keywords) * 100
    else:
        mental_health_score = 50  # Neutral baseline
    
    return {
        'mental_health_score': mental_health_score,
        'positive_indicators': positive_count,
        'negative_indicators': negative_count,
        'keyword_analysis': {
            'positive_words_found': [w for w in words if w in positive_keywords],
            'negative_words_found': [w for w in words if w in negative_keywords]
        }
    }
```

## 🎙️ Voice Analysis Module

### Audio Processing Pipeline
```python
class VoiceAnalyzer:
    def __init__(self):
        """Initialize audio processing parameters"""
        self.sample_rate = 22050
        self.n_mfcc = 13  # Number of MFCC coefficients
        
    def analyze(self, audio_file_path):
        """Main voice analysis pipeline"""
        
        # Step 1: Load audio file
        y, sr = librosa.load(audio_file_path, sr=self.sample_rate)
        
        # Step 2: Extract features
        features = self._extract_audio_features(y, sr)
        
        # Step 3: Analyze emotional indicators
        emotional_indicators = self._analyze_voice_emotion(features)
        
        return {
            'audio_features': features,
            'emotional_analysis': emotional_indicators,
            'voice_quality_metrics': self._get_voice_quality(y, sr)
        }
```

### MFCC Feature Extraction
```python
def _extract_audio_features(self, y, sr):
    """Extract Mel-Frequency Cepstral Coefficients"""
    
    # MFCC features (captures voice timbre)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
    mfcc_means = np.mean(mfccs, axis=1)  # Average across time
    
    # Pitch/fundamental frequency
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_mean = np.mean(pitches[pitches > 0]) if len(pitches[pitches > 0]) > 0 else 0
    
    # Energy/RMS
    rms = librosa.feature.rms(y=y)[0]
    energy_mean = np.mean(rms)
    
    return {
        'mfcc_features': mfcc_means.tolist(),
        'pitch_mean': float(pitch_mean),
        'energy_mean': float(energy_mean),
        'audio_length': len(y) / sr
    }
```

## 📸 Facial Analysis Module

### Face Detection with OpenCV
```python
class FacialAnalyzer:
    def __init__(self):
        """Initialize face detection cascade"""
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
    def analyze(self, image_path):
        """Analyze facial expressions in image"""
        
        # Load and preprocess image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,    # Image pyramid scaling
            minNeighbors=5,     # Minimum neighbor rectangles
            minSize=(30, 30)    # Minimum face size
        )
        
        results = {
            'faces_detected': len(faces),
            'face_coordinates': faces.tolist(),
            'facial_analysis': []
        }
        
        # Analyze each detected face
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]  # Region of Interest
            face_analysis = self._analyze_facial_expression(face_roi)
            results['facial_analysis'].append(face_analysis)
            
        return results
```

## 🔧 Utility Functions

### Data Preprocessing
```python
def preprocess_text(text):
    """Clean and prepare text for analysis"""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove special characters (keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    # Handle common contractions
    contractions = {
        "don't": "do not",
        "won't": "will not",
        "can't": "cannot"
    }
    
    for contraction, expansion in contractions.items():
        text = text.replace(contraction, expansion)
    
    return text
```

### File Handling
```python
def save_temp_file(uploaded_file):
    """Safely save uploaded file to temporary location"""
    
    # Create temp directory if it doesn't exist
    temp_dir = '/tmp/mental_health_analyzer'
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate unique filename
    filename = f"{uuid.uuid4()}_{uploaded_file.filename}"
    file_path = os.path.join(temp_dir, filename)
    
    # Save file
    uploaded_file.save(file_path)
    
    return file_path

def cleanup_temp_file(file_path):
    """Remove temporary file after processing"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Could not delete temp file {file_path}: {e}")
```

## 🎯 Key Programming Concepts Used

### Object-Oriented Programming
- **Classes**: `TextAnalyzer`, `VoiceAnalyzer`, `FacialAnalyzer`
- **Encapsulation**: Private methods with `_` prefix
- **Inheritance**: All analyzers could inherit from base `Analyzer` class

### Error Handling Patterns
```python
try:
    result = risky_operation()
    return success_response(result)
except SpecificException as e:
    logger.error(f"Specific error: {e}")
    return error_response("User-friendly message", 400)
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return error_response("Something went wrong", 500)
```

### Functional Programming
- **List Comprehensions**: `[w for w in words if w not in stop_words]`
- **Map/Filter Operations**: Processing collections efficiently
- **Pure Functions**: Functions that don't modify global state

### File I/O and Resource Management
```python
# Context managers for safe file handling
with open('file.txt', 'r') as f:
    content = f.read()

# Automatic cleanup with try/finally
try:
    file_path = save_temp_file(upload)
    results = process_file(file_path)
finally:
    cleanup_temp_file(file_path)
```

## 🔍 Testing and Debugging

### Unit Testing Example
```python
import unittest
from analysis.text_analysis import TextAnalyzer

class TestTextAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TextAnalyzer()
    
    def test_positive_sentiment(self):
        result = self.analyzer.analyze("I feel amazing and happy!")
        self.assertGreater(result['basic_sentiment']['polarity'], 0)
        self.assertEqual(result['basic_sentiment']['classification'], 'positive')
```

### Debug Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def analyze_text(text):
    logger.debug(f"Analyzing text: {text[:50]}...")
    # Analysis logic
    logger.info(f"Analysis completed, sentiment: {sentiment}")
```

**Understanding this backend helps you:**
- 🐍 Learn Python web development with Flask
- 🤖 Understand machine learning integration
- 📊 See how to process different data types (text, audio, images)
- 🔧 Learn about error handling and validation
- 📁 Understand file upload and processing
- 🧪 Learn testing and debugging techniques

**Next Steps:**
- 🎨 Check out [Frontend Logic](frontend-logic) to see how UI connects to backend
- 🔌 Review [API Endpoints](api-endpoints) for complete endpoint documentation
- 🧪 Try [Testing Guide](testing-guide) to learn testing practices 