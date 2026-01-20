# Quick Start Guide

## 1. Setup Environment

```bash
# Navigate to BE directory
cd BE

# Copy environment file
cp env.example .env

# Edit .env file and configure:
# - SECRET_KEY=your-secret-key-here
# - POSTGRES_HOST=localhost
# - POSTGRES_PORT=5432
# - POSTGRES_DB=shopify_chatbot
# - POSTGRES_USER=postgres
# - POSTGRES_PASSWORD=your_password
# - OPENAI_API_KEY=your_openai_api_key_here
```

## 2. Setup PostgreSQL

```bash
# Create database
createdb shopify_chatbot

# Or using psql:
psql -U postgres
CREATE DATABASE shopify_chatbot;
```

## 3. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## 4. Run Migrations

```bash
# Create migrations
make makemigrations

# Apply migrations
make migrate
```

## 5. Create Superuser (Optional - for admin panel)

```bash
make createsuperuser
```

## 6. Run Application

```bash
# Using Makefile
make run

# Or directly
uv run python manage.py runserver
```

The API will be available at: http://localhost:8000

Admin panel: http://localhost:8000/admin/

## 7. Test the API

### Using curl

```bash
# Health check
curl http://localhost:8000/api/v1/health/

# Send a chat message
curl -X POST http://localhost:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "How to set up free shipping for specific products?"}'

# Get conversations
curl http://localhost:8000/api/v1/conversations/

# Get conversation details
curl http://localhost:8000/api/v1/conversations/1/

# Delete conversation
curl -X DELETE http://localhost:8000/api/v1/conversations/1/delete/
```

## 8. Example Chat Flow

1. **First message** (creates new conversation):
```json
POST /api/v1/chat/
{
  "message": "Tell me about discount settings in Shopify"
}
```

Response:
```json
{
  "conversation_id": 1,
  "message": "Based on the Shopify Community threads...",
  "messages": [
    {"role": "user", "content": "Tell me about discount settings in Shopify"},
    {"role": "assistant", "content": "Based on the Shopify Community threads..."}
  ]
}
```

2. **Continue conversation**:
```json
POST /api/v1/chat/
{
  "message": "Can you give me more details?",
  "conversation_id": 1
}
```

3. **Get conversation history**:
```json
GET /api/v1/conversations/1/
```

## Troubleshooting

### Database connection error
- Check PostgreSQL is running
- Verify DATABASE_URL or DB_* variables in .env file
- Ensure database exists

### Migration errors
- Make sure to run `makemigrations` before `migrate`
- Check database permissions

### OpenAI API error
- Verify OPENAI_API_KEY in .env file
- Check API key is valid and has credits

### Import errors
- Ensure all dependencies are installed: `uv sync`
- Check Python version >= 3.10

### Secret key warning
- Generate a new secret key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Add it to .env file as SECRET_KEY
