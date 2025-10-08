"""
Response schemas for the EduSense AI API endpoints.
Defines Pydantic models for API responses.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


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


class CurriculumWeek(BaseModel):
    """
    Schema for a single week in a curriculum.
    
    Attributes:
        week_number: Week number in the curriculum
        title: Week title/theme
        topics: List of topics to cover
        learning_objectives: Learning objectives for the week
        suggested_activities: Suggested learning activities
    """
    week_number: int = Field(..., description="Week number")
    title: str = Field(..., description="Week title")
    topics: List[str] = Field(..., description="Topics to cover")
    learning_objectives: List[str] = Field(..., description="Learning objectives")
    suggested_activities: Optional[List[str]] = Field(None, description="Suggested activities")


class CurriculumResponse(BaseModel):
    """
    Response schema for curriculum generation endpoint.
    
    Attributes:
        subject: Subject name
        difficulty_level: Difficulty level
        total_weeks: Total curriculum duration
        overview: Curriculum overview
        weeks: List of weekly curriculum items
        prerequisites: Optional prerequisites
        timestamp: Response timestamp
    """
    subject: str = Field(..., description="Subject name")
    difficulty_level: str = Field(..., description="Difficulty level")
    total_weeks: int = Field(..., description="Total weeks")
    overview: str = Field(..., description="Curriculum overview")
    weeks: List[CurriculumWeek] = Field(..., description="Weekly curriculum")
    prerequisites: Optional[List[str]] = Field(None, description="Prerequisites")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class MCQOption(BaseModel):
    """
    Schema for a multiple choice option.
    
    Attributes:
        option: Option label (A, B, C, D)
        text: Option text
    """
    option: str = Field(..., description="Option label")
    text: str = Field(..., description="Option text")


class MCQQuestion(BaseModel):
    """
    Schema for a single MCQ question.
    
    Attributes:
        question_number: Question number
        question: Question text
        options: List of answer options
        correct_answer: Correct answer option
        explanation: Optional explanation for the correct answer
        difficulty: Optional difficulty level
    """
    question_number: int = Field(..., description="Question number")
    question: str = Field(..., description="Question text")
    options: List[MCQOption] = Field(..., description="Answer options")
    correct_answer: str = Field(..., description="Correct answer option (A, B, C, D)")
    explanation: Optional[str] = Field(None, description="Explanation for correct answer")
    difficulty: Optional[str] = Field(None, description="Question difficulty")


class MCQResponse(BaseModel):
    """
    Response schema for MCQ generation endpoint.
    
    Attributes:
        total_questions: Total number of questions generated
        difficulty_level: Overall difficulty level
        questions: List of MCQ questions
        timestamp: Response timestamp
    """
    total_questions: int = Field(..., description="Total questions")
    difficulty_level: str = Field(..., description="Difficulty level")
    questions: List[MCQQuestion] = Field(..., description="MCQ questions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


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


class ErrorResponse(BaseModel):
    """
    Standard error response schema.
    
    Attributes:
        error: Error message
        detail: Optional detailed error information
        status_code: HTTP status code
    """
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")

