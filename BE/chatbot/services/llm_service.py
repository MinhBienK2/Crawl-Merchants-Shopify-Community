"""LLM service for chat functionality."""
from typing import List, Optional

from django.conf import settings
from openai import OpenAI, AzureOpenAI

from .data_loader import data_loader


class LLMService:
    """Service for LLM interactions."""

    def __init__(self):
        """Initialize LLM service."""
        # Initialize client based on configuration
        if settings.USE_AZURE_OPENAI:
            self.client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.AZURE_OPENAI_API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )
            self.model = settings.AZURE_OPENAI_DEPLOYMENT_NAME
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL
        self.system_prompt = """You are a helpful assistant that answers questions about Shopify Community forum threads.
You have access to crawled data from the Shopify Community forum. Use this context to provide accurate and helpful answers.

When answering:
- Be concise and clear
- Reference specific threads or posts when relevant
- If you don't have information about something, say so
- Answer in the same language as the user's question
- Provide relevant thread URLs when available

Context from Shopify Community data:
{context}
"""

    def get_response(
        self, user_message: str, conversation_history: Optional[List[dict]] = None, context: Optional[str] = None
    ) -> str:
        """Get LLM response for user message."""
        # Get relevant context if not provided
        if context is None:
            context = data_loader.get_context_for_llm(user_message)

        # Prepare system message with context
        system_message = self.system_prompt.format(context=context)

        # Prepare messages
        messages = [{"role": "system", "content": system_message}]

        # Add conversation history if available
        if conversation_history:
            for msg in conversation_history[-10:]:  # Limit to last 10 messages
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Get response from OpenAI
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Error getting response: {str(e)}"

    def generate_conversation_title(self, first_message: str) -> str:
        """Generate a title for conversation based on first message."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Generate a short title (max 50 characters) for this conversation based on the first message. Return only the title, nothing else.",
                    },
                    {"role": "user", "content": first_message},
                ],
                temperature=0.5,
                max_tokens=50,
            )
            title = response.choices[0].message.content.strip()
            # Truncate to 50 chars if needed
            return title[:50] if len(title) > 50 else title
        except Exception:
            # Fallback to truncated message
            return first_message[:50] + "..." if len(first_message) > 50 else first_message


# Global instance
llm_service = LLMService()
