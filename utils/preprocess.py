import re
import string
import numpy as np
from typing import List, Dict, Any

def clean_text(text: str) -> str:
    """Clean and preprocess text data"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()

def normalize_audio_features(features: Dict[str, float]) -> Dict[str, float]:
    """Normalize audio features to standard ranges"""
    normalized = {}
    
    for key, value in features.items():
        if isinstance(value, (int, float)):
            # Simple min-max normalization (could be improved with actual data statistics)
            if 'mfcc' in key:
                # MFCCs typically range from -50 to 50
                normalized[key] = np.clip((value + 50) / 100, 0, 1)
            elif 'spectral' in key:
                # Spectral features - rough normalization
                normalized[key] = np.clip(value / 5000, 0, 1)
            elif 'tempo' in key:
                # Tempo typically ranges from 60-180 BPM
                normalized[key] = np.clip((value - 60) / 120, 0, 1)
            else:
                # Default normalization
                normalized[key] = np.clip(value, 0, 1)
        else:
            normalized[key] = value
    
    return normalized

def validate_file_type(filename: str, allowed_types: List[str]) -> bool:
    """Validate if file type is allowed"""
    if not filename:
        return False
    
    file_extension = filename.lower().split('.')[-1]
    return file_extension in allowed_types

def safe_float_conversion(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float with default fallback"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def calculate_confidence_score(scores: List[float]) -> float:
    """Calculate overall confidence score from multiple analysis scores"""
    if not scores:
        return 0.0
    
    # Remove any invalid scores
    valid_scores = [s for s in scores if isinstance(s, (int, float)) and 0 <= s <= 1]
    
    if not valid_scores:
        return 0.0
    
    # Calculate weighted confidence based on consistency
    mean_score = np.mean(valid_scores)
    std_score = np.std(valid_scores)
    
    # Lower standard deviation = higher confidence
    consistency_factor = max(0, 1 - std_score)
    
    # Combine mean and consistency
    confidence = (mean_score * 0.7) + (consistency_factor * 0.3)
    
    return min(0.95, confidence)  # Cap at 95% 