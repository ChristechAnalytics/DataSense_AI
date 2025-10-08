"""Schemas module for request and response validation."""

from app.schemas.requests import (
    ChatWithNotesRequest,
    GenerateCurriculumRequest,
    GenerateMCQRequest,
    GenerateFlashcardsRequest,
)
from app.schemas.responses import (
    ChatResponse,
    CurriculumResponse,
    CurriculumWeek,
    MCQResponse,
    MCQQuestion,
    MCQOption,
    FlashcardsResponse,
    Flashcard,
    ErrorResponse,
)

__all__ = [
    # Request schemas
    "ChatWithNotesRequest",
    "GenerateCurriculumRequest",
    "GenerateMCQRequest",
    "GenerateFlashcardsRequest",
    # Response schemas
    "ChatResponse",
    "CurriculumResponse",
    "CurriculumWeek",
    "MCQResponse",
    "MCQQuestion",
    "MCQOption",
    "FlashcardsResponse",
    "Flashcard",
    "ErrorResponse",
]

