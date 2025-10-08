# EduSense AI - Educational Assistant API

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green?style=flat)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange?style=flat)

A powerful FastAPI application that provides AI-powered educational tools using Google's Gemini AI and LangChain. Generate curricula, create practice questions, build flashcards, and chat with your study materials.

## 🌟 Features

- **💬 Chat with Notes**: Ask questions about your class notes and get contextual, AI-powered answers
- **📚 Curriculum Generator**: Transform documents into comprehensive, structured curricula
- **✅ MCQ Generator**: Create practice multiple-choice questions with correct answers and explanations
- **🎴 Flashcard Generator**: Generate study flashcards for effective learning and memorization

All endpoints accept text input and return structured JSON responses for easy integration.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Endpoints](#-endpoints)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Security](#-security)
- [Contributing](#-contributing)
- [License](#-license)

## 🔧 Prerequisites

- Python 3.9 or higher
- Google Cloud account with Gemini API access
- Google Gemini API key

## 📦 Installation

### 1. Clone the Repository

```bash
cd ai_app
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 2. Set Up Environment Variables

Create a `.env` file in the `ai_app` directory:

```bash
# Copy the example file
cp .env.example .env
```

Edit the `.env` file and add your Google API key:

```env
# Google Gemini AI Configuration
GOOGLE_API_KEY=your_actual_google_api_key_here

# Application Configuration
APP_NAME=EduSense AI
APP_VERSION=1.0.0
DEBUG_MODE=False

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**⚠️ Security Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## 🚀 Running the Application

### Development Mode

```bash
# From the ai_app directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or run directly:

```bash
python app/main.py
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📖 API Documentation

Once the application is running, visit:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs) - Interactive API documentation
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc) - Alternative API documentation

## 🔌 Endpoints

### 1. Chat with Notes

**POST** `/api/v1/education/chat`

Ask questions about your class notes and get AI-powered answers.

**Request:**
```json
{
  "notes": "Python is a high-level programming language...",
  "question": "What are the key features of Python?",
  "context": null
}
```

**Response:**
```json
{
  "answer": "Based on your notes, Python's key features include...",
  "confidence": 0.85,
  "sources": ["Python is a high-level programming language..."],
  "timestamp": "2025-10-08T16:30:00"
}
```

### 2. Generate Curriculum

**POST** `/api/v1/education/curriculum`

Generate a structured curriculum from course content.

**Request:**
```json
{
  "document": "Machine learning is a subset of AI...",
  "subject": "Machine Learning Fundamentals",
  "difficulty_level": "intermediate",
  "duration_weeks": 12
}
```

**Response:**
```json
{
  "subject": "Machine Learning Fundamentals",
  "difficulty_level": "intermediate",
  "total_weeks": 12,
  "overview": "Comprehensive ML curriculum...",
  "weeks": [
    {
      "week_number": 1,
      "title": "Introduction to ML",
      "topics": ["What is ML?", "Types of learning"],
      "learning_objectives": ["Understand ML basics"],
      "suggested_activities": ["Read chapters 1-2"]
    }
  ],
  "prerequisites": ["Python basics", "Statistics"],
  "timestamp": "2025-10-08T16:30:00"
}
```

### 3. Generate MCQ Questions

**POST** `/api/v1/education/mcq`

Generate multiple-choice questions with answers and explanations.

**Request:**
```json
{
  "content": "Photosynthesis is the process...",
  "num_questions": 5,
  "difficulty_level": "medium",
  "include_explanations": true
}
```

**Response:**
```json
{
  "total_questions": 5,
  "difficulty_level": "medium",
  "questions": [
    {
      "question_number": 1,
      "question": "What is the primary purpose of photosynthesis?",
      "options": [
        {"option": "A", "text": "Convert light to chemical energy"},
        {"option": "B", "text": "Produce oxygen"},
        {"option": "C", "text": "Absorb water"},
        {"option": "D", "text": "Release CO2"}
      ],
      "correct_answer": "A",
      "explanation": "Photosynthesis converts light energy...",
      "difficulty": "medium"
    }
  ],
  "timestamp": "2025-10-08T16:30:00"
}
```

### 4. Generate Flashcards

**POST** `/api/v1/education/flashcards`

Generate study flashcards from learning materials.

**Request:**
```json
{
  "content": "The water cycle describes how water evaporates...",
  "num_flashcards": 10,
  "focus_areas": "key terms and processes"
}
```

**Response:**
```json
{
  "total_cards": 10,
  "focus_areas": "key terms and processes",
  "flashcards": [
    {
      "card_number": 1,
      "front": "What is evaporation?",
      "back": "The process by which water changes from liquid to gas",
      "category": "Water Cycle",
      "difficulty": "easy"
    }
  ],
  "timestamp": "2025-10-08T16:30:00"
}
```

### 5. Health Check

**GET** `/api/v1/education/health`

Check if the API is operational.

**Response:**
```json
{
  "status": "healthy",
  "service": "Education AI API",
  "timestamp": "2025-10-08T16:30:00"
}
```

## 💡 Usage Examples

### Using cURL

**Chat with Notes:**
```bash
curl -X POST "http://localhost:8000/api/v1/education/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Python supports object-oriented, functional, and procedural programming.",
    "question": "What programming paradigms does Python support?"
  }'
```

**Generate MCQs:**
```bash
curl -X POST "http://localhost:8000/api/v1/education/mcq" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "The mitochondria is the powerhouse of the cell...",
    "num_questions": 3,
    "difficulty_level": "easy"
  }'
```

### Using Python Requests

```python
import requests

# Chat endpoint
response = requests.post(
    "http://localhost:8000/api/v1/education/chat",
    json={
        "notes": "FastAPI is a modern Python web framework...",
        "question": "What is FastAPI?"
    }
)
print(response.json())

# Flashcards endpoint
response = requests.post(
    "http://localhost:8000/api/v1/education/flashcards",
    json={
        "content": "Machine learning algorithms learn from data...",
        "num_flashcards": 5
    }
)
print(response.json())
```

### Using JavaScript/Fetch

```javascript
// Generate curriculum
fetch('http://localhost:8000/api/v1/education/curriculum', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    document: 'Data Science involves statistics, programming...',
    subject: 'Data Science Fundamentals',
    duration_weeks: 8
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📁 Project Structure

```
ai_app/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration and environment variables
│   ├── routes/
│   │   ├── __init__.py
│   │   └── education.py        # API route handlers
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── requests.py         # Pydantic request models
│   │   └── responses.py        # Pydantic response models
│   ├── services/
│   │   ├── __init__.py
│   │   └── ai_service.py       # LangChain & Gemini AI integration
│   └── models/
│       └── __init__.py         # Database models (future)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🔒 Security

This application follows security best practices:

### ✅ Implemented Security Measures

1. **Input Validation**: All inputs validated using Pydantic models
2. **Environment Variables**: Sensitive data stored in `.env` file
3. **CORS Configuration**: Configurable CORS middleware
4. **Error Handling**: Comprehensive error handling without leaking sensitive information
5. **Logging**: Security-conscious logging that doesn't expose secrets
6. **Type Safety**: Strong typing with Pydantic for data validation

### 🔐 Security Recommendations

1. **API Key Protection**: Never commit your `.env` file or expose your API key
2. **CORS**: Configure `allow_origins` in production to specific domains
3. **HTTPS**: Use HTTPS in production environments
4. **Rate Limiting**: Implement rate limiting for production (consider using FastAPI-Limiter)
5. **Authentication**: Add authentication middleware for production use
6. **Input Sanitization**: All text inputs are validated and sanitized
7. **Regular Updates**: Keep dependencies updated regularly

## 🧪 Testing

To run tests (when implemented):

```bash
pytest
```

To check linting:

```bash
flake8 app/
black app/ --check
```

## 🛠️ Development

### Code Style

This project follows:
- **PEP 8** style guide
- **Black** for code formatting
- **Type hints** for better code clarity
- **Docstrings** for all modules, classes, and functions

### Adding New Endpoints

1. Define request/response schemas in `app/schemas/`
2. Implement service logic in `app/services/`
3. Create route handler in `app/routes/`
4. Register router in `app/main.py`

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues, questions, or contributions, please open an issue on the repository.

## 🙏 Acknowledgments

- **FastAPI**: Modern Python web framework
- **LangChain**: Framework for building LLM applications
- **Google Gemini**: Powerful AI model
- **Pydantic**: Data validation using Python type annotations

---

**Built with ❤️ using FastAPI, LangChain, and Google Gemini AI**

