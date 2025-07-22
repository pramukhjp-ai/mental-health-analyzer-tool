import librosa
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class VoiceAnalyzer:
    def __init__(self):
        """Initialize voice analyzer with feature extraction capabilities"""
        self.sample_rate = 22050
        self.emotion_labels = ['calm', 'happy', 'sad', 'angry', 'fearful', 'surprised']
        
    def extract_features(self, audio_path):
        """Extract audio features for emotion analysis"""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=self.sample_rate, duration=30)
            
            # Extract various audio features
            features = {}
            
            # 1. Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            features['spectral_centroid_mean'] = np.mean(spectral_centroids)
            features['spectral_centroid_std'] = np.std(spectral_centroids)
            
            # 2. Spectral rolloff
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
            features['spectral_rolloff_std'] = np.std(spectral_rolloff)
            
            # 3. Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            features['zcr_mean'] = np.mean(zcr)
            features['zcr_std'] = np.std(zcr)
            
            # 4. MFCCs (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            for i in range(13):
                features[f'mfcc_{i}_mean'] = np.mean(mfccs[i])
                features[f'mfcc_{i}_std'] = np.std(mfccs[i])
            
            # 5. Chroma features
            chroma = librosa.feature.chroma_stft(y=y, sr=sr)
            features['chroma_mean'] = np.mean(chroma)
            features['chroma_std'] = np.std(chroma)
            
            # 6. Spectral contrast
            contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            features['spectral_contrast_mean'] = np.mean(contrast)
            features['spectral_contrast_std'] = np.std(contrast)
            
            # 7. Tonnetz
            tonnetz = librosa.feature.tonnetz(y=librosa.effects.harmonic(y), sr=sr)
            features['tonnetz_mean'] = np.mean(tonnetz)
            features['tonnetz_std'] = np.std(tonnetz)
            
            # 8. Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features['tempo'] = tempo
            
            # 9. RMS Energy
            rms = librosa.feature.rms(y=y)[0]
            features['rms_mean'] = np.mean(rms)
            features['rms_std'] = np.std(rms)
            
            return features
            
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None
    
    def classify_emotion_simple(self, features):
        """Simple rule-based emotion classification"""
        if not features:
            return {'emotion': 'neutral', 'confidence': 0.0}
        
        # Simple heuristic classification based on audio features
        emotion_scores = {
            'calm': 0.0,
            'happy': 0.0,
            'sad': 0.0,
            'angry': 0.0,
            'fearful': 0.0,
            'surprised': 0.0
        }
        
        # High energy and tempo suggest happiness or anger
        if features.get('rms_mean', 0) > 0.02 and features.get('tempo', 0) > 120:
            if features.get('spectral_centroid_mean', 0) > 2000:
                emotion_scores['happy'] += 0.4
            else:
                emotion_scores['angry'] += 0.3
        
        # Low energy suggests sadness or calm
        elif features.get('rms_mean', 0) < 0.015:
            if features.get('zcr_mean', 0) < 0.1:
                emotion_scores['sad'] += 0.3
            else:
                emotion_scores['calm'] += 0.4
        
        # High variation in features suggests fear or surprise
        if features.get('spectral_centroid_std', 0) > 500:
            emotion_scores['fearful'] += 0.2
            emotion_scores['surprised'] += 0.2
        
        # Default to calm if no strong indicators
        if max(emotion_scores.values()) < 0.1:
            emotion_scores['calm'] = 0.5
        
        # Get dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        return {
            'emotion': dominant_emotion[0],
            'confidence': min(0.95, dominant_emotion[1] + 0.3),
            'emotion_scores': emotion_scores
        }
    
    def analyze_vocal_characteristics(self, features):
        """Analyze vocal characteristics for additional insights"""
        if not features:
            return {}
        
        characteristics = {}
        
        # Energy level
        rms_mean = features.get('rms_mean', 0)
        if rms_mean > 0.025:
            characteristics['energy_level'] = 'high'
        elif rms_mean > 0.015:
            characteristics['energy_level'] = 'medium'
        else:
            characteristics['energy_level'] = 'low'
        
        # Speaking rate estimation
        zcr_mean = features.get('zcr_mean', 0)
        if zcr_mean > 0.15:
            characteristics['speaking_rate'] = 'fast'
        elif zcr_mean > 0.08:
            characteristics['speaking_rate'] = 'normal'
        else:
            characteristics['speaking_rate'] = 'slow'
        
        # Pitch variation
        spectral_centroid_std = features.get('spectral_centroid_std', 0)
        if spectral_centroid_std > 600:
            characteristics['pitch_variation'] = 'high'
        elif spectral_centroid_std > 300:
            characteristics['pitch_variation'] = 'medium'
        else:
            characteristics['pitch_variation'] = 'low'
        
        return characteristics
    
    def generate_voice_recommendations(self, emotion, characteristics):
        """Generate recommendations based on voice analysis"""
        recommendations = []
        
        if emotion == 'sad':
            recommendations.append("Your voice suggests low mood - consider speaking with someone you trust")
            recommendations.append("Vocal exercises and singing can help improve mood")
        
        elif emotion == 'angry':
            recommendations.append("Your voice indicates stress - try calming breathing exercises")
            recommendations.append("Consider taking breaks to manage emotional intensity")
        
        elif emotion == 'fearful':
            recommendations.append("Your voice suggests anxiety - practice relaxation techniques")
            recommendations.append("Slow, deep breathing can help calm your nervous system")
        
        elif emotion == 'happy':
            recommendations.append("Your voice reflects positive energy - keep it up!")
            recommendations.append("Share your positive mood with others")
        
        # Add recommendations based on characteristics
        if characteristics.get('energy_level') == 'low':
            recommendations.append("Low vocal energy detected - ensure adequate rest")
        
        if characteristics.get('speaking_rate') == 'fast':
            recommendations.append("Fast speaking rate detected - try slowing down for clarity")
        
        return recommendations
    
    def analyze_audio(self, audio_path):
        """Main method to analyze audio file"""
        if not os.path.exists(audio_path):
            return {
                "error": "Audio file not found",
                "emotion": "unknown",
                "confidence": 0.0
            }
        
        try:
            # Extract features
            features = self.extract_features(audio_path)
            
            if not features:
                return {
                    "error": "Could not extract audio features",
                    "emotion": "unknown",
                    "confidence": 0.0
                }
            
            # Classify emotion
            emotion_result = self.classify_emotion_simple(features)
            
            # Analyze vocal characteristics
            characteristics = self.analyze_vocal_characteristics(features)
            
            # Generate recommendations
            recommendations = self.generate_voice_recommendations(
                emotion_result['emotion'], 
                characteristics
            )
            
            # Calculate overall emotion score for combination with other analyses
            emotion_score = 0.0
            if emotion_result['emotion'] in ['happy', 'calm']:
                emotion_score = emotion_result['confidence'] * 0.7
            elif emotion_result['emotion'] in ['sad', 'angry', 'fearful']:
                emotion_score = -emotion_result['confidence'] * 0.7
            
            return {
                "primary_emotion": emotion_result['emotion'],
                "confidence": emotion_result['confidence'],
                "emotion_scores": emotion_result['emotion_scores'],
                "vocal_characteristics": characteristics,
                "recommendations": recommendations,
                "emotion_score": emotion_score,
                "audio_duration": self._get_audio_duration(audio_path),
                "features_extracted": len(features)
            }
            
        except Exception as e:
            return {
                "error": f"Analysis failed: {str(e)}",
                "emotion": "unknown",
                "confidence": 0.0
            }
    
    def _get_audio_duration(self, audio_path):
        """Get audio file duration"""
        try:
            y, sr = librosa.load(audio_path, sr=None)
            return len(y) / sr
        except:
            return 0.0

    def calculate_overall_analysis(self, aggregated_data):
        """Calculate overall analysis from multiple voice recordings"""
        if not aggregated_data['emotions']:
            return aggregated_data
        
        # Calculate dominant emotion
        emotion_counts = {}
        for emotion in aggregated_data['emotions']:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        # Calculate average confidence
        avg_confidence = sum(aggregated_data['confidence_scores']) / len(aggregated_data['confidence_scores'])
        
        # Determine overall mood
        positive_emotions = ['happy', 'calm', 'excited']
        negative_emotions = ['sad', 'angry', 'fearful', 'anxious']
        
        positive_count = sum(1 for emotion in aggregated_data['emotions'] if emotion in positive_emotions)
        negative_count = sum(1 for emotion in aggregated_data['emotions'] if emotion in negative_emotions)
        
        if positive_count > negative_count:
            overall_mood = 'positive'
        elif negative_count > positive_count:
            overall_mood = 'negative'
        else:
            overall_mood = 'neutral'
        
        # Determine stress level based on vocal characteristics
        stress_level = 'low'
        if 'energy_level' in aggregated_data['vocal_characteristics']:
            high_energy_count = aggregated_data['vocal_characteristics']['energy_level'].count('high')
            if high_energy_count > len(aggregated_data['vocal_characteristics']['energy_level']) * 0.6:
                stress_level = 'high'
            elif high_energy_count > len(aggregated_data['vocal_characteristics']['energy_level']) * 0.3:
                stress_level = 'medium'
        
        # Generate comprehensive recommendations
        comprehensive_recommendations = self.generate_comprehensive_recommendations(
            dominant_emotion, overall_mood, stress_level, aggregated_data['vocal_characteristics']
        )
        
        # Remove duplicates from recommendations
        unique_recommendations = list(set(comprehensive_recommendations))
        
        return {
            'dominant_emotion': dominant_emotion,
            'overall_mood': overall_mood,
            'stress_level': stress_level,
            'average_confidence': avg_confidence,
            'emotion_distribution': emotion_counts,
            'comprehensive_recommendations': unique_recommendations,
            'questions_analyzed': len(aggregated_data['emotions']),
            'vocal_characteristics_summary': self.summarize_vocal_characteristics(aggregated_data['vocal_characteristics'])
        }

    def generate_comprehensive_recommendations(self, dominant_emotion, overall_mood, stress_level, vocal_characteristics):
        """Generate comprehensive recommendations based on overall analysis"""
        recommendations = []
        
        # Mood-based recommendations
        if overall_mood == 'negative':
            recommendations.extend([
                "Consider speaking with a mental health professional",
                "Practice daily relaxation techniques",
                "Engage in activities that bring you joy",
                "Maintain regular sleep patterns"
            ])
        elif overall_mood == 'positive':
            recommendations.extend([
                "Your positive energy is great! Keep it up",
                "Share your positive mood with others",
                "Use this energy to tackle challenging tasks"
            ])
        
        # Stress level recommendations
        if stress_level == 'high':
            recommendations.extend([
                "High stress detected - practice deep breathing exercises",
                "Consider taking regular breaks throughout the day",
                "Engage in physical activity to reduce stress",
                "Limit caffeine and ensure adequate sleep"
            ])
        elif stress_level == 'medium':
            recommendations.extend([
                "Moderate stress levels - practice mindfulness",
                "Take short breaks to reset your mind",
                "Consider stress management techniques"
            ])
        
        # Vocal characteristics recommendations
        if 'speaking_rate' in vocal_characteristics:
            fast_speaking = vocal_characteristics['speaking_rate'].count('fast')
            if fast_speaking > len(vocal_characteristics['speaking_rate']) * 0.5:
                recommendations.append("Fast speaking rate detected - try slowing down for better communication")
        
        if 'energy_level' in vocal_characteristics:
            low_energy = vocal_characteristics['energy_level'].count('low')
            if low_energy > len(vocal_characteristics['energy_level']) * 0.5:
                recommendations.append("Low vocal energy - ensure you're getting adequate rest and nutrition")
        
        return recommendations

    def summarize_vocal_characteristics(self, vocal_characteristics):
        """Summarize vocal characteristics across all recordings"""
        summary = {}
        
        for characteristic, values in vocal_characteristics.items():
            if values:
                # Count occurrences of each value
                value_counts = {}
                for value in values:
                    value_counts[value] = value_counts.get(value, 0) + 1
                
                # Get most common value
                most_common = max(value_counts.items(), key=lambda x: x[1])[0]
                summary[characteristic] = {
                    'most_common': most_common,
                    'distribution': value_counts,
                    'consistency': max(value_counts.values()) / len(values)
                }
        
        return summary 