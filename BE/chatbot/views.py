"""Views for chatbot API."""
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    ChatRequestSerializer,
    ChatResponseSerializer,
    ConversationDetailSerializer,
    ConversationSummarySerializer,
)
from .services.chat_service import chat_service


@api_view(['POST'])
def chat(request):
    """Send a message and get AI response."""
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    message = serializer.validated_data['message']
    conversation_id = serializer.validated_data.get('conversation_id')

    try:
        conv_id, assistant_message, all_messages = chat_service.send_message(message, conversation_id)
        
        response_data = {
            'conversation_id': conv_id,
            'message': assistant_message,
            'messages': [
                {'role': msg.role, 'content': msg.content}
                for msg in all_messages
            ]
        }
        
        response_serializer = ChatResponseSerializer(data=response_data)
        response_serializer.is_valid()  # Validate but we already have valid data
        return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
    
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error processing message: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def conversations_list(request):
    """Get list of all conversations."""
    skip = int(request.query_params.get('skip', 0))
    limit = int(request.query_params.get('limit', 100))
    
    conversations = chat_service.get_all_conversations(skip=skip, limit=limit)
    serializer = ConversationSummarySerializer(conversations, many=True)
    
    return Response({
        'conversations': serializer.data,
        'total': len(conversations)
    })


@api_view(['GET'])
def conversation_detail(request, conversation_id):
    """Get conversation details with messages."""
    conversation = chat_service.get_conversation(conversation_id)
    if not conversation:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ConversationDetailSerializer(conversation)
    return Response(serializer.data)


@api_view(['DELETE'])
def conversation_delete(request, conversation_id):
    """Delete a conversation and all its messages."""
    success = chat_service.delete_conversation(conversation_id)
    if not success:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'message': 'Conversation deleted successfully'})


@api_view(['GET'])
def health_check(request):
    """Health check endpoint."""
    from django.conf import settings
    
    return Response({
        'status': 'healthy',
        'app_name': getattr(settings, 'APP_NAME', 'Shopify Community Chatbot'),
        'version': getattr(settings, 'APP_VERSION', '1.0.0'),
    })
