"""
Education API routes for AI-powered educational features.
Implements endpoints for chat, curriculum, MCQs, and flashcards.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.requests import (
    ChatWithNotesRequest,
    GenerateCurriculumRequest,
    GenerateMCQRequest,
    GenerateFlashcardsRequest,
)
from app.schemas.responses import (
    ChatResponse,
    CurriculumResponse,
    MCQResponse,
    FlashcardsResponse,
    ErrorResponse,
)
from app.services import ai_service
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(
    prefix="/api/v1/education",
    tags=["Education AI"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
    },
)


@router.post(
    "/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chat with Class Notes",
    description="Ask questions about your class notes and get AI-powered answers based on the content provided.",
)
async def chat_with_notes(request: ChatWithNotesRequest) -> ChatResponse:
    """
    Chat with class notes endpoint.
    
    Upload your notes as text and ask questions to get detailed answers
    based on the content. The AI will provide contextual answers derived
    from your notes.
    
    Args:
        request: ChatWithNotesRequest containing notes and question
        
    Returns:
        ChatResponse with answer and metadata
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        logger.info(f"Processing chat request with question: {request.question[:50]}...")
        
        result = await ai_service.chat_with_notes(
            notes=request.notes,
            question=request.question,
            context=request.context
        )
        
        return ChatResponse(
            answer=result["answer"],
            confidence=result.get("confidence"),
            sources=result.get("sources"),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error in chat_with_notes endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.post(
    "/curriculum",
    response_model=CurriculumResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Curriculum",
    description="Generate a structured curriculum from a document or course content.",
)
async def generate_curriculum(request: GenerateCurriculumRequest) -> CurriculumResponse:
    """
    Generate curriculum endpoint.
    
    Upload course content or a document to automatically generate a
    comprehensive, week-by-week curriculum with learning objectives,
    topics, and suggested activities.
    
    Args:
        request: GenerateCurriculumRequest containing document and parameters
        
    Returns:
        CurriculumResponse with structured curriculum
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(f"Generating curriculum for subject: {request.subject}")
        
        result = await ai_service.generate_curriculum(
            document=request.document,
            subject=request.subject,
            difficulty_level=request.difficulty_level,
            duration_weeks=request.duration_weeks
        )
        
        return CurriculumResponse(
            subject=result["subject"],
            difficulty_level=result["difficulty_level"],
            total_weeks=result["total_weeks"],
            overview=result["overview"],
            weeks=result["weeks"],
            prerequisites=result.get("prerequisites"),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error in generate_curriculum endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate curriculum: {str(e)}"
        )


@router.post(
    "/mcq",
    response_model=MCQResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate MCQ Questions",
    description="Generate multiple choice questions with correct answers from your study content.",
)
async def generate_mcq(request: GenerateMCQRequest) -> MCQResponse:
    """
    Generate MCQ questions endpoint.
    
    Upload study content to automatically generate practice multiple choice
    questions with correct answers and optional explanations. Perfect for
    exam preparation and self-assessment.
    
    Args:
        request: GenerateMCQRequest containing content and parameters
        
    Returns:
        MCQResponse with MCQ questions and answers
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(f"Generating {request.num_questions} MCQ questions")
        
        result = await ai_service.generate_mcqs(
            content=request.content,
            num_questions=request.num_questions,
            difficulty_level=request.difficulty_level,
            include_explanations=request.include_explanations
        )
        
        return MCQResponse(
            total_questions=result["total_questions"],
            difficulty_level=result["difficulty_level"],
            questions=result["questions"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error in generate_mcq endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate MCQs: {str(e)}"
        )


@router.post(
    "/flashcards",
    response_model=FlashcardsResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Flashcards",
    description="Generate study flashcards from your learning materials.",
)
async def generate_flashcards(request: GenerateFlashcardsRequest) -> FlashcardsResponse:
    """
    Generate flashcards endpoint.
    
    Upload study content to automatically generate flashcards for effective
    learning and memorization. Each flashcard contains a question/term on
    the front and the answer/definition on the back.
    
    Args:
        request: GenerateFlashcardsRequest containing content and parameters
        
    Returns:
        FlashcardsResponse with generated flashcards
        
    Raises:
        HTTPException: If generation fails
    """
    try:
        logger.info(f"Generating {request.num_flashcards} flashcards")
        
        result = await ai_service.generate_flashcards(
            content=request.content,
            num_flashcards=request.num_flashcards,
            focus_areas=request.focus_areas
        )
        
        return FlashcardsResponse(
            total_cards=result["total_cards"],
            focus_areas=result.get("focus_areas"),
            flashcards=result["flashcards"],
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error in generate_flashcards endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate flashcards: {str(e)}"
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the education API endpoints are operational.",
)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "service": "Education AI API",
        "timestamp": datetime.now()
    }

