from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, ResumeUpload
from .agent import get_resume_agent
import os
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.genai import types

# Initialize ADK services (In-memory for prototype)
session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

def chat_view(request):
    """
    Renders the main chat interface.
    """
    session = ChatSession.objects.create()
    return render(request, "chat.html", {"session_id": str(session.id)})

@csrf_exempt
def send_message(request):
    """
    Handles incoming chat messages and file uploads.
    """
    if request.method == "POST":
        session_id = request.POST.get("session_id")
        user_message = request.POST.get("message", "")
        resume_file = request.FILES.get("resume")
        
        try:
            db_session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Session not found"}, status=404)
        
        agent = get_resume_agent()
        
        # Setup Runner
        runner = Runner(
            app_name="ResumeBuilder",
            agent=agent,
            session_service=session_service,
            memory_service=memory_service,
            auto_create_session=True
        )
        
        # Handle file upload
        if resume_file:
            fs = FileSystemStorage()
            filename = fs.save(f"resumes/{resume_file.name}", resume_file)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)
            ResumeUpload.objects.create(session=db_session, file=filename)
            user_message = f"{user_message} [System: User uploaded a file at {file_path}]".strip()

        # Run the agent
        # We'll use the Runner.run (sync wrapper) for this prototype
        # ADK expects types.Content for new_message
        new_message_content = types.Content(role="user", parts=[types.Part(text=user_message)])
        
        response_text = ""
        error_messages = []
        try:
            events = runner.run(
                user_id="anonymous",
                session_id=str(session_id),
                new_message=new_message_content
            )
            
            for event in events:
                if event.error_message:
                    error_messages.append(event.error_message)
                
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text
                        if part.function_call:
                             # Optionally log or notify about function calls
                             pass
            
            if not response_text:
                if error_messages:
                    response_text = f"The agent encountered errors: {', '.join(error_messages)}"
                else:
                    response_text = "The agent did not return a text response. It might be waiting for tool execution or encounter a silent failure. Please check if the API key has quota."

        except Exception as e:
            response_text = f"Critical error running agent: {str(e)}"

        
        return JsonResponse({
            "response": response_text,
            "session_id": session_id
        })

    
    return JsonResponse({"error": "Invalid request"}, status=400)

