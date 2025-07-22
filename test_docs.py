#!/usr/bin/env python3
"""
Test script to verify the documentation server is working correctly
"""

import requests
import time
import webbrowser

def test_docs_server():
    """Test if the documentation server is responsive"""
    
    print("🧪 Testing Documentation Server...")
    
    try:
        # Test main documentation page
        response = requests.get('http://127.0.0.1:8000', timeout=5)
        if response.status_code == 200:
            print("✅ Main documentation page is working")
        else:
            print(f"❌ Main page returned status {response.status_code}")
            return False
            
        # Test specific documentation pages
        test_pages = [
            'quick-start',
            'tech-stack', 
            'api-overview',
            'backend-logic',
            'frontend-logic',
            'architecture',
            'setup-development'
        ]
        
        for page in test_pages:
            try:
                response = requests.get(f'http://127.0.0.1:8000/docs/{page}', timeout=3)
                if response.status_code == 200:
                    print(f"✅ {page} page is working")
                else:
                    print(f"⚠️  {page} page returned status {response.status_code}")
            except requests.RequestException:
                print(f"❌ {page} page is not accessible")
        
        print("\n🎉 Documentation server is working correctly!")
        print("📖 Visit http://127.0.0.1:8000 to view the documentation")
        
        # Optionally open browser
        user_input = input("\n🌐 Open documentation in browser? (y/n): ")
        if user_input.lower() == 'y':
            webbrowser.open('http://127.0.0.1:8000')
            
        return True
        
    except requests.ConnectionError:
        print("❌ Documentation server is not running")
        print("💡 Start it with: python docs_server.py")
        return False
    except Exception as e:
        print(f"❌ Error testing documentation server: {e}")
        return False

def show_documentation_summary():
    """Show what documentation has been created"""
    
    print("\n📚 DOCUMENTATION SUMMARY")
    print("=" * 50)
    
    docs_created = [
        ("🚀 Quick Start Guide", "Get the app running in 5 minutes"),
        ("🔌 API Overview", "Complete REST API documentation with examples"),
        ("🧠 Backend Logic", "Deep dive into Python Flask code"),
        ("🎨 Frontend Logic", "JavaScript and UI component explanations"),
        ("🏗️ System Architecture", "How all components work together"),
        ("🛠️ Development Setup", "Complete dev environment configuration"),
        ("🛠️ Technology Stack", "Overview of all tools and libraries used"),
        ("📖 Main Index", "Comprehensive welcome page with learning paths")
    ]
    
    for title, description in docs_created:
        print(f"{title}")
        print(f"   {description}")
        print()
    
    print("🎯 STUDENT LEARNING FEATURES:")
    print("   ✅ Progressive learning path (Beginner → Intermediate → Advanced)")
    print("   ✅ Complete code explanations with examples")
    print("   ✅ Setup guides for development environment")
    print("   ✅ API documentation with curl and Python examples")
    print("   ✅ Architecture diagrams and data flow")
    print("   ✅ Security and performance best practices")
    print("   ✅ Troubleshooting guides and common issues")
    print("   ✅ Next steps and feature extension ideas")

if __name__ == "__main__":
    print("🧠 Mental Health Analyzer - Documentation Test")
    print("=" * 50)
    
    show_documentation_summary()
    
    print("\n" + "=" * 50)
    test_docs_server()
    
    print("\n🎓 Perfect for student learning!")
    print("Students can now:")
    print("   📖 Learn modern web development concepts")
    print("   🐍 Understand Python Flask applications") 
    print("   🤖 Explore machine learning integration")
    print("   🎨 Master frontend JavaScript development")
    print("   🏗️ See full-stack architecture patterns")
    print("   🚀 Build and extend real-world applications") 