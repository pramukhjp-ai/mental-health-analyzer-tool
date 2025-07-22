# 📘 Mental Health Analyzer – Rapid Development Spec (Healthcare Domain)

## 🧠 Objective

To develop a **Mental Health Analyzer** that:
- Detects **mood swings**, **emotions**, and **sentiments**.
- Uses **Text**, **Voice Tone**, and **Facial Expression** inputs.
- Fully implemented using **Python full stack** with **local logic and ML**—no paid APIs or LLM keys.

---

## 🧩 Functional Modules (Incremental)

### 1️⃣ Text-Based Analyzer
- **Input Mode**: Text responses to a list of personal + professional questions.
- **Analysis**: NLP-based sentiment/mood classification using pretrained models like `VADER`, `TextBlob`, or custom-trained ML models.
- **Tech Stack**:
  - `Flask` backend API
  - `HTML + JS` frontend form
  - `scikit-learn`, `nltk`, `textblob`

---

### 2️⃣ Voice Tone Analyzer
- **Input Mode**: Short voice note responses to the same question set.
- **Analysis**:
  - Voice feature extraction (pitch, tempo, energy) using `librosa` or `pyAudioAnalysis`.
  - Emotion classification using traditional ML (e.g., SVM, Random Forest).
- **Tech Stack**:
  - `Flask` API to upload and process `.wav` files
  - `librosa`, `numpy`, `scikit-learn`, `matplotlib`

---

### 3️⃣ Facial Expression Analyzer
- **Input Mode**: Record short video responses capturing facial expressions.
- **Analysis**:
  - Frame extraction from video
  - Facial emotion detection using OpenCV + a lightweight CNN or Haarcascade + facial landmarks.
- **Tech Stack**:
  - `OpenCV`, `mediapipe`, `keras`, `cvlib`, `Flask`

---

## 🧪 Technologies & Tools

| Component         | Tech Used                       |
|------------------|----------------------------------|
| Backend          | Flask (Python)                  |
| Frontend         | HTML5, Bootstrap, JS            |
| Text NLP         | NLTK, TextBlob, VADER            |
| Voice Analysis   | Librosa, PyDub, NumPy            |
| Facial Detection | OpenCV, Haarcascade, Keras       |
| ML Classifier    | Scikit-learn                     |
| Docs Server      | Flask Markdown viewer / MkDocs   |

---

## 📋 Sample Questionnaire (to be used across all modes)

> All questions are consistent across text, voice, and facial input modes.

- How was your day today?
- Have you been feeling anxious or overwhelmed lately?
- Can you share something that made you smile recently?
- How are your sleeping patterns lately?
- Do you often feel tired or restless?

(Stored as a `.json` or `.txt` file for reuse.)

---

## 📁 Project Folder Structure

mental-health-analyzer/
│
├── app.py # Flask app entry
├── templates/
│ └── index.html # UI for text, voice, and video inputs
├── static/
│ ├── style.css
│ └── js/
│ └── recorder.js # Audio/Video recording
├── models/
│ ├── sentiment_model.pkl # Optional ML models
│ └── emotion_classifier.pkl
├── analysis/
│ ├── text_analysis.py
│ ├── voice_analysis.py
│ └── facial_analysis.py
├── questions/
│ └── questions.json
├── utils/
│ ├── preprocess.py
│ └── helpers.py
├── README.md
└── requirement.md # ← You're reading this

yaml
Copy
Edit

---

## 🚀 Deployment Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
Run Flask app:

bash
Copy
Edit
python app.py
Access via:

cpp
Copy
Edit
http://127.0.0.1:5000
📄 Documentation
Serve local documentation via browser:

Use Flask-Markdown or MkDocs to serve this requirement.md + other .md files.

Include UI instructions and classifier accuracy details.

⚠️ Limitations (Handled with fallback logic)
No real-time webcam streaming → video upload or local cv2.VideoCapture

No large model training → use simple ML or pretrained classifiers

⏱️ Time Constraint
⚡ Must be fully functional for demo within 30 minutes. Focus on:

Text Analyzer + Voice Analyzer working fully.

Facial detection minimal, just load 1-2 emotions via OpenCV face classifier.

✅ Output Expectation
Web interface with tabbed/section input for:

Text Responses

Voice Recording Upload

Video Facial Expression Upload

Display overall mental state: Calm, Stressed, Happy, Anxious, etc.

