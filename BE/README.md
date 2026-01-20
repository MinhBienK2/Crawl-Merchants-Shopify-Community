# Shopify Community Chatbot Backend (Django)

Django REST Framework backend for chatbot that answers questions about Shopify Community forum threads.

## Setup

### 1. Install dependencies using uv

```bash
cd BE
uv sync
```

### 2. Setup PostgreSQL Database

Create a PostgreSQL database:

```sql
CREATE DATABASE shopify_chatbot;
```

### 3. Configure Environment Variables

Copy `env.example` to `.env` and update the values:

```bash
cp env.example .env
```

Update the following in `.env`:
- `SECRET_KEY`: Django secret key (generate a new one)
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`: PostgreSQL connection details
- `OPENAI_API_KEY`: Your OpenAI API key

### 4. Run Migrations

```bash
# Create migrations
make makemigrations

# Apply migrations
make migrate
```

Or directly:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

## Running the Application

### Development

```bash
make run
# or
uv run python manage.py runserver
```

### Create Superuser (for Django Admin)

```bash
make createsuperuser
# or
uv run python manage.py createsuperuser
```

## API Endpoints

### Health Check
- `GET /api/v1/health/` - Health check

### Chat
- `POST /api/v1/chat/` - Send a message and get AI response
  ```json
  {
    "message": "Your question here",
    "conversation_id": 1  // optional, for continuing conversation
  }
  ```

### Conversations
- `GET /api/v1/conversations/` - Get list of conversations
  - Query params: `skip`, `limit`
- `GET /api/v1/conversations/{id}/` - Get conversation details with messages
- `DELETE /api/v1/conversations/{id}/delete/` - Delete a conversation

## Project Structure

```
BE/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings with .env integration
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI config
│
├── chatbot/               # Main chatbot application
│   ├── models.py          # Conversation and Message models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   ├── urls.py            # App URLs
│   ├── admin.py           # Django admin configuration
│   └── services/          # Business logic
│       ├── data_loader.py    # Load & search Shopify data
│       ├── llm_service.py    # OpenAI LLM integration
│       └── chat_service.py   # Chat conversation management
│
├── data/                  # Data files
│   └── shopify_community_threads.json
│
├── manage.py              # Django management script
├── pyproject.toml         # uv dependencies
└── .env                   # Environment variables
```

## Admin Panel

Access Django admin at: http://localhost:8000/admin/

You can manage conversations and messages through the admin interface after creating a superuser.

## Example API Usage

### Send a chat message

```bash
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "How to set up free shipping?"}'
```

### Get conversations

```bash
curl http://localhost:8000/api/v1/conversations/
```

### Get conversation details

```bash
curl http://localhost:8000/api/v1/conversations/1/
```

## Database Schema

- **Conversation**: Stores chat sessions
  - id, title, created_at, updated_at
  
- **Message**: Stores individual messages
  - id, conversation_id, role (user/assistant), content, created_at

## Notes

- All environment variables are loaded from `.env` file
- Database configuration supports both individual DB_* variables and DATABASE_URL
- CORS is enabled for local development (adjust in production)
- OpenAI integration requires valid API key
