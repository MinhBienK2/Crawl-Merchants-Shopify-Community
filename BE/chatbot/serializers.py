"""Serializers for chatbot API."""
from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    
    class Meta:
        model = Message
        fields = ['id', 'conversation_id', 'role', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationSummarySerializer(serializers.ModelSerializer):
    """Serializer for conversation list view."""
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at']


class ConversationDetailSerializer(serializers.ModelSerializer):
    """Serializer for conversation detail with messages."""
    
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'messages']


class ChatRequestSerializer(serializers.Serializer):
    """Serializer for chat request."""
    
    message = serializers.CharField(min_length=1)
    conversation_id = serializers.IntegerField(required=False, allow_null=True)


class ChatResponseSerializer(serializers.Serializer):
    """Serializer for chat response."""
    
    conversation_id = serializers.IntegerField()
    message = serializers.CharField()
    messages = MessageSerializer(many=True)
