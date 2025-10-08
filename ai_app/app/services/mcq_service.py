"""
MCQ service for generating multiple choice questions from content.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import settings
from typing import Dict, Any
import json
import logging

logger = logging.getLogger(__name__)


class MCQService:
    """
    Service class for MCQ generation functionality.
    
    Handles AI-powered creation of multiple choice questions.
    """
    
    def __init__(self):
        """Initialize the MCQ service with Gemini model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )
            logger.info("MCQ Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize MCQ Service: {str(e)}")
            raise
    
    async def generate_mcqs(
        self,
        content: str,
        num_questions: int = 5,
        difficulty_level: str = "medium",
        include_explanations: bool = True
    ) -> Dict[str, Any]:
        """
        Generate multiple choice questions from content.
        
        Args:
            content: Content to generate questions from
            num_questions: Number of MCQs to generate
            difficulty_level: Difficulty level (easy, medium, hard)
            include_explanations: Whether to include explanations
            
        Returns:
            Dict containing MCQ questions with answers
            
        Raises:
            Exception: If MCQ generation fails
        """
        try:
            prompt_template = """You are an expert test creator. Generate {num_questions} multiple choice questions (MCQs) from the following content.

Content:
{content}

Difficulty Level: {difficulty_level}
Include Explanations: {include_explanations}

Generate questions in JSON format with this structure:
{{
  "total_questions": {num_questions},
  "difficulty_level": "{difficulty_level}",
  "questions": [
    {{
      "question_number": 1,
      "question": "question text",
      "options": [
        {{"option": "A", "text": "option A text"}},
        {{"option": "B", "text": "option B text"}},
        {{"option": "C", "text": "option C text"}},
        {{"option": "D", "text": "option D text"}}
      ],
      "correct_answer": "A",
      "explanation": "explanation for why A is correct",
      "difficulty": "medium"
    }}
  ]
}}

Ensure:
1. Questions are clear and unambiguous
2. All options are plausible
3. Only one correct answer per question
4. Explanations are educational and detailed
5. Questions cover different aspects of the content

JSON Response:"""
            
            prompt = PromptTemplate(
                input_variables=["content", "num_questions", "difficulty_level", "include_explanations"],
                template=prompt_template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = await chain.ainvoke({
                "content": content,
                "num_questions": num_questions,
                "difficulty_level": difficulty_level,
                "include_explanations": str(include_explanations)
            })
            
            # Parse JSON response
            mcq_data = self._parse_json_response(result["text"])
            
            return mcq_data
            
        except Exception as e:
            logger.error(f"Error in generate_mcqs: {str(e)}")
            raise Exception(f"Failed to generate MCQs: {str(e)}")
    
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


# Global MCQ service instance
mcq_service = MCQService()

