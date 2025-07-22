# 🧠 Mental Health Analyzer

A comprehensive mental health analysis tool that uses text responses, voice tone analysis, and facial expression recognition to assess emotional and mental states locally without any external APIs or data storage.

## 🚀 Features

- **Text Analysis**: Sentiment and mood classification using NLTK, TextBlob, and VADER.
- **Voice Analysis**: Audio feature extraction (MFCCs, spectral features) and emotion classification with Librosa.
- **Facial Analysis**: Facial expression detection via OpenCV Haar Cascades and rule-based classification.
- **Combined Analysis**: Aggregated insights from text, voice, and facial modules into a unified mental health report.
- **Beautiful UI**: Responsive web interface built with Bootstrap 5, real-time feedback, and drag-and-drop support.
- **Offline Processing**: All processing runs locally; no data is stored or transmitted.

## 🧩 Core Modules

### 1️⃣ Text-Based Analyzer
- **Input Mode**: Text responses to mental health questions.
- **Analysis**: NLP-based sentiment/mood classification using VADER, TextBlob, and NLTK.
- **Implementation**: `analysis/text_analysis.py`

### 2️⃣ Voice Tone Analyzer
- **Input Mode**: Short voice recordings answering the same questions.
- **Analysis**: Voice feature extraction (pitch, tempo, energy) and emotion classification.
- **Implementation**: `analysis/voice_analysis.py`

### 3️⃣ Facial Expression Analyzer
- **Input Mode**: Video recordings capturing facial expressions.
- **Analysis**: Frame extraction and facial emotion detection using OpenCV.
- **Implementation**: `analysis/facial_analysis.py`

## 🛠 Tech Stack & Skills

- **Backend**: Python 3.8+, Flask web framework
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Natural Language Processing**: NLTK, TextBlob, VADER
- **Audio Processing**: Librosa, NumPy, SoundFile
- **Computer Vision**: OpenCV, Haar Cascades
- **Machine Learning**: scikit-learn for classifiers
- **Data Visualization**: Matplotlib, Seaborn
- **Utilities**: Python scripting, JSON handling, data preprocessing

## 📁 Project Structure

```
mental-health-analyzer-tool/
├── app.py                         # Main Flask application and API routes
├── run_mental_health_analyzer.sh  # Setup and launch script for macOS/Linux
├── requirements.txt               # Python dependencies
├── test_setup.py                  # Environment and dependency validation tests
├── analysis/                      # Core analysis modules
│   ├── __init__.py                # Package initialization
│   ├── text_analysis.py           # Text sentiment/mood classification logic
│   ├── voice_analysis.py          # Audio feature extraction and emotion classification
│   └── facial_analysis.py         # Facial expression detection and emotion rules
├── questions/                     # Mental health question prompts
│   └── questions.json             # JSON file with question list
├── utils/                         # Helper utilities
│   ├── __init__.py                # Package initialization
│   └── preprocess.py              # Text preprocessing and cleanup functions
├── static/                        # Frontend assets
│   ├── css/
│   │   └── style.css              # Custom styles for the web interface
│   └── js/
│       ├── app.js                 # Frontend logic and API interactions
│       ├── recorder.js            # Generic audio/video recording utilities
│       └── voiceRecorder.js       # Voice-specific recording functions
├── templates/                     # HTML templates
│   └── index.html                 # Main UI with tabs for each analysis mode
└── models/                        # Directory for ML models (optional)
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip
- A modern web browser with microphone and camera access

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mental-health-analyzer-tool
   ```
2. **Run the setup script**:
   ```bash
   chmod +x run_mental_health_analyzer.sh
   ./run_mental_health_analyzer.sh
   ```
3. **Open the application** by navigating to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Manual Setup

1. (Optional) **Create and activate** a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Download NLTK data**:
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```
4. **Launch the Flask app**:
   ```bash
   python app.py
   ```
5. **Visit** [http://127.0.0.1:5000](http://127.0.0.1:5000).

## 📖 Usage

### Text Analysis
1. Select the **Text Analysis** tab.
2. Answer the five mental health questions:
   - How was your day today?
   - Have you been feeling anxious or overwhelmed lately?
   - Can you share something that made you smile recently?
   - How are your sleeping patterns lately?
   - Do you often feel tired or restless?
3. Click **Analyze Text Responses** to view sentiment, polarity, and mood classification.

### Voice Analysis
1. Go to the **Voice Analysis** tab.
2. Record your voice or upload an audio file (MP3, WAV, M4A).
3. Click **Analyze Voice** to extract audio features and classify emotions.

### Facial Analysis
1. Navigate to the **Facial Analysis** tab.
2. Upload a short video (MP4, AVI, MOV, WEBM).
3. Click **Analyze Facial Expression** to detect emotions from facial landmarks.

### Combined Analysis
1. Complete at least one individual analysis.
2. Switch to the **Combined Analysis** tab.
3. Click **Generate Combined Analysis** to receive a unified mental health report.

## 🔒 Privacy & Security

- All processing is **local**; no personal data is stored or transmitted.
- Uploaded files are processed **in-memory** and immediately deleted.
- No external APIs or third-party services are used.

## 🚨 Troubleshooting

- **Microphone Issues**: Check browser permissions and hardware connectivity.
- **Video Upload Errors**: Ensure file size is under 16MB and the format is supported.
- **Slow Analysis**: Use smaller files or restart the application.
- **Dependency Errors**: Upgrade pip or recreate the virtual environment.

## ⚠️ Limitations

- No real-time webcam streaming → video upload or local capture
- Limited model training → uses simple ML or pretrained classifiers
- Maximum file size: 16MB (configurable in app.py)

## 🤝 Contributing

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes and open a pull request.
4. Ensure all tests in `test_setup.py` pass before merging.

## 📄 License & Disclaimer

This tool is for **educational and demonstration** purposes only. It is **not** a medical device and should not substitute professional mental health advice or diagnosis.

---

*Built with Python, Flask, Bootstrap, NLTK, TextBlob, VADER, Librosa, OpenCV, and scikit-learn.* 