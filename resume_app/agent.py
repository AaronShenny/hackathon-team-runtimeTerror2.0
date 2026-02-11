from google.adk import Agent
from google.adk.models import Gemini, BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.models.llm_request import LlmRequest
from google.genai import types
from typing import AsyncGenerator
from .tools import (
    parse_resume_tool,
    semantic_similarity_tool,
    keyword_match_tool,
    ats_checker_tool,
    scoring_tool,
    latex_builder_tool
)
import os


# Define the Gemini model configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBycJgaEHvxJGmo5E4pGZP6wB1FMHboFmI")




class MockGemini(BaseLlm):
    """
    A Mock LLM for testing when no API key is provided.
    """
    model: str = "mock-gemini"

    async def generate_content_async(
        self, llm_request: "LlmRequest", stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        last_msg = ""
        if llm_request.contents:
             last_msg = llm_request.contents[-1].parts[0].text.lower()
        
        if "remove these **" in last_msg or "beautfull" in last_msg:
            text = """### Key Observations & Missing Elements:

1. **Core Languages:** The JD explicitly requires experience in **C++, Java, or Python**. These are currently missing from your profile.
2. **Infrastructure & Systems:** Showcase your experience with **distributed systems and storage architecture**.
3. **Technical Depth:** Highlight your proficiency in **data structures and software test engineering**.
4. **Experience Gap:** Shift focus from campus roles to **technical projects and AI agent development**.

I have implemented these suggestions in your optimized profile below! Would you like me to rebuild your resume now?"""
        elif "rebuild" in last_msg or "resume" in last_msg:
            text = "I've analyzed your profiles and the job description. I'm ready to rebuild your optimized resume with the new skills highlighted. Should I use the **Professional Classic** template?"
        else:
            text = "I see your request! I'm currently in **Simulated Mode** to ensure your demo keeps running smoothly. \n\nI can help you analyze your resume, match keywords, and generate a LaTeX optimized version. What would you like to do first?"

        response = LlmResponse(
            content=types.Content(role="model", parts=[types.Part(text=text)]),
            partial=False
        )
        yield response


def get_resume_agent():
    """
    Initializes and returns the Google ADK Agent for resume building.
    Has a fallback if API_KEY is not provided.
    """
    
    # Check if API key is provided
    use_mock = GEMINI_API_KEY == "YOUR_API_KEY_HERE" or not GEMINI_API_KEY

    if use_mock:
        model = MockGemini()
    else:
        # Set the environment variable for google-genai client
        os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
        model = Gemini(
            model="gemini-2.0-flash-lite"
        )








    agent = Agent(
        name="ResumeAI",
        instruction="""
        You are a smart ATS-optimized Resume Builder.
        Your goal is to help users analyze their resumes against job descriptions and generate optimized versions.
        
        FLOW:
        1. Ask if they have a resume.
        2. If YES: Accept upload, ask for JD, run ATS analysis tools (semantic_similarity_tool, keyword_match_tool, ats_checker_tool), return score via scoring_tool.
        3. Offer to "Rebuild Optimized Resume".
        4. If requested, use the latex_builder_tool with a JSON matching this structure:
           {
             "name": "...",
             "email": "...",
             "phone": "...",
             "summary": "...",
             "experience": [{"title": "...", "company": "...", "dates": "...", "description": "..."}],
             "education": [{"degree": "...", "school": "...", "dates": "..."}],
             "skills": ["...", "..."]
           }
        
        Always use the provided tools for parsing and analysis. 
        When generating a resume, use the latex_builder_tool with the final structured JSON.

        """,
        model=model,
        tools=[
            parse_resume_tool,
            semantic_similarity_tool,
            keyword_match_tool,
            ats_checker_tool,
            scoring_tool,
            latex_builder_tool
        ]
    )
    
    return agent
