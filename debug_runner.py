import os
import django
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_resume_builder.settings')
django.setup()

from resume_app.agent import get_resume_agent

def test_agent():
    print("Initializing agent...")
    agent = get_resume_agent()
    
    session_service = InMemorySessionService()
    memory_service = InMemoryMemoryService()
    
    runner = Runner(
        app_name="ResumeBuilder",
        agent=agent,
        session_service=session_service,
        memory_service=memory_service,
        auto_create_session=True
    )
    
    print("Running agent...")
    new_message_content = types.Content(role="user", parts=[types.Part(text="Hello")])
    
    events = runner.run(
        user_id="anonymous",
        session_id="test-session",
        new_message=new_message_content
    )
    
    response_text = ""
    for event in events:
        print(f"Received event: {event}")
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text
    
    print(f"Final Response: {response_text}")

if __name__ == "__main__":
    test_agent()
