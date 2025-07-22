#!/usr/bin/env python3
"""
Quick test script to verify Mental Health Analyzer setup
"""

import sys
import os
import importlib.util

def test_python_version():
    """Test if Python version is compatible"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def test_required_modules():
    """Test if required modules can be imported"""
    required_modules = [
        'flask', 'numpy', 'sklearn', 'nltk', 'textblob', 
        'vaderSentiment', 'librosa', 'cv2', 'json', 'os'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'cv2':
                import cv2
            elif module == 'sklearn':
                import sklearn
            else:
                __import__(module)
            print(f"✅ {module} - Available")
        except ImportError:
            print(f"❌ {module} - Missing")
            missing_modules.append(module)
    
    return len(missing_modules) == 0, missing_modules

def test_file_structure():
    """Test if required files and directories exist"""
    required_items = [
        ('file', 'app.py'),
        ('file', 'requirements.txt'),
        ('file', 'questions/questions.json'),
        ('file', 'templates/index.html'),
        ('file', 'static/js/app.js'),
        ('file', 'static/js/recorder.js'),
        ('file', 'analysis/text_analysis.py'),
        ('file', 'analysis/voice_analysis.py'),
        ('file', 'analysis/facial_analysis.py'),
        ('file', 'utils/preprocess.py'),
        ('dir', 'analysis'),
        ('dir', 'templates'),
        ('dir', 'static'),
        ('dir', 'questions'),
        ('dir', 'utils')
    ]
    
    missing_items = []
    for item_type, path in required_items:
        if item_type == 'file' and os.path.isfile(path):
            print(f"✅ {path} - Exists")
        elif item_type == 'dir' and os.path.isdir(path):
            print(f"✅ {path}/ - Exists")
        else:
            print(f"❌ {path} - Missing")
            missing_items.append(path)
    
    return len(missing_items) == 0, missing_items

def test_analysis_modules():
    """Test if analysis modules can be imported"""
    try:
        from analysis.text_analysis import TextAnalyzer
        from analysis.voice_analysis import VoiceAnalyzer
        from analysis.facial_analysis import FacialAnalyzer
        print("✅ Analysis modules - Importable")
        
        # Test initialization
        text_analyzer = TextAnalyzer()
        voice_analyzer = VoiceAnalyzer()
        facial_analyzer = FacialAnalyzer()
        print("✅ Analyzers - Initializable")
        return True
    except Exception as e:
        print(f"❌ Analysis modules - Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧠 Mental Health Analyzer - Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test Python version
    print("\n📋 Testing Python Version:")
    if not test_python_version():
        all_passed = False
    
    # Test required modules
    print("\n📦 Testing Required Modules:")
    modules_ok, missing = test_required_modules()
    if not modules_ok:
        all_passed = False
        print(f"\n💡 Missing modules: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
    
    # Test file structure
    print("\n📁 Testing File Structure:")
    files_ok, missing_files = test_file_structure()
    if not files_ok:
        all_passed = False
        print(f"\n💡 Missing files: {', '.join(missing_files)}")
    
    # Test analysis modules
    print("\n🔧 Testing Analysis Modules:")
    if not test_analysis_modules():
        all_passed = False
    
    # Final result
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! Ready to run the application.")
        print("💡 Run: ./run_app.sh or python app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("💡 Try running: pip install -r requirements.txt")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 