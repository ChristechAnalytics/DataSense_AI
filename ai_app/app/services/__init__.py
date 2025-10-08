"""Services module for business logic and AI operations."""

from app.services.chat_service import chat_service, ChatService
from app.services.curriculum_service import curriculum_service, CurriculumService
from app.services.mcq_service import mcq_service, MCQService
from app.services.flashcard_service import flashcard_service, FlashcardService

__all__ = [
    "chat_service",
    "ChatService",
    "curriculum_service",
    "CurriculumService",
    "mcq_service",
    "MCQService",
    "flashcard_service",
    "FlashcardService",
]
