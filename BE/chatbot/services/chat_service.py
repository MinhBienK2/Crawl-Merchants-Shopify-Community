"""Chat service for managing conversations and messages."""
from typing import List, Optional, Tuple

from django.core.exceptions import ObjectDoesNotExist

from ..models import Conversation, Message
from .llm_service import llm_service


class ChatService:
    """Service for chat operations."""

    @staticmethod
    def create_conversation(title: Optional[str] = None) -> Conversation:
        """Create a new conversation."""
        return Conversation.objects.create(title=title)

    @staticmethod
    def get_conversation(conversation_id: int) -> Optional[Conversation]:
        """Get conversation by ID."""
        try:
            return Conversation.objects.get(id=conversation_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_all_conversations(skip: int = 0, limit: int = 100) -> List[Conversation]:
        """Get all conversations."""
        return list(Conversation.objects.all().order_by('-updated_at')[skip:skip+limit])

    @staticmethod
    def get_conversation_messages(conversation_id: int) -> List[Message]:
        """Get all messages for a conversation."""
        return list(Message.objects.filter(conversation_id=conversation_id).order_by('created_at'))

    @staticmethod
    def add_message(conversation_id: int, role: str, content: str) -> Message:
        """Add a message to a conversation."""
        return Message.objects.create(
            conversation_id=conversation_id,
            role=role,
            content=content
        )

    @staticmethod
    def get_conversation_history(conversation_id: int) -> List[dict]:
        """Get conversation history as list of dicts."""
        messages = ChatService.get_conversation_messages(conversation_id)
        return [{"role": msg.role, "content": msg.content} for msg in messages]

    @staticmethod
    def send_message(user_message: str, conversation_id: Optional[int] = None) -> Tuple[int, str, List[Message]]:
        """Send a message and get AI response.

        Returns:
            tuple: (conversation_id, assistant_response, all_messages)
        """
        # Create or get conversation
        if conversation_id:
            conversation = ChatService.get_conversation(conversation_id)
            if not conversation:
                raise ValueError(f"Conversation {conversation_id} not found")
        else:
            # Generate title from first message
            title = llm_service.generate_conversation_title(user_message)
            conversation = ChatService.create_conversation(title=title)

        # Get conversation history
        history_messages = ChatService.get_conversation_history(conversation.id)

        # Get LLM response
        assistant_response = llm_service.get_response(user_message, history_messages)

        # Save user message
        ChatService.add_message(conversation.id, "user", user_message)

        # Save assistant response
        ChatService.add_message(conversation.id, "assistant", assistant_response)

        # Get updated history
        all_messages = ChatService.get_conversation_messages(conversation.id)

        return conversation.id, assistant_response, all_messages

    @staticmethod
    def delete_conversation(conversation_id: int) -> bool:
        """Delete a conversation and all its messages."""
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            conversation.delete()
            return True
        except ObjectDoesNotExist:
            return False


# Global instance
chat_service = ChatService()
