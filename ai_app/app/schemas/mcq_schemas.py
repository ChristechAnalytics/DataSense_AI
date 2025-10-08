"""
Schemas for MCQ generation functionality.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


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

