"""
Request schemas for the EduSense AI API endpoints.
Defines Pydantic models for validating incoming requests.
"""

from pydantic import BaseModel, Field
from typing import Optional


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


class GenerateCurriculumRequest(BaseModel):
    """
    Request schema for generating a curriculum from a document.
    
    Attributes:
        document: The source document content
        subject: Optional subject/topic name
        difficulty_level: Optional difficulty level (beginner, intermediate, advanced)
        duration_weeks: Optional curriculum duration in weeks
    """
    document: str = Field(..., description="Document content for curriculum generation", min_length=50)
    subject: Optional[str] = Field(None, description="Subject or topic name")
    difficulty_level: Optional[str] = Field("intermediate", description="Difficulty level")
    duration_weeks: Optional[int] = Field(8, description="Curriculum duration in weeks", ge=1, le=52)
    
    class Config:
        json_schema_extra = {
            "example": {
                "document": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience...",
                "subject": "Machine Learning Fundamentals",
                "difficulty_level": "intermediate",
                "duration_weeks": 12
            }
        }


class GenerateMCQRequest(BaseModel):
    """
    Request schema for generating multiple choice questions.
    
    Attributes:
        content: The content to generate questions from
        num_questions: Number of MCQs to generate
        difficulty_level: Optional difficulty level
        include_explanations: Whether to include explanations for answers
    """
    content: str = Field(..., description="Content to generate MCQs from", min_length=50)
    num_questions: int = Field(5, description="Number of questions to generate", ge=1, le=20)
    difficulty_level: Optional[str] = Field("medium", description="Difficulty level (easy, medium, hard)")
    include_explanations: bool = Field(True, description="Include explanations for correct answers")
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "Photosynthesis is the process by which plants convert light energy into chemical energy...",
                "num_questions": 5,
                "difficulty_level": "medium",
                "include_explanations": True
            }
        }


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

