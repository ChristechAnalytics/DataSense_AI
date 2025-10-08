"""
Chat with notes API routes.
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas.chat_schemas import ChatWithNotesRequest, ChatResponse
from app.schemas.common_schemas import ErrorResponse
from app.services.chat_service import chat_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Chat with Notes"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        400: {"model": ErrorResponse, "description": "Bad Request"},
    },
)


@router.post(
    "",
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
        
        result = await chat_service.chat_with_notes(
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


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Chat Service Health Check",
    description="Check if the chat service is operational.",
)
async def health_check():
    """
    Health check endpoint for chat service.
    
    Returns:
        Dict with health status
    """
    return {
        "status": "healthy",
        "service": "Chat with Notes Service",
        "timestamp": datetime.now()
    }

