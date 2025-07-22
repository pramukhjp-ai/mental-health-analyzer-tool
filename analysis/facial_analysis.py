import cv2
import numpy as np
import os
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class FacialAnalyzer:
    def __init__(self):
        """Initialize facial analyzer with OpenCV cascade classifiers"""
        # Load pre-trained face detection classifier
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        except Exception as e:
            print(f"Warning: Could not load OpenCV classifiers: {e}")
            self.face_cascade = None
            self.eye_cascade = None
        
        # Simple emotion mapping based on facial features
        self.emotion_mapping = {
            'neutral': 0.0,
            'happy': 0.7,
            'sad': -0.6,
            'angry': -0.8,
            'surprised': 0.3,
            'fearful': -0.7,
            'disgusted': -0.5
        }
    
    def detect_faces(self, frame):
        """Detect faces in a frame"""
        if self.face_cascade is None:
            return []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces
    
    def extract_facial_features(self, frame, face_coords):
        """Extract basic facial features for emotion analysis"""
        x, y, w, h = face_coords
        face_roi = frame[y:y+h, x:x+w]
        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
        features = {}
        
        # 1. Face dimensions
        features['face_width'] = w
        features['face_height'] = h
        features['face_ratio'] = w / h if h > 0 else 1.0
        
        # 2. Eye detection
        if self.eye_cascade is not None:
            eyes = self.eye_cascade.detectMultiScale(gray_face)
            features['eye_count'] = len(eyes)
            if len(eyes) >= 2:
                # Calculate eye distance and position
                eye_positions = [(eye[0] + eye[2]//2, eye[1] + eye[3]//2) for eye in eyes[:2]]
                if len(eye_positions) == 2:
                    eye_distance = np.sqrt((eye_positions[0][0] - eye_positions[1][0])**2 + 
                                         (eye_positions[0][1] - eye_positions[1][1])**2)
                    features['eye_distance'] = eye_distance
                    features['eye_symmetry'] = abs(eye_positions[0][1] - eye_positions[1][1])
        
        # 3. Brightness and contrast analysis
        features['mean_brightness'] = np.mean(gray_face)
        features['brightness_std'] = np.std(gray_face)
        
        # 4. Face position in frame
        frame_height, frame_width = frame.shape[:2]
        features['face_center_x'] = (x + w/2) / frame_width
        features['face_center_y'] = (y + h/2) / frame_height
        
        return features
    
    def analyze_emotion_simple(self, features_list):
        """Simple rule-based emotion analysis from facial features"""
        if not features_list:
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'emotion_scores': {'neutral': 1.0}
            }
        
        # Aggregate features across all frames
        avg_features = {}
        for key in features_list[0].keys():
            values = [f.get(key, 0) for f in features_list if key in f]
            if values:
                avg_features[key] = np.mean(values)
        
        emotion_scores = {
            'neutral': 0.4,  # Default baseline
            'happy': 0.0,
            'sad': 0.0,
            'angry': 0.0,
            'surprised': 0.0,
            'fearful': 0.0
        }
        
        # Simple heuristics based on facial features
        brightness = avg_features.get('mean_brightness', 128)
        brightness_variation = avg_features.get('brightness_std', 0)
        eye_count = avg_features.get('eye_count', 0)
        eye_symmetry = avg_features.get('eye_symmetry', 0)
        
        # Brightness-based emotion indicators
        if brightness > 140:  # Brighter faces might indicate happiness
            emotion_scores['happy'] += 0.3
        elif brightness < 100:  # Darker faces might indicate sadness
            emotion_scores['sad'] += 0.2
        
        # Eye-based indicators
        if eye_count >= 2:
            emotion_scores['happy'] += 0.2  # Both eyes visible suggests engagement
            if eye_symmetry < 5:  # Symmetric eyes
                emotion_scores['happy'] += 0.1
                emotion_scores['neutral'] += 0.1
        elif eye_count == 0:
            emotion_scores['sad'] += 0.2  # No eyes detected might indicate looking down
        
        # Brightness variation might indicate expression changes
        if brightness_variation > 50:
            emotion_scores['surprised'] += 0.2
            emotion_scores['fearful'] += 0.1
        
        # Face size might indicate distance/engagement
        face_size = avg_features.get('face_width', 0) * avg_features.get('face_height', 0)
        if face_size > 10000:  # Large face = close to camera = engaged
            emotion_scores['happy'] += 0.1
        elif face_size < 3000:  # Small face = distant = withdrawn
            emotion_scores['sad'] += 0.1
        
        # Get dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        return {
            'emotion': dominant_emotion[0],
            'confidence': min(0.85, dominant_emotion[1] + 0.2),
            'emotion_scores': emotion_scores
        }
    
    def generate_facial_recommendations(self, emotion, features_summary):
        """Generate recommendations based on facial analysis"""
        recommendations = []
        
        if emotion == 'sad':
            recommendations.append("Facial analysis suggests low mood - consider engaging in uplifting activities")
            recommendations.append("Try smiling exercises or watch something that makes you laugh")
        
        elif emotion == 'angry':
            recommendations.append("Facial tension detected - try facial relaxation exercises")
            recommendations.append("Take deep breaths and try to relax your facial muscles")
        
        elif emotion == 'fearful':
            recommendations.append("Signs of anxiety in facial expression - practice calming techniques")
            recommendations.append("Try progressive muscle relaxation starting with your face")
        
        elif emotion == 'happy':
            recommendations.append("Great! Your facial expression shows positive emotions")
            recommendations.append("Continue with activities that bring you joy")
        
        elif emotion == 'surprised':
            recommendations.append("Your expression shows alertness - this can be positive energy")
        
        # Additional recommendations based on features
        if features_summary.get('average_eye_count', 0) < 1:
            recommendations.append("Limited eye visibility - ensure good lighting and face the camera")
        
        return recommendations
    
    def analyze_video(self, video_path):
        """Main method to analyze video file for facial emotions"""
        if not os.path.exists(video_path):
            return {
                "error": "Video file not found",
                "emotion": "unknown",
                "confidence": 0.0
            }
        
        try:
            # Open video file
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                return {
                    "error": "Could not open video file",
                    "emotion": "unknown",
                    "confidence": 0.0
                }
            
            frames_analyzed = 0
            features_list = []
            face_detection_count = 0
            
            # Process video frames
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frames_analyzed += 1
                
                # Skip frames for faster processing (analyze every 10th frame)
                if frames_analyzed % 10 != 0:
                    continue
                
                # Detect faces
                faces = self.detect_faces(frame)
                
                if len(faces) > 0:
                    face_detection_count += 1
                    # Use the largest face detected
                    largest_face = max(faces, key=lambda face: face[2] * face[3])
                    
                    # Extract features
                    features = self.extract_facial_features(frame, largest_face)
                    features_list.append(features)
                
                # Limit analysis to first 100 processed frames for speed
                if frames_analyzed >= 1000:
                    break
            
            cap.release()
            
            if not features_list:
                return {
                    "error": "No faces detected in video",
                    "emotion": "unknown",
                    "confidence": 0.0,
                    "frames_analyzed": frames_analyzed,
                    "faces_detected": 0
                }
            
            # Analyze emotions
            emotion_result = self.analyze_emotion_simple(features_list)
            
            # Calculate features summary
            features_summary = {}
            if features_list:
                for key in features_list[0].keys():
                    values = [f.get(key, 0) for f in features_list if key in f]
                    if values:
                        features_summary[f'average_{key}'] = np.mean(values)
                        features_summary[f'std_{key}'] = np.std(values)
            
            # Generate recommendations
            recommendations = self.generate_facial_recommendations(
                emotion_result['emotion'],
                features_summary
            )
            
            # Calculate emotion score for combination with other analyses
            emotion_score = self.emotion_mapping.get(emotion_result['emotion'], 0.0)
            emotion_score *= emotion_result['confidence']
            
            return {
                "primary_emotion": emotion_result['emotion'],
                "confidence": emotion_result['confidence'],
                "emotion_scores": emotion_result['emotion_scores'],
                "features_summary": features_summary,
                "recommendations": recommendations,
                "emotion_score": emotion_score,
                "frames_analyzed": frames_analyzed,
                "faces_detected": face_detection_count,
                "face_detection_rate": face_detection_count / max(1, frames_analyzed // 10)
            }
            
        except Exception as e:
            return {
                "error": f"Video analysis failed: {str(e)}",
                "emotion": "unknown",
                "confidence": 0.0
            }
    
    def analyze_image(self, image_path):
        """Analyze a single image for facial emotions"""
        if not os.path.exists(image_path):
            return {
                "error": "Image file not found",
                "emotion": "unknown",
                "confidence": 0.0
            }
        
        try:
            # Load image
            frame = cv2.imread(image_path)
            if frame is None:
                return {
                    "error": "Could not load image",
                    "emotion": "unknown",
                    "confidence": 0.0
                }
            
            # Detect faces
            faces = self.detect_faces(frame)
            
            if len(faces) == 0:
                return {
                    "error": "No faces detected in image",
                    "emotion": "unknown",
                    "confidence": 0.0
                }
            
            # Use the largest face
            largest_face = max(faces, key=lambda face: face[2] * face[3])
            
            # Extract features
            features = self.extract_facial_features(frame, largest_face)
            
            # Analyze emotion (using single frame)
            emotion_result = self.analyze_emotion_simple([features])
            
            # Generate recommendations
            recommendations = self.generate_facial_recommendations(
                emotion_result['emotion'],
                features
            )
            
            # Calculate emotion score
            emotion_score = self.emotion_mapping.get(emotion_result['emotion'], 0.0)
            emotion_score *= emotion_result['confidence']
            
            return {
                "primary_emotion": emotion_result['emotion'],
                "confidence": emotion_result['confidence'],
                "emotion_scores": emotion_result['emotion_scores'],
                "features": features,
                "recommendations": recommendations,
                "emotion_score": emotion_score,
                "faces_detected": len(faces)
            }
            
        except Exception as e:
            return {
                "error": f"Image analysis failed: {str(e)}",
                "emotion": "unknown",
                "confidence": 0.0
            } 