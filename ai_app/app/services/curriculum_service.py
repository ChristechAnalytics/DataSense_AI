"""
Curriculum service for generating structured curricula from documents.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import settings
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class CurriculumService:
    """
    Service class for curriculum generation functionality.
    
    Handles AI-powered curriculum creation from documents.
    """
    
    def __init__(self):
        """Initialize the curriculum service with Gemini model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )
            logger.info("Curriculum Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Curriculum Service: {str(e)}")
            raise
    
    async def generate_curriculum(
        self,
        document: str,
        subject: str = None,
        difficulty_level: str = "intermediate",
        duration_weeks: int = 8
    ) -> Dict[str, Any]:
        """
        Generate a structured curriculum from a document.
        
        Args:
            document: Source document content
            subject: Subject or topic name
            difficulty_level: Difficulty level (beginner, intermediate, advanced)
            duration_weeks: Curriculum duration in weeks
            
        Returns:
            Dict containing structured curriculum data
            
        Raises:
            Exception: If curriculum generation fails
        """
        try:
            prompt_template = """You are an expert curriculum designer. Create a comprehensive {duration_weeks}-week curriculum based on the following content.

Content:
{document}

Subject: {subject}
Difficulty Level: {difficulty_level}
Duration: {duration_weeks} weeks

Generate a structured curriculum in JSON format with the following structure:
{{
  "subject": "subject name",
  "difficulty_level": "{difficulty_level}",
  "total_weeks": {duration_weeks},
  "overview": "brief overview of the curriculum",
  "prerequisites": ["prerequisite 1", "prerequisite 2"],
  "weeks": [
    {{
      "week_number": 1,
      "title": "week title",
      "topics": ["topic 1", "topic 2"],
      "learning_objectives": ["objective 1", "objective 2"],
      "suggested_activities": ["activity 1", "activity 2"]
    }}
  ]
}}

Ensure the curriculum is comprehensive, well-structured, and appropriate for the {difficulty_level} level.

JSON Response:"""
            
            prompt = PromptTemplate(
                input_variables=["document", "subject", "difficulty_level", "duration_weeks"],
                template=prompt_template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = await chain.ainvoke({
                "document": document,
                "subject": subject or "General Studies",
                "difficulty_level": difficulty_level,
                "duration_weeks": duration_weeks
            })
            
            # Parse JSON response
            curriculum_data = self._parse_json_response(result["text"])
            
            return curriculum_data
            
        except Exception as e:
            logger.error(f"Error in generate_curriculum: {str(e)}")
            raise Exception(f"Failed to generate curriculum: {str(e)}")
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON from AI response, handling potential formatting issues.
        
        Args:
            response: Raw AI response text
            
        Returns:
            Parsed JSON dict
            
        Raises:
            ValueError: If JSON parsing fails
        """
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                response = response[json_start:json_end].strip()
            
            # Parse JSON
            return json.loads(response.strip())
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}\nResponse: {response}")
            raise ValueError(f"Invalid JSON response from AI: {str(e)}")


# Global curriculum service instance
curriculum_service = CurriculumService()

