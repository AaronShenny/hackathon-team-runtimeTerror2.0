from django.db import models
import uuid

class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    history = models.JSONField(default=list)  # Stores chat history for ADK state management

    def __str__(self):
        return f"Session {self.id} started at {self.created_at}"

class ResumeUpload(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resume exported for {self.session.id} at {self.uploaded_at}"
