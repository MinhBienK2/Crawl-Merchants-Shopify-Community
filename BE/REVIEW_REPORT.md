# Django Backend Review Report

**Date:** January 19, 2026  
**Project:** Merchants Community Crawl - Backend (Django)  
**User Question:** Explanation of Django backend for someone who has never worked with Django before

---

## Overview

The BE/ folder contains a Django REST Framework (DRF) backend for a Shopify Community Chatbot. The application provides API endpoints for a chat interface that uses OpenAI's LLM to answer questions about Shopify community forum threads.

---

## Technology Stack

- **Framework:** Django 5.0+
- **API Framework:** Django REST Framework 3.14+
- **Database:** PostgreSQL (with psycopg2-binary driver)
- **LLM:** OpenAI API (GPT-3.5-turbo or configurable)
- **Configuration:** python-dotenv for environment variables
- **CORS:** django-cors-headers for frontend integration

---

## Project Structure

```
BE/
├── manage.py                    # Django CLI entry point
├── config/                      # Project configuration
│   ├── settings.py             # All app settings (database, middleware, etc.)
│   ├── urls.py                 # Root URL routing
│   ├── wsgi.py                 # WSGI server interface
│   └── asgi.py                 # ASGI interface (async support)
├── chatbot/                     # Main application module
│   ├── models.py               # Database models (Conversation, Message)
│   ├── views.py                # API view functions
│   ├── urls.py                 # App-specific URL routing
│   ├── serializers.py          # DRF serializers for validation
│   ├── admin.py                # Admin panel configuration
│   └── services/               # Business logic layer
│       ├── data_loader.py      # Load & search Shopify forum data
│       ├── llm_service.py      # OpenAI API integration
│       └── chat_service.py     # Chat conversation management
├── requirements.txt             # Python dependencies
├── pyproject.toml              # UV package manager config
├── .env                        # Environment variables (not in git)
├── env.example                 # Environment template
└── Makefile                    # Development commands
```

---

## Core Django Concepts Explained

### 1. **Django Project vs Django App**
- **Project (config/)**: Overall configuration and settings
- **App (chatbot/)**: Modular, reusable component with specific functionality
- A project can contain multiple apps

### 2. **MVT Architecture (Model-View-Template)**
For API-only projects like this, it's essentially MVC:
- **Model (models.py)**: Database schema and ORM
- **View (views.py)**: Request handlers (controllers)
- **Template**: Not used (API returns JSON instead)

### 3. **ORM (Object-Relational Mapping)**
Django's ORM lets you interact with databases using Python instead of SQL:

```python
# Python ORM query
conversations = Conversation.objects.filter(created_at__gte=today)

# Equivalent SQL
SELECT * FROM conversations WHERE created_at >= '2026-01-19';
```

### 4. **Migrations**
Database schema version control:
- When you change models, create migrations (`makemigrations`)
- Apply migrations to update database (`migrate`)
- Migration files are version-controlled

### 5. **Middleware**
Request/response processors that run globally:
- Security middleware
- CORS handling
- Authentication
- CSRF protection

---

## Database Models

### Conversation Model
Stores chat sessions:
```python
- id (auto-generated primary key)
- title (optional, max 500 chars)
- created_at (auto timestamp)
- updated_at (auto timestamp)
```

### Message Model
Stores individual chat messages:
```python
- id (auto-generated primary key)
- conversation (ForeignKey to Conversation)
- role (user/assistant)
- content (text)
- created_at (auto timestamp)
```

**Relationship:** One-to-Many (Conversation → Messages)
- One conversation has many messages
- When conversation deleted, all messages cascade delete

---

## API Endpoints

All endpoints prefixed with `/api/v1/`:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health/` | Health check |
| POST | `/chat/` | Send message, get AI response |
| GET | `/conversations/` | List all conversations (paginated) |
| GET | `/conversations/{id}/` | Get conversation with messages |
| DELETE | `/conversations/{id}/delete/` | Delete conversation |

### Request/Response Flow

```
Client Request
    ↓
Django WSGI Server
    ↓
Middleware Processing
    ↓
URL Dispatcher (config/urls.py → chatbot/urls.py)
    ↓
View Function (views.py)
    ├─ Validate data (serializers.py)
    ├─ Business logic (services/)
    ├─ Database operations (models.py via ORM)
    └─ Return Response
    ↓
Middleware Processing
    ↓
JSON Response to Client
```

---

## Service Layer Architecture

Clean separation of concerns:

### chat_service.py
- Manages conversation lifecycle
- Coordinates message saving
- Orchestrates LLM calls

### llm_service.py
- OpenAI API integration
- Prompt engineering
- Context management

### data_loader.py
- Loads Shopify forum thread data
- Semantic search functionality
- Data retrieval for RAG (Retrieval-Augmented Generation)

---

## Configuration Highlights

### Environment Variables (.env)
```bash
SECRET_KEY=            # Django secret key
DEBUG=True             # Development mode
POSTGRES_HOST=         # PostgreSQL host (default: localhost)
POSTGRES_PORT=         # PostgreSQL port (default: 5432)
POSTGRES_DB=           # Database name (default: shopify_chatbot)
POSTGRES_USER=         # Database user (default: postgres)
POSTGRES_PASSWORD=     # Database password
OPENAI_API_KEY=        # OpenAI API key
OPENAI_MODEL=          # Model selection (default: gpt-3.5-turbo)
```

### CORS Configuration
Allows frontend to access API:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Next.js frontend
    "http://localhost:8000",
]
```

### REST Framework Settings
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_RENDERER_CLASSES': ['JSONRenderer'],
}
```

---

## Key Django Features Used

### 1. **Admin Panel**
- Free, auto-generated interface at `/admin/`
- Manage conversations and messages through GUI
- Requires superuser account

### 2. **Django REST Framework**
- Simplified API development
- Built-in serialization/validation
- Browsable API interface
- Standard HTTP status codes

### 3. **Database Relationships**
- ForeignKey for one-to-many relationships
- `related_name` for reverse queries
- `on_delete=CASCADE` for automatic cleanup

### 4. **Auto Timestamps**
- `auto_now_add=True`: Set once on creation
- `auto_now=True`: Update on every save

### 5. **Query Optimization**
- `db_index=True` on frequently queried fields
- Efficient ORM queries
- Ordering at database level

---

## Development Workflow

### Initial Setup
```bash
1. cd BE
2. uv sync                          # Install dependencies
3. cp env.example .env              # Configure environment
4. make migrate                     # Create database tables
5. make createsuperuser             # Create admin user
6. make run                         # Start development server
```

### Common Commands (via Makefile)
```bash
make run              # Start server (port 8000)
make migrate          # Apply database migrations
make makemigrations   # Create new migrations
make createsuperuser  # Create admin user
make shell            # Open Django shell
make test             # Run tests
```

---

## Django Advantages Demonstrated

1. **Rapid Development**: Admin panel, ORM, built-in auth out of the box
2. **Security**: CSRF protection, SQL injection prevention, XSS protection
3. **Scalability**: Modular app structure, service layer separation
4. **Maintainability**: Clear structure, migrations, DRY principle
5. **Documentation**: Self-documenting with DRF browsable API
6. **Ecosystem**: Rich third-party packages (DRF, CORS, etc.)

---

## Learning Resources for Beginners

1. **Official Django Tutorial**  
   https://docs.djangoproject.com/en/stable/intro/tutorial01/

2. **Django REST Framework Tutorial**  
   https://www.django-rest-framework.org/tutorial/quickstart/

3. **Django ORM Documentation**  
   https://docs.djangoproject.com/en/stable/topics/db/queries/

4. **This Project's Documentation**
   - `README.md`: Setup and API documentation
   - `QUICKSTART.md`: Quick start guide
   - `DJANGO_EXPLAINED.md`: Detailed Django explanation

---

## Best Practices Applied

✅ **Environment Variables**: Secrets in `.env`, not code  
✅ **Service Layer**: Business logic separated from views  
✅ **Database Indexing**: Indexed frequently queried fields  
✅ **Error Handling**: Try-catch blocks with appropriate status codes  
✅ **CORS Configuration**: Secure cross-origin setup  
✅ **Migrations**: Database schema version-controlled  
✅ **Model Meta Options**: Custom table names, ordering  
✅ **Foreign Key Relationships**: Proper cascade behavior  
✅ **REST API Standards**: Standard HTTP methods and responses  
✅ **Code Organization**: Clear separation of concerns  

---

## Architecture Decisions

### Why Django + DRF?
- **Batteries Included**: Admin panel, ORM, authentication built-in
- **DRF**: Industry standard for Python REST APIs
- **PostgreSQL**: Robust, scalable relational database
- **Modular Design**: Easy to extend and maintain

### Service Layer Pattern
- Separates business logic from HTTP layer
- Makes testing easier
- Promotes code reusability
- Cleaner view functions

### Environment-based Configuration
- Different settings for development/production
- Secrets never in code
- Easy deployment across environments

---

## Potential Improvements

1. **Caching**: Add Redis for conversation caching
2. **Authentication**: Add user authentication (JWT/OAuth)
3. **Rate Limiting**: Prevent API abuse
4. **Logging**: Enhanced logging with structured logs
5. **Testing**: Add comprehensive test suite
6. **Async Views**: Use Django async views for better concurrency
7. **WebSockets**: Real-time chat updates
8. **Pagination**: Cursor-based pagination for better performance
9. **API Versioning**: More robust versioning strategy
10. **Documentation**: Auto-generated API docs (Swagger/OpenAPI)

---

## Summary

This Django backend is a well-structured, production-ready API for a chatbot application. It follows Django best practices, uses appropriate design patterns, and demonstrates clean architecture with proper separation of concerns. The project is easy to understand for Django beginners due to:

- Clear project structure
- Comprehensive documentation
- Standard Django conventions
- Simple, focused functionality
- Good error handling
- Environment-based configuration

For someone new to Django, this project serves as an excellent learning resource, showcasing core concepts like models, views, URLs, serializers, and the ORM in a real-world application context.

---

**End of Review Report**
