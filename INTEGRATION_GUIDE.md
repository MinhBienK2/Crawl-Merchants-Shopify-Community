# Full Stack Integration Guide

Complete guide to run both Backend (Django) and Frontend (Next.js) together.

---

## 🎯 Overview

This system consists of:
- **Backend**: Django REST API (Port 8000)
- **Frontend**: Next.js Application (Port 3000)

---

## 📋 Prerequisites

Ensure you have:

### Backend Requirements
- ✅ Python 3.10+
- ✅ uv (Python package manager)
- ✅ PostgreSQL database
- ✅ OpenAI API key

### Frontend Requirements
- ✅ Node.js 18+
- ✅ npm/yarn/pnpm

---

## 🚀 Quick Start (Both Services)

### Option 1: Using Two Terminals (Recommended)

**Terminal 1 - Backend:**
```bash
cd BE
uv sync
cp env.example .env
# Edit .env with your database and OpenAI key
make migrate
make run
```

**Terminal 2 - Frontend:**
```bash
cd FE
npm install
cp env.example .env.local
npm run dev
```

**Open Browser:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/admin/

---

### Option 2: Using Makefile (If Available)

Create a `Makefile` in the root directory:

```makefile
.PHONY: help install-all run-all stop-all

help:
	@echo "Available commands:"
	@echo "  make install-all  - Install both backend and frontend"
	@echo "  make run-all      - Run both services"
	@echo "  make stop-all     - Stop all services"

install-all:
	@echo "Installing backend..."
	cd BE && uv sync
	@echo "Installing frontend..."
	cd FE && npm install

run-all:
	@echo "Starting backend and frontend..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	cd BE && make run & cd FE && npm run dev
```

Then run:
```bash
make install-all
make run-all
```

---

## 📝 Detailed Setup

### Step 1: Setup Backend

```bash
# Navigate to backend
cd BE

# Install dependencies
uv sync

# Create environment file
cp env.example .env

# Edit .env file with your settings
# Required: DATABASE_URL, OPENAI_API_KEY, SECRET_KEY
```

**Example .env for Backend:**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DB_NAME=shopify_chatbot
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

```bash
# Create database (PostgreSQL)
createdb shopify_chatbot

# Run migrations
make migrate

# (Optional) Create superuser for admin
make createsuperuser

# Start backend server
make run
```

**Backend should now be running at: http://localhost:8000**

---

### Step 2: Setup Frontend

```bash
# Navigate to frontend
cd FE

# Install dependencies
npm install

# Create environment file
cp env.example .env.local
```

**Example .env.local for Frontend:**
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
NEXT_PUBLIC_APP_NAME=Merchants Community Chatbot
NEXT_PUBLIC_MAX_MESSAGE_LENGTH=2000
```

```bash
# Start frontend server
npm run dev
```

**Frontend should now be running at: http://localhost:3000**

---

## 🔍 Verify Installation

### 1. Check Backend Health
```bash
curl http://localhost:8000/api/v1/health/
```

**Expected Response:**
```json
{
  "status": "ok"
}
```

### 2. Check Frontend
Open browser: http://localhost:3000

You should see:
- ✅ Sidebar with "New Chat" button
- ✅ Chat interface
- ✅ No console errors

### 3. Test Integration
1. Click "New Chat"
2. Type a message: "Hello, how do I set up shipping?"
3. Press Enter
4. Wait for AI response

**Success Indicators:**
- ✅ Message appears immediately (optimistic update)
- ✅ Loading indicator shows
- ✅ AI response appears in a few seconds
- ✅ Conversation appears in sidebar

---

## 🔧 Configuration Details

### Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health/` | GET | Health check |
| `/api/v1/chat/` | POST | Send message |
| `/api/v1/conversations/` | GET | List conversations |
| `/api/v1/conversations/{id}/` | GET | Get conversation |
| `/api/v1/conversations/{id}/delete/` | DELETE | Delete conversation |
| `/admin/` | GET | Django admin panel |

### CORS Configuration

Ensure backend allows frontend origin:

**BE/config/settings.py:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

## 🐛 Troubleshooting

### Issue 1: Cannot Connect to Backend

**Symptoms:**
- Frontend shows "Network error"
- Console error: "Failed to fetch"

**Solutions:**

1. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/api/v1/health/
   ```

2. **Check CORS settings in backend:**
   ```python
   # BE/config/settings.py
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
   ]
   ```

3. **Verify frontend .env.local:**
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

4. **Restart both servers:**
   ```bash
   # Kill and restart backend
   cd BE && make run

   # Kill and restart frontend
   cd FE && npm run dev
   ```

---

### Issue 2: Database Connection Error

**Symptoms:**
- Backend crashes on startup
- Error: "connection to server failed"

**Solutions:**

1. **Verify PostgreSQL is running:**
   ```bash
   # On macOS
   brew services list | grep postgresql

   # On Linux
   sudo systemctl status postgresql

   # On Windows
   # Check Services app for PostgreSQL
   ```

2. **Check database exists:**
   ```bash
   psql -l | grep shopify_chatbot
   ```

3. **Verify .env settings:**
   ```env
   DB_NAME=shopify_chatbot
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. **Create database if missing:**
   ```bash
   createdb shopify_chatbot
   cd BE && make migrate
   ```

---

### Issue 3: OpenAI API Error

**Symptoms:**
- Messages send but no AI response
- Backend logs show API error

**Solutions:**

1. **Verify API key is set:**
   ```bash
   # Check .env
   cat BE/.env | grep OPENAI_API_KEY
   ```

2. **Test API key:**
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

3. **Check API quota:**
   - Visit: https://platform.openai.com/usage
   - Ensure you have credits

---

### Issue 4: Port Already in Use

**Backend (Port 8000):**
```bash
# Find process
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)

# Or use different port
cd BE && python manage.py runserver 8001
```

**Frontend (Port 3000):**
```bash
# Use different port
cd FE && PORT=3001 npm run dev
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Browser                      │
│               http://localhost:3000                 │
└────────────────────┬────────────────────────────────┘
                     │
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────┐
│              Next.js Frontend (Port 3000)           │
│  ┌─────────────────────────────────────────────┐   │
│  │  - React Components                         │   │
│  │  - State Management (useChat hook)          │   │
│  │  - API Service Layer                        │   │
│  └─────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────┘
                     │
                     │ REST API Calls
                     │ POST /api/v1/chat/
                     │ GET /api/v1/conversations/
                     ▼
┌─────────────────────────────────────────────────────┐
│           Django Backend (Port 8000)                │
│  ┌─────────────────────────────────────────────┐   │
│  │  - REST API Endpoints                       │   │
│  │  - Chat Service                             │   │
│  │  - LLM Service (OpenAI)                     │   │
│  │  - Data Loader                              │   │
│  └─────────────────────────────────────────────┘   │
└────────────┬──────────────────────┬─────────────────┘
             │                      │
             │                      │ API Calls
             │                      ▼
             │         ┌────────────────────────┐
             │         │   OpenAI API           │
             │         │   (GPT-4)              │
             │         └────────────────────────┘
             │
             │ Database Queries
             ▼
┌─────────────────────────────────────────────────────┐
│            PostgreSQL Database                      │
│  ┌─────────────────────────────────────────────┐   │
│  │  - Conversations                            │   │
│  │  - Messages                                 │   │
│  │  - User Data                                │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

```
1. User types message in frontend
        ↓
2. Frontend sends POST to /api/v1/chat/
        ↓
3. Backend receives request
        ↓
4. Backend queries Shopify data
        ↓
5. Backend calls OpenAI API
        ↓
6. Backend saves message to database
        ↓
7. Backend returns response
        ↓
8. Frontend updates UI
        ↓
9. User sees AI response
```

---

## 📈 Performance Tips

### Backend
- Use production WSGI server (gunicorn)
- Enable database connection pooling
- Cache frequently accessed data
- Optimize database queries

### Frontend
- Use production build (`npm run build`)
- Enable compression
- Optimize images
- Implement lazy loading

---

## 🚀 Production Deployment

### Backend (Django)
```bash
# Install production dependencies
pip install gunicorn

# Collect static files
python manage.py collectstatic

# Run with gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (Next.js)
```bash
# Build for production
npm run build

# Start production server
npm run start
```

### Environment Variables (Production)
- Update API URLs to production domains
- Set DEBUG=False in Django
- Use production database
- Configure proper CORS origins
- Set up SSL/HTTPS

---

## 📝 Development Workflow

### Daily Development
```bash
# Terminal 1 - Backend
cd BE
source venv/bin/activate  # or activate virtual env
make run

# Terminal 2 - Frontend
cd FE
npm run dev

# Terminal 3 - Database (if needed)
psql shopify_chatbot
```

### Making Changes

**Backend Changes:**
1. Edit Python files
2. Server auto-reloads (Django DEBUG=True)
3. Test API endpoints
4. Check Django admin

**Frontend Changes:**
1. Edit React/TypeScript files
2. Browser auto-refreshes (Next.js Fast Refresh)
3. Check browser console
4. Test UI interactions

---

## ✅ Success Checklist

After setup, verify:

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database connected
- [ ] OpenAI API working
- [ ] Can send messages
- [ ] Can receive AI responses
- [ ] Conversations saved in database
- [ ] Can view conversation history
- [ ] Can delete conversations
- [ ] No console errors
- [ ] Responsive design works

---

## 🎉 All Done!

You now have a fully functional chatbot system running!

### Test It:
1. Open http://localhost:3000
2. Click "New Chat"
3. Ask: "How do I set up free shipping on Shopify?"
4. Enjoy the AI-powered responses!

### Next Steps:
- Explore the Django admin: http://localhost:8000/admin/
- Read the API docs in BE/README.md
- Customize the UI in FE/src/components/
- Add your own features!

---

**Happy Development! 🚀**

*Need help? Check the documentation in both BE/ and FE/ folders.*
