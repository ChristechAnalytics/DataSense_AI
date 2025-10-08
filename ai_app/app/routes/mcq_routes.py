"""
MCQ generation API routes.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.mcq_schemas import GenerateMCQRequest, MCQResponse
from app.schemas.common_schemas import ErrorResponse
from app.services.mcq_service import mcq_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/mcq",
    tags=["MCQ Generation"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
    },
)


@router.post(
    "",
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
        
        result = await mcq_service.generate_mcqs(
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


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="MCQ Service Health Check",
    description="Check if the MCQ generation service is operational.",
)
async def health_check():
    """
    Health check endpoint for MCQ service.
    
    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "service": "MCQ Generation Service",
        "timestamp": datetime.now()
    }

