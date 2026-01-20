"""URLs for chatbot API."""
from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('health/', views.health_check, name='health'),
    path('chat/', views.chat, name='chat'),
    path('conversations/', views.conversations_list, name='conversations-list'),
    path('conversations/<int:conversation_id>/', views.conversation_detail, name='conversation-detail'),
    path('conversations/<int:conversation_id>/delete/', views.conversation_delete, name='conversation-delete'),
]
