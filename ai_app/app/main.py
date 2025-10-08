"""
Main FastAPI application for EduSense AI.
Provides AI-powered educational endpoints for chat, curriculum, MCQs, and flashcards.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routes import education_router
from app.config import settings
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    EduSense AI - AI-Powered Educational Assistant API
    
    This API provides intelligent educational tools powered by Google's Gemini AI and LangChain:
    
    **Features:**
    - 💬 Chat with your class notes and get contextual answers
    - 📚 Generate comprehensive curricula from documents
    - ✅ Create practice MCQs with correct answers and explanations
    - 🎴 Generate flashcards for effective learning
    
    All endpoints accept text input and return structured JSON responses.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.
    
    Args:
        request: The incoming request
        exc: The exception that was raised
        
    Returns:
        JSON response with error details
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.debug_mode else "An unexpected error occurred",
            "status_code": 500
        }
    )


# Include routers
app.include_router(education_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Dict with API information and available endpoints
    """
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "timestamp": datetime.now(),
        "documentation": "/docs",
        "endpoints": {
            "chat_with_notes": "/api/v1/education/chat",
            "generate_curriculum": "/api/v1/education/curriculum",
            "generate_mcq": "/api/v1/education/mcq",
            "generate_flashcards": "/api/v1/education/flashcards",
            "health_check": "/api/v1/education/health"
        },
        "description": "AI-powered educational assistant API using Google Gemini and LangChain"
    }


@app.on_event("startup")
async def startup_event():
    """Execute on application startup."""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Debug mode: {settings.debug_mode}")
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown."""
    logger.info("Shutting down application")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug_mode,
        log_level="info"
    )

