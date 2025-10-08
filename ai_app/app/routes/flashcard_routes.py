"""
Flashcard generation API routes.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.flashcard_schemas import GenerateFlashcardsRequest, FlashcardsResponse
from app.schemas.common_schemas import ErrorResponse
from app.services.flashcard_service import flashcard_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcard Generation"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
    },
)


@router.post(
    "",
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
        
        result = await flashcard_service.generate_flashcards(
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
    summary="Flashcard Service Health Check",
    description="Check if the flashcard generation service is operational.",
)
async def health_check():
    """
    Health check endpoint for flashcard service.
    
    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "service": "Flashcard Generation Service",
        "timestamp": datetime.now()
    }

