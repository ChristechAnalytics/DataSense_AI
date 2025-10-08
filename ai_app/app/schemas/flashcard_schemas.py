"""
Schemas for flashcard generation functionality.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class GenerateFlashcardsRequest(BaseModel):
    """
    Request schema for generating flashcards.
    
    Attributes:
        content: The content to generate flashcards from
        num_flashcards: Number of flashcards to generate
        focus_areas: Optional specific areas to focus on
    """
    content: str = Field(..., description="Content to generate flashcards from", min_length=50)
    num_flashcards: int = Field(10, description="Number of flashcards to generate", ge=1, le=50)
    focus_areas: Optional[str] = Field(None, description="Specific areas or topics to focus on")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "The water cycle describes how water evaporates from the surface, rises into the atmosphere...",
                "num_flashcards": 10,
                "focus_areas": "key terms and processes"
            }
        }


class Flashcard(BaseModel):
    """
    Schema for a single flashcard.
    
    Attributes:
        card_number: Flashcard number
        front: Front of the card (question/term)
        back: Back of the card (answer/definition)
        category: Optional category or topic
        difficulty: Optional difficulty level
    """
    card_number: int = Field(..., description="Flashcard number")
    front: str = Field(..., description="Front of card (question/term)")
    back: str = Field(..., description="Back of card (answer/definition)")
    category: Optional[str] = Field(None, description="Category or topic")
    difficulty: Optional[str] = Field(None, description="Difficulty level")


class FlashcardsResponse(BaseModel):
    """
    Response schema for flashcard generation endpoint.
    
    Attributes:
        total_cards: Total number of flashcards generated
        focus_areas: Focus areas covered
        flashcards: List of flashcards
        timestamp: Response timestamp
    """
    total_cards: int = Field(..., description="Total flashcards")
    focus_areas: Optional[str] = Field(None, description="Focus areas")
    flashcards: List[Flashcard] = Field(..., description="Flashcards")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

