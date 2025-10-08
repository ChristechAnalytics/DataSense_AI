"""
Example script to test the EduSense AI API endpoints.
Make sure the server is running before executing this script.

Usage:
    python test_example.py
"""

import requests
import json
from typing import Dict, Any


BASE_URL = "http://localhost:8000"


def print_response(title: str, response: Dict[Any, Any]):
    """Pretty print API response."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)
    print(json.dumps(response, indent=2, default=str))
    print('=' * 60)


def test_health_check():
    """Test the health check endpoint."""
    print("\n🔍 Testing Health Check Endpoint...")
    response = requests.get(f"{BASE_URL}/api/v1/education/health")
    
    if response.status_code == 200:
        print("✅ Health check passed!")
        print_response("Health Check Response", response.json())
    else:
        print(f"❌ Health check failed with status {response.status_code}")
        print(response.text)


def test_chat_with_notes():
    """Test the chat with notes endpoint."""
    print("\n💬 Testing Chat with Notes Endpoint...")
    
    payload = {
        "notes": """
        Python is a high-level, interpreted programming language created by Guido van Rossum.
        It was first released in 1991. Python supports multiple programming paradigms including
        procedural, object-oriented, and functional programming. It is known for its simple syntax
        and readability, making it an excellent choice for beginners and experts alike.
        """,
        "question": "When was Python first released and who created it?",
        "context": None
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/education/chat",
        json=payload
    )
    
    if response.status_code == 200:
        print("✅ Chat endpoint test passed!")
        print_response("Chat Response", response.json())
    else:
        print(f"❌ Chat endpoint failed with status {response.status_code}")
        print(response.text)


def test_generate_curriculum():
    """Test the curriculum generation endpoint."""
    print("\n📚 Testing Curriculum Generation Endpoint...")
    
    payload = {
        "document": """
        Introduction to Web Development covers HTML, CSS, and JavaScript fundamentals.
        Students will learn to create responsive websites, work with the DOM, handle events,
        and make asynchronous requests. The course includes best practices for accessibility,
        performance optimization, and modern web development tools like Git and VS Code.
        """,
        "subject": "Web Development Fundamentals",
        "difficulty_level": "beginner",
        "duration_weeks": 6
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/education/curriculum",
        json=payload
    )
    
    if response.status_code == 200:
        print("✅ Curriculum generation test passed!")
        print_response("Curriculum Response", response.json())
    else:
        print(f"❌ Curriculum generation failed with status {response.status_code}")
        print(response.text)


def test_generate_mcq():
    """Test the MCQ generation endpoint."""
    print("\n✅ Testing MCQ Generation Endpoint...")
    
    payload = {
        "content": """
        Photosynthesis is the process by which green plants and some other organisms use
        sunlight to synthesize foods with the help of chlorophyll. The process converts
        carbon dioxide and water into glucose and oxygen. The general equation is:
        6CO2 + 6H2O + light energy → C6H12O6 + 6O2
        """,
        "num_questions": 3,
        "difficulty_level": "medium",
        "include_explanations": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/education/mcq",
        json=payload
    )
    
    if response.status_code == 200:
        print("✅ MCQ generation test passed!")
        print_response("MCQ Response", response.json())
    else:
        print(f"❌ MCQ generation failed with status {response.status_code}")
        print(response.text)


def test_generate_flashcards():
    """Test the flashcard generation endpoint."""
    print("\n🎴 Testing Flashcard Generation Endpoint...")
    
    payload = {
        "content": """
        Machine Learning is a subset of artificial intelligence that enables systems to
        learn and improve from experience without being explicitly programmed. There are
        three main types: supervised learning (with labeled data), unsupervised learning
        (finding patterns in unlabeled data), and reinforcement learning (learning through
        trial and error with rewards). Common algorithms include decision trees, neural
        networks, support vector machines, and k-means clustering.
        """,
        "num_flashcards": 5,
        "focus_areas": "key concepts and algorithms"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/education/flashcards",
        json=payload
    )
    
    if response.status_code == 200:
        print("✅ Flashcard generation test passed!")
        print_response("Flashcard Response", response.json())
    else:
        print(f"❌ Flashcard generation failed with status {response.status_code}")
        print(response.text)


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  🧪 EduSense AI API Testing Suite")
    print("=" * 60)
    print("\nMake sure the server is running at", BASE_URL)
    print("Start it with: python run.py\n")
    
    try:
        # Test health check first
        test_health_check()
        
        # Run API tests
        test_chat_with_notes()
        test_generate_curriculum()
        test_generate_mcq()
        test_generate_flashcards()
        
        print("\n" + "=" * 60)
        print("  ✨ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("Make sure the server is running at", BASE_URL)
        print("Start it with: python run.py")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")


if __name__ == "__main__":
    main()

