from flask import Flask, render_template, request, jsonify
import os
import json
from analysis.text_analysis import TextAnalyzer
from analysis.voice_analysis import VoiceAnalyzer
from analysis.facial_analysis import FacialAnalyzer
import base64
import tempfile
from collections import Counter

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize analyzers
text_analyzer = TextAnalyzer()
voice_analyzer = VoiceAnalyzer()
facial_analyzer = FacialAnalyzer()

@app.route('/')
def index():
    """Main page with tabbed interface for different input modes"""
    return render_template('index.html')

@app.route('/get_questions')
def get_questions():
    """API endpoint to get questions for all input modes"""
    try:
        with open('questions/questions.json', 'r') as f:
            questions = json.load(f)
        return jsonify(questions)
    except FileNotFoundError:
        # Fallback questions if file doesn't exist
        default_questions = [
            "How was your day today?",
            "Have you been feeling anxious or overwhelmed lately?",
            "Can you share something that made you smile recently?",
            "How are your sleeping patterns lately?",
            "Do you often feel tired or restless?"
        ]
        return jsonify({"questions": default_questions})

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    """Analyze text responses for sentiment and mood"""
    try:
        data = request.get_json()
        responses = data.get('responses', [])
        
        if not responses:
            return jsonify({"error": "No text responses provided"}), 400
        
        # Analyze text responses
        analysis_result = text_analyzer.analyze_responses(responses)
        
        return jsonify({
            "success": True,
            "analysis": analysis_result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze_voice', methods=['POST'])
def analyze_voice():
    """Analyze multiple voice recordings for comprehensive emotional analysis"""
    try:
        # Get all audio files from the request
        audio_files = {}
        for key in request.files:
            if key.startswith('audio_'):
                question_index = key.replace('audio_', '')
                audio_files[question_index] = request.files[key]
        
        if not audio_files:
            return jsonify({"error": "No audio files provided"}), 400
        
        # Analyze each question's voice recording
        question_analyses = {}
        overall_analysis = {
            'emotions': [],
            'confidence_scores': [],
            'vocal_characteristics': {},
            'recommendations': [],
            'overall_mood': 'neutral',
            'stress_level': 'low'
        }
        
        temp_files = []
        
        try:
            for question_index, audio_file in audio_files.items():
                # Save temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    audio_file.save(tmp_file.name)
                    temp_files.append(tmp_file.name)
                
                # Analyze this question's voice
                try:
                    analysis_result = voice_analyzer.analyze_audio(tmp_file.name)
                    question_analyses[question_index] = analysis_result
                except Exception as e:
                    print(f"Error analyzing voice for question {question_index}: {e}")
                    # Provide fallback analysis result
                    question_analyses[question_index] = {
                        'primary_emotion': 'neutral',
                        'confidence': 0.5,
                        'vocal_characteristics': {'energy_level': 'medium'},
                        'recommendations': ['Unable to analyze this recording']
                    }
                
                # Aggregate data for overall analysis
                if analysis_result and 'primary_emotion' in analysis_result:
                    overall_analysis['emotions'].append(analysis_result['primary_emotion'])
                if analysis_result and 'confidence' in analysis_result:
                    overall_analysis['confidence_scores'].append(analysis_result['confidence'])
                if analysis_result and 'vocal_characteristics' in analysis_result:
                    # Merge vocal characteristics
                    for key, value in analysis_result['vocal_characteristics'].items():
                        if key not in overall_analysis['vocal_characteristics']:
                            overall_analysis['vocal_characteristics'][key] = []
                        overall_analysis['vocal_characteristics'][key].append(value)
                if analysis_result and 'recommendations' in analysis_result:
                    overall_analysis['recommendations'].extend(analysis_result['recommendations'])
            
            # Calculate overall mood and stress level
            if not overall_analysis['emotions']:
                # Fallback if no emotions detected
                overall_analysis['emotions'] = ['neutral']
                overall_analysis['confidence_scores'] = [0.5]
                overall_analysis['vocal_characteristics'] = {'energy_level': ['medium']}
                overall_analysis['recommendations'] = ['Unable to analyze voice patterns']
            
            overall_analysis = voice_analyzer.calculate_overall_analysis(overall_analysis)
            
            return jsonify({
                "success": True,
                "question_analyses": question_analyses,
                "overall_analysis": overall_analysis
            })
            
        finally:
            # Clean up temporary files
            for tmp_path in temp_files:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze_facial', methods=['POST'])
def analyze_facial():
    """Analyze facial expressions from video/image"""
    try:
        # Get all video files from the request
        video_files = {}
        for key in request.files:
            if key.startswith('video_'):
                question_index = key.replace('video_', '')
                video_files[question_index] = request.files[key]
        
        if not video_files:
            return jsonify({"error": "No video files provided"}), 400
        
        # Analyze each question's video
        question_analyses = {}
        overall_analysis = {
            'emotions': [],
            'confidence_scores': [],
            'emotion_scores': [],  # Add this
            'facial_features': {},
            'recommendations': [],
            'overall_emotion': 'neutral',
            'stress_level': 'low'
        }
        
        temp_files = []
        
        try:
            for question_index, video_file in video_files.items():
                # Save temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp_file:
                    video_file.save(tmp_file.name)
                    temp_files.append(tmp_file.name)
                
                # Analyze this question's video
                analysis_result = facial_analyzer.analyze_video(tmp_file.name)
                question_analyses[question_index] = analysis_result
                
                # Aggregate data
                if 'primary_emotion' in analysis_result:
                    overall_analysis['emotions'].append(analysis_result['primary_emotion'])
                if 'confidence' in analysis_result:
                    overall_analysis['confidence_scores'].append(analysis_result['confidence'])
                if 'features_summary' in analysis_result:
                    # Simple merge, you can improve this
                    overall_analysis['facial_features'][question_index] = analysis_result['features_summary']
                if 'recommendations' in analysis_result:
                    overall_analysis['recommendations'].extend(analysis_result['recommendations'])
                if 'emotion_score' in analysis_result:
                    overall_analysis['emotion_scores'].append(analysis_result['emotion_score'])
            
            # Calculate overall emotion
            if overall_analysis['emotions']:
                counter = Counter(overall_analysis['emotions'])
                overall_analysis['overall_emotion'] = counter.most_common(1)[0][0]
            
            # Calculate average confidence
            if overall_analysis['confidence_scores']:
                overall_analysis['average_confidence'] = sum(overall_analysis['confidence_scores']) / len(overall_analysis['confidence_scores'])
            
            if overall_analysis['emotion_scores']:
                overall_analysis['emotion_score'] = sum(overall_analysis['emotion_scores']) / len(overall_analysis['emotion_scores'])
            else:
                overall_analysis['emotion_score'] = 0.0
            
            return jsonify({
                "success": True,
                "question_analyses": question_analyses,
                "overall_analysis": overall_analysis
            })
        finally:
            for tmp in temp_files:
                if os.path.exists(tmp):
                    os.unlink(tmp)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/combined_analysis', methods=['POST'])
def combined_analysis():
    """Perform combined analysis from all three input modes"""
    try:
        data = request.get_json()
        
        # Get individual analysis results
        text_result = None
        voice_result = None
        facial_result = None
        
        if data.get('text_responses'):
            text_result = text_analyzer.analyze_responses(data['text_responses'])
        
        if data.get('voice_analysis'):
            voice_result = data['voice_analysis']
        
        if data.get('facial_analysis'):
            facial_result = data['facial_analysis']
        
        # Combine results for overall mental state assessment
        combined_result = {
            "overall_mood": "Neutral",
            "confidence": 0.0,
            "recommendations": [],
            "individual_analyses": {
                "text": text_result,
                "voice": voice_result,
                "facial": facial_result
            }
        }
        
        # Simple combination logic
        mood_scores = []
        if text_result:
            mood_scores.append(text_result.get('overall_sentiment_score', 0))
        if voice_result:
            mood_scores.append(voice_result.get('emotion_score', 0))
        if facial_result:
            # Update to use new structure
            mood_scores.append(facial_result.get('overall_analysis', {}).get('emotion_score', 0))
        
        if mood_scores:
            avg_score = sum(mood_scores) / len(mood_scores)
            if avg_score > 0.3:
                combined_result["overall_mood"] = "Positive"
            elif avg_score < -0.3:
                combined_result["overall_mood"] = "Negative"
            else:
                combined_result["overall_mood"] = "Neutral"
            
            combined_result["confidence"] = min(0.95, len(mood_scores) * 0.3)
        
        # Generate combined recommendations
        all_recommendations = []
        if text_result and 'recommendations' in text_result:
            all_recommendations.extend(text_result['recommendations'])
        if voice_result and 'recommendations' in voice_result:
            all_recommendations.extend(voice_result['recommendations'])
        if facial_result and 'overall_analysis' in facial_result and 'recommendations' in facial_result['overall_analysis']:
            all_recommendations.extend(facial_result['overall_analysis']['recommendations'])
        
        # Remove duplicates and add general recommendations
        combined_result["recommendations"] = list(set(all_recommendations))
        if not combined_result["recommendations"]:
            combined_result["recommendations"] = [
                "Continue monitoring your mental health regularly",
                "Consider speaking with a mental health professional if needed"
            ]
        
        return jsonify({
            "success": True,
            "analysis": combined_result
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('analysis', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('questions', exist_ok=True)
    os.makedirs('utils', exist_ok=True)
    
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print(f"🧠 Mental Health Analyzer starting on http://127.0.0.1:{port}")
    print("🔥 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='127.0.0.1', port=port, ssl_context=None) 