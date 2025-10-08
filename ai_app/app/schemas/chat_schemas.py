"""
Schemas for chat with notes functionality.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatWithNotesRequest(BaseModel):
    """
    Request schema for chatting with class notes.
    
    Attributes:
        notes: The class notes or knowledge base content
        question: The user's question about the notes
        context: Optional conversation context for follow-up questions
    """
    notes: str = Field(..., description="Class notes or knowledge base content", min_length=10)
    question: str = Field(..., description="Question to ask about the notes", min_length=3)
    context: Optional[str] = Field(None, description="Previous conversation context")
    
    class Config:
        json_schema_extra = {
            "example": {
                "notes": "Python is a high-level programming language. It supports multiple programming paradigms including procedural, object-oriented, and functional programming.",
                "question": "What programming paradigms does Python support?",
                "context": None
            }
        }


class ChatResponse(BaseModel):
    """
    Response schema for chat with notes endpoint.
    
    Attributes:
        answer: The AI-generated answer to the question
        confidence: Optional confidence score
        sources: Optional list of relevant source snippets
        timestamp: Response timestamp
    """
    answer: str = Field(..., description="AI-generated answer")
    confidence: Optional[float] = Field(None, description="Confidence score (0-1)")
    sources: Optional[List[str]] = Field(None, description="Relevant source snippets")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Python supports three main programming paradigms: procedural, object-oriented, and functional programming.",
                "confidence": 0.95,
                "sources": ["Python supports multiple programming paradigms..."],
                "timestamp": "2025-10-08T16:30:00"
            }
        }

