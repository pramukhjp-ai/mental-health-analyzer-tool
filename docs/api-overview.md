# 🔌 API Overview

## Mental Health Analyzer REST API

The Mental Health Analyzer provides a RESTful API built with Flask that handles all analysis operations. This guide explains each endpoint and how to use them.

## Base URL
```
http://127.0.0.1:5000
```

## API Endpoints

### 📝 Text Analysis
**POST** `/analyze_text`

Analyzes text input for sentiment, emotions, and mental health indicators.

**Request Body:**
```json
{
  "text": "I feel really happy and excited about today!"
}
```

**Response:**
```json
{
  "sentiment": {
    "polarity": 0.8,
    "subjectivity": 0.9,
    "classification": "positive"
  },
  "vader_sentiment": {
    "compound": 0.7717,
    "positive": 0.4,
    "neutral": 0.6,
    "negative": 0.0
  },
  "word_count": 8,
  "mental_health_score": 75
}
```

### 🎙️ Voice Analysis
**POST** `/analyze_voice`

Analyzes audio recordings for voice patterns and emotional indicators.

**Request:**
- Content-Type: `multipart/form-data`
- File field: `voice_file` (audio file)

**Response:**
```json
{
  "mfcc_features": [1.2, 3.4, -0.8, ...],
  "pitch_mean": 180.5,
  "energy_mean": 0.65,
  "voice_quality": "stable",
  "emotional_indicators": {
    "stress_level": "low",
    "confidence": 0.72
  }
}
```

### 📸 Facial Analysis
**POST** `/analyze_facial`

Analyzes facial expressions in uploaded images.

**Request:**
- Content-Type: `multipart/form-data`
- File field: `image_file` (image file)

**Response:**
```json
{
  "faces_detected": 1,
  "face_coordinates": [[x, y, width, height]],
  "facial_features": {
    "expression": "happy",
    "confidence": 0.85
  },
  "emotional_state": "positive"
}
```

### 🔗 Combined Analysis
**POST** `/combined_analysis`

Combines results from multiple analysis types for comprehensive insights.

**Request Body:**
```json
{
  "text_results": {...},
  "voice_results": {...},
  "facial_results": {...}
}
```

**Response:**
```json
{
  "overall_mental_health_score": 78,
  "dominant_emotion": "happiness",
  "consistency_across_modalities": 0.82,
  "recommendations": [
    "Continue positive mental practices",
    "Consider stress management techniques"
  ],
  "detailed_breakdown": {
    "text_weight": 0.4,
    "voice_weight": 0.3,
    "facial_weight": 0.3
  }
}
```

### 📋 Get Questions
**GET** `/get_questions`

Retrieves the mental health questionnaire for text analysis.

**Response:**
```json
{
  "questions": [
    {
      "id": 1,
      "question": "How are you feeling today?",
      "type": "open_text"
    },
    {
      "id": 2,
      "question": "Rate your stress level (1-10)",
      "type": "scale"
    }
  ]
}
```

## How the API Works

### 🏗️ Request Flow
1. **Frontend** sends user data to Flask endpoint
2. **Flask route** receives and validates the request
3. **Analysis module** processes the data using ML libraries
4. **Results** are formatted and returned as JSON
5. **Frontend** displays the results to the user

### 🔍 Behind the Scenes

**Text Analysis Process:**
```python
@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')
    
    # Use TextAnalyzer class
    analyzer = TextAnalyzer()
    results = analyzer.analyze(text)
    
    return jsonify(results)
```

**Error Handling:**
```python
try:
    # Analysis logic
    results = analyzer.analyze(data)
    return jsonify(results)
except Exception as e:
    return jsonify({
        'error': str(e),
        'status': 'failed'
    }), 500
```

## Authentication & Security

### 🔒 Security Features
- **No external data transmission**: All processing happens locally
- **Temporary file handling**: Files are deleted after processing
- **Input validation**: All inputs are sanitized and validated
- **File size limits**: Maximum 16MB per upload
- **CORS enabled**: For frontend-backend communication

### 📁 File Upload Security
- **Allowed extensions**: `.wav`, `.mp3`, `.jpg`, `.png`, `.jpeg`
- **File type validation**: Content-type checking
- **Temporary storage**: Files stored in `/tmp` and auto-deleted
- **Memory limits**: Processing limited to prevent memory overflow

## Testing the API

### 🧪 Using curl
```bash
# Test text analysis
curl -X POST http://127.0.0.1:5000/analyze_text \
  -H "Content-Type: application/json" \
  -d '{"text": "I feel great today!"}'

# Test voice upload
curl -X POST http://127.0.0.1:5000/analyze_voice \
  -F "voice_file=@test_audio.wav"

# Test facial analysis
curl -X POST http://127.0.0.1:5000/analyze_facial \
  -F "image_file=@test_image.jpg"
```

### 🔍 Using Python Requests
```python
import requests

# Text analysis
response = requests.post('http://127.0.0.1:5000/analyze_text', 
                        json={'text': 'I feel amazing!'})
print(response.json())

# File upload
with open('audio.wav', 'rb') as f:
    response = requests.post('http://127.0.0.1:5000/analyze_voice',
                           files={'voice_file': f})
print(response.json())
```

## Error Codes

| Code | Meaning | Common Causes |
|------|---------|---------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Missing required fields, invalid JSON |
| 413 | File Too Large | Upload exceeds 16MB limit |
| 415 | Unsupported Media Type | Invalid file format |
| 500 | Internal Server Error | Processing error, missing dependencies |

## Rate Limiting

Currently no rate limiting is implemented, but for production use consider:
- Request per minute limits
- File upload size restrictions  
- Memory usage monitoring

**Next Steps:**
- 📖 Learn about [Data Models](data-models) for detailed response schemas
- 🎯 Check [API Endpoints](api-endpoints) for complete parameter lists
- 💻 See [Backend Logic](backend-logic) to understand the implementation 