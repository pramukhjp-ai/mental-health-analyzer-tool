import nltk
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
import os

class TextAnalyzer:
    def __init__(self):
        """Initialize text analyzer with sentiment analysis tools"""
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        # Initialize sentiment analyzers
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Define emotion keywords for mood detection
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'fantastic', 'delighted'],
            'sad': ['sad', 'depressed', 'miserable', 'unhappy', 'down', 'blue', 'gloomy', 'melancholy'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'fearful', 'panicked', 'overwhelmed'],
            'angry': ['angry', 'furious', 'mad', 'irritated', 'frustrated', 'annoyed', 'rage', 'livid'],
            'calm': ['calm', 'peaceful', 'relaxed', 'serene', 'tranquil', 'content', 'at ease', 'comfortable'],
            'tired': ['tired', 'exhausted', 'fatigued', 'weary', 'drained', 'sleepy', 'lethargic', 'restless']
        }
    
    def preprocess_text(self, text):
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def analyze_sentiment_vader(self, text):
        """Analyze sentiment using VADER"""
        scores = self.vader_analyzer.polarity_scores(text)
        return {
            'positive': scores['pos'],
            'negative': scores['neg'],
            'neutral': scores['neu'],
            'compound': scores['compound']
        }
    
    def analyze_sentiment_textblob(self, text):
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        return {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def detect_emotions(self, text):
        """Detect emotions based on keyword matching"""
        text_lower = text.lower()
        detected_emotions = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                detected_emotions[emotion] = count
        
        return detected_emotions
    
    def classify_mood(self, sentiment_scores, emotions):
        """Classify overall mood based on sentiment and emotions"""
        # Get compound sentiment score
        compound_score = sentiment_scores.get('compound', 0)
        
        # Determine primary emotion
        primary_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral'
        
        # Mood classification logic
        if compound_score > 0.3:
            if primary_emotion in ['happy', 'calm']:
                return 'Positive'
            else:
                return 'Mixed'
        elif compound_score < -0.3:
            if primary_emotion in ['sad', 'anxious', 'angry']:
                return 'Negative'
            else:
                return 'Mixed'
        else:
            return 'Neutral'
    
    def generate_recommendations(self, mood, emotions):
        """Generate recommendations based on mood and emotions"""
        recommendations = []
        
        if mood == 'Negative':
            if 'anxious' in emotions:
                recommendations.append("Consider deep breathing exercises or meditation")
                recommendations.append("Try to identify specific sources of anxiety")
            if 'sad' in emotions:
                recommendations.append("Connect with friends or family members")
                recommendations.append("Engage in activities you usually enjoy")
            if 'tired' in emotions:
                recommendations.append("Ensure you're getting adequate sleep")
                recommendations.append("Consider your daily routine and energy levels")
        
        elif mood == 'Positive':
            recommendations.append("Great! Continue with activities that bring you joy")
            recommendations.append("Share your positive energy with others")
        
        else:  # Neutral
            recommendations.append("Maintain a balanced routine")
            recommendations.append("Consider trying new activities to boost mood")
        
        return recommendations
    
    def analyze_responses(self, responses):
        """Analyze a list of text responses"""
        if not responses:
            return {
                "error": "No responses provided",
                "overall_mood": "Unknown",
                "confidence": 0.0
            }
        
        all_text = " ".join(responses)
        processed_text = self.preprocess_text(all_text)
        
        # Perform sentiment analysis
        vader_scores = self.analyze_sentiment_vader(processed_text)
        textblob_scores = self.analyze_sentiment_textblob(processed_text)
        
        # Detect emotions
        emotions = self.detect_emotions(processed_text)
        
        # Classify mood
        mood = self.classify_mood(vader_scores, emotions)
        
        # Generate recommendations
        recommendations = self.generate_recommendations(mood, emotions)
        
        # Calculate confidence based on response length and sentiment strength
        confidence = min(0.95, len(processed_text.split()) * 0.01 + abs(vader_scores['compound']) * 0.5)
        
        return {
            "overall_mood": mood,
            "overall_sentiment_score": vader_scores['compound'],
            "sentiment_breakdown": {
                "positive": vader_scores['positive'],
                "negative": vader_scores['negative'],
                "neutral": vader_scores['neutral']
            },
            "subjectivity": textblob_scores['subjectivity'],
            "detected_emotions": emotions,
            "primary_emotion": max(emotions.items(), key=lambda x: x[1])[0] if emotions else 'neutral',
            "recommendations": recommendations,
            "confidence": confidence,
            "response_count": len(responses),
            "total_words": len(processed_text.split())
        } 