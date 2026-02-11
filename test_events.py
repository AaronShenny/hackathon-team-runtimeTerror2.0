from resume_app.agent import get_resume_agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types
import os

# Ensure API key is set
os.environ["GOOGLE_API_KEY"] = "AIzaSyBzUZEZSki8X6PhA_Ga9ZHAoOh5mBokymg"

agent = get_resume_agent()
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

runner = Runner(
    app_name="Test",
    agent=agent,
    session_service=session_service,
    memory_service=memory_service,
    auto_create_session=True
)

user_msg = "remove these ** and make it beautfull like implement these things"
new_message = types.Content(role="user", parts=[types.Part(text=user_msg)])

print(f"Starting run with message: {user_msg}")
try:
    events = list(runner.run(user_id="test", session_id="test_reproduce", new_message=new_message))
    print(f"Received {len(events)} events.")

    for i, event in enumerate(events):
        print(f"Event {i}: {event}")
        if event.error_message:
            print(f"  ERROR: {event.error_message}")
        if event.content:
            for j, part in enumerate(event.content.parts):
                print(f"    Part {j}: text='{part.text}', func_call={part.function_call}")
except Exception as e:
    print(f"CRASH: {e}")
