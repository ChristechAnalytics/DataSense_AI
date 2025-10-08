"""Routes module for API endpoints."""

from app.routes.chat_routes import router as chat_router
from app.routes.curriculum_routes import router as curriculum_router
from app.routes.mcq_routes import router as mcq_router
from app.routes.flashcard_routes import router as flashcard_router

__all__ = [
    "chat_router",
    "curriculum_router",
    "mcq_router",
    "flashcard_router",
]
