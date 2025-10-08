"""
Curriculum generation API routes.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.curriculum_schemas import GenerateCurriculumRequest, CurriculumResponse
from app.schemas.common_schemas import ErrorResponse
from app.services.curriculum_service import curriculum_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/curriculum",
    tags=["Curriculum Generation"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
    },
)


@router.post(
    "",
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
        
        result = await curriculum_service.generate_curriculum(
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


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Curriculum Service Health Check",
    description="Check if the curriculum generation service is operational.",
)
async def health_check():
    """
    Health check endpoint for curriculum service.
    
    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "service": "Curriculum Generation Service",
        "timestamp": datetime.now()
    }

