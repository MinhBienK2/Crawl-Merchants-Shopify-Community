"""Models for chatbot application."""
from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    """Model to store chat conversations."""
    
    title = models.CharField(max_length=500, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        db_table = 'conversations'

    def __str__(self):
        return f"Conversation {self.id}: {self.title or 'Untitled'}"


class Message(models.Model):
    """Model to store individual chat messages."""
    
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        db_table = 'messages'

    def __str__(self):
        return f"Message {self.id} ({self.role}) in Conversation {self.conversation_id}"
