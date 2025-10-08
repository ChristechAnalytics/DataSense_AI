"""Schemas module for request and response validation."""

from app.schemas.chat_schemas import ChatWithNotesRequest, ChatResponse
from app.schemas.curriculum_schemas import (
    GenerateCurriculumRequest,
    CurriculumResponse,
    CurriculumWeek,
)
from app.schemas.mcq_schemas import (
    GenerateMCQRequest,
    MCQResponse,
    MCQQuestion,
    MCQOption,
)
from app.schemas.flashcard_schemas import (
    GenerateFlashcardsRequest,
    FlashcardsResponse,
    Flashcard,
)
from app.schemas.common_schemas import ErrorResponse

__all__ = [
    # Chat schemas
    "ChatWithNotesRequest",
    "ChatResponse",
    # Curriculum schemas
    "GenerateCurriculumRequest",
    "CurriculumResponse",
    "CurriculumWeek",
    # MCQ schemas
    "GenerateMCQRequest",
    "MCQResponse",
    "MCQQuestion",
    "MCQOption",
    # Flashcard schemas
    "GenerateFlashcardsRequest",
    "FlashcardsResponse",
    "Flashcard",
    # Common schemas
    "ErrorResponse",
]
