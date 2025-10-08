"""
AI Service for LangChain and Gemini AI integration.
Handles all AI-powered educational content generation.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.config import settings
from typing import Dict, Any, List
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIService:
    """
    Service class for AI operations using LangChain and Gemini.
    
    This class provides methods for:
    - Chatting with notes/knowledge base
    - Generating curriculum from documents
    - Creating MCQ questions
    - Generating flashcards
    """
    
    def __init__(self):
        """Initialize the AI service with Gemini model."""
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.model_name,
                google_api_key=settings.google_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )
            logger.info("AI Service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Service: {str(e)}")
            raise
    
    async def chat_with_notes(
        self,
        notes: str,
        question: str,
        context: str = None
    ) -> Dict[str, Any]:
        """
        Chat with class notes using AI.
        
        Args:
            notes: The class notes or knowledge base content
            question: User's question about the notes
            context: Optional previous conversation context
            
        Returns:
            Dict containing the answer and metadata
            
        Raises:
            Exception: If AI generation fails
        """
        try:
            prompt_template = """You are an expert educational assistant helping students understand their class notes.

Class Notes:
{notes}

{context_section}

Question: {question}

Provide a clear, accurate, and educational answer based on the notes provided. If the question cannot be answered from the notes, politely say so and suggest what additional information might be needed.

Answer:"""
            
            context_section = f"Previous Context:\n{context}\n" if context else ""
            
            prompt = PromptTemplate(
                input_variables=["notes", "question", "context_section"],
                template=prompt_template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = await chain.ainvoke({
                "notes": notes,
                "question": question,
                "context_section": context_section
            })
            
            return {
                "answer": result["text"].strip(),
                "confidence": 0.85,  # You can implement confidence scoring if needed
                "sources": self._extract_relevant_snippets(notes, question)
            }
            
        except Exception as e:
            logger.error(f"Error in chat_with_notes: {str(e)}")
            raise Exception(f"Failed to generate answer: {str(e)}")
    
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
    
    async def generate_flashcards(
        self,
        content: str,
        num_flashcards: int = 10,
        focus_areas: str = None
    ) -> Dict[str, Any]:
        """
        Generate flashcards from content.
        
        Args:
            content: Content to generate flashcards from
            num_flashcards: Number of flashcards to generate
            focus_areas: Optional specific areas to focus on
            
        Returns:
            Dict containing flashcard data
            
        Raises:
            Exception: If flashcard generation fails
        """
        try:
            prompt_template = """You are an expert at creating educational flashcards. Generate {num_flashcards} flashcards from the following content.

Content:
{content}

{focus_section}

Generate flashcards in JSON format with this structure:
{{
  "total_cards": {num_flashcards},
  "focus_areas": "{focus_areas}",
  "flashcards": [
    {{
      "card_number": 1,
      "front": "Question or term (concise)",
      "back": "Answer or definition (clear and complete)",
      "category": "topic category",
      "difficulty": "easy/medium/hard"
    }}
  ]
}}

Ensure:
1. Front of card is concise (question/term)
2. Back provides clear, complete answer
3. Cards cover key concepts
4. Mix of difficulty levels
5. Logical categorization

JSON Response:"""
            
            focus_section = f"Focus Areas: {focus_areas}" if focus_areas else "Focus Areas: Cover all key concepts"
            
            prompt = PromptTemplate(
                input_variables=["content", "num_flashcards", "focus_section", "focus_areas"],
                template=prompt_template
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            result = await chain.ainvoke({
                "content": content,
                "num_flashcards": num_flashcards,
                "focus_section": focus_section,
                "focus_areas": focus_areas or "general"
            })
            
            # Parse JSON response
            flashcard_data = self._parse_json_response(result["text"])
            
            return flashcard_data
            
        except Exception as e:
            logger.error(f"Error in generate_flashcards: {str(e)}")
            raise Exception(f"Failed to generate flashcards: {str(e)}")
    
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
    
    def _extract_relevant_snippets(self, notes: str, question: str, max_snippets: int = 3) -> List[str]:
        """
        Extract relevant snippets from notes based on question.
        
        Args:
            notes: The full notes text
            question: The question to match against
            max_snippets: Maximum number of snippets to return
            
        Returns:
            List of relevant text snippets
        """
        # Simple implementation - split into sentences and return first few
        # You could enhance this with semantic similarity
        sentences = notes.split('. ')
        return sentences[:max_snippets] if len(sentences) > max_snippets else sentences


# Global AI service instance
ai_service = AIService()

