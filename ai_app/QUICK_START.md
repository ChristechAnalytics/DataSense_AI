# Quick Start Guide - EduSense AI

Get up and running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
cd ai_app
pip install -r requirements.txt
```

### 2. Configure API Key

1. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Create a `.env` file:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

3. Edit `.env` and add your API key:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

**Option 1 - Using the run script:**
```bash
python run.py
```

**Option 2 - Using uvicorn directly:**
```bash
uvicorn app.main:app --reload
```

**Option 3 - Using Python module:**
```bash
python -m uvicorn app.main:app --reload
```

### 4. Access the API

Open your browser:
- **API Docs**: http://localhost:8000/docs
- **API Root**: http://localhost:8000

## 📝 Quick Test

### Test with cURL

```bash
# Health check
curl http://localhost:8000/api/v1/education/health

# Chat with notes
curl -X POST http://localhost:8000/api/v1/education/chat \
  -H "Content-Type: application/json" \
  -d "{\"notes\":\"Python is a programming language\",\"question\":\"What is Python?\"}"
```

### Test with Python

```python
import requests

# Chat endpoint
response = requests.post(
    "http://localhost:8000/api/v1/education/chat",
    json={
        "notes": "Machine learning uses algorithms to learn from data",
        "question": "What is machine learning?"
    }
)
print(response.json())
```

## 🎯 Available Endpoints

1. **Chat with Notes**: `POST /api/v1/education/chat`
2. **Generate Curriculum**: `POST /api/v1/education/curriculum`
3. **Generate MCQs**: `POST /api/v1/education/mcq`
4. **Generate Flashcards**: `POST /api/v1/education/flashcards`
5. **Health Check**: `GET /api/v1/education/health`

## ⚠️ Common Issues

### Issue: "ModuleNotFoundError"
**Solution**: Make sure you've activated your virtual environment and installed dependencies
```bash
pip install -r requirements.txt
```

### Issue: "GOOGLE_API_KEY not found"
**Solution**: Create a `.env` file with your API key (see step 2 above)

### Issue: "Port already in use"
**Solution**: Change the port in `.env` or kill the process using port 8000
```bash
# Windows
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :8000
```

## 📖 Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore the interactive docs at http://localhost:8000/docs
3. Try all 4 endpoints with your own content
4. Integrate the API into your application

## 💡 Tips

- Use the `/docs` endpoint for interactive API testing
- All endpoints return JSON responses
- Text inputs can be copy-pasted directly
- Check the logs for debugging information

Enjoy using EduSense AI! 🎓✨

