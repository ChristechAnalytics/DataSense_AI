"""
Schemas for curriculum generation functionality.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


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

