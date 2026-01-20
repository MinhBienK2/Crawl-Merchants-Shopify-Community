# Merchants Community Chatbot - Full Stack Application

A complete AI-powered chatbot system for answering questions about Shopify Community data. Built with Django REST API backend and Next.js frontend.

---

## 🎯 Project Overview

This full-stack application consists of three main components:

1. **Backend (BE/)** - Django REST API with OpenAI integration
2. **Frontend (FE/)** - Next.js chatbot interface
3. **Crawler (crawl-data/)** - Data collection system

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Browser                         │
│              Next.js Frontend (Port 3000)               │
│         React, TypeScript, Tailwind CSS                 │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ REST API
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Django Backend (Port 8000)                 │
│         Django REST Framework + OpenAI                  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           PostgreSQL Database + Vector DB               │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### Frontend
- 💬 Real-time chat interface
- 📝 Conversation management
- 🎨 Modern, responsive UI
- ⚡ Optimistic UI updates
- 📱 Mobile-friendly design
- 🎯 TypeScript for type safety

### Backend
- 🤖 OpenAI GPT-4 integration
- 📊 RAG (Retrieval-Augmented Generation)
- 🔍 Vector similarity search
- 💾 Conversation persistence
- 🔐 RESTful API
- 📈 Django admin interface

### Data Crawler
- 🕷️ Shopify Community forum scraper
- 💾 JSON data storage
- 📊 Thread and reply extraction

---

## 📂 Project Structure

```
merchants-community-crawl/
│
├── BE/                          # Backend (Django)
│   ├── chatbot/                # Main chatbot app
│   ├── config/                 # Django settings
│   ├── data/                   # Crawled data
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md               # Backend documentation
│   ├── QUICKSTART.md
│   └── REVIEW_REPORT.md
│
├── FE/                          # Frontend (Next.js)
│   ├── src/
│   │   ├── app/               # Next.js pages
│   │   ├── components/        # React components
│   │   ├── services/          # API integration
│   │   ├── hooks/             # Custom hooks
│   │   ├── types/             # TypeScript types
│   │   └── constants/         # Configuration
│   ├── package.json
│   ├── README.md               # Frontend documentation
│   ├── QUICKSTART.md
│   ├── INSTALLATION.md
│   ├── PROJECT_STRUCTURE.md
│   ├── REVIEW_REPORT.md
│   └── SUMMARY.md
│
├── crawl-data/                  # Data crawler
│   ├── src/                    # Crawler source
│   ├── config/                 # Configuration
│   ├── main.py
│   └── README.md
│
├── INTEGRATION_GUIDE.md         # Full system setup
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

**Backend:**
- Python 3.10+
- PostgreSQL
- OpenAI API key

**Frontend:**
- Node.js 18+
- npm/yarn/pnpm

### Installation

#### 1. Clone Repository
```bash
git clone <repository-url>
cd merchants-community-crawl
```

#### 2. Setup Backend
```bash
cd BE
uv sync                      # Install dependencies
cp env.example .env          # Create environment file
# Edit .env with your database and OpenAI key
make migrate                 # Run database migrations
make run                     # Start backend server
```

**Backend will run on: http://localhost:8000**

#### 3. Setup Frontend
```bash
cd FE
npm install                  # Install dependencies
cp env.example .env.local    # Create environment file
npm run dev                  # Start development server
```

**Frontend will run on: http://localhost:3000**

#### 4. Open Browser
Navigate to **http://localhost:3000** and start chatting!

---

## 📖 Documentation

### Quick Start Guides
- [Backend Quick Start](BE/QUICKSTART.md)
- [Frontend Quick Start](FE/QUICKSTART.md)
- [Full Integration Guide](INTEGRATION_GUIDE.md)

### Complete Documentation
- [Backend README](BE/README.md) - API endpoints, setup, architecture
- [Frontend README](FE/README.md) - Components, structure, customization
- [Frontend Installation](FE/INSTALLATION.md) - Detailed setup guide
- [Project Structure](FE/PROJECT_STRUCTURE.md) - Architecture diagrams

### Review Reports
- [Backend Review](BE/REVIEW_REPORT.md)
- [Frontend Review](FE/REVIEW_REPORT.md)
- [Frontend Summary](FE/SUMMARY.md)

---

## 🎨 Tech Stack

### Backend
- **Framework**: Django 4.x
- **API**: Django REST Framework
- **AI**: OpenAI GPT-4
- **Database**: PostgreSQL
- **Search**: Vector similarity search

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 3
- **HTTP**: Axios
- **Icons**: React Icons
- **Markdown**: React Markdown

### Data Crawler
- **Language**: Python 3.10+
- **HTTP**: Requests
- **Parsing**: BeautifulSoup4
- **Storage**: JSON

---

## 🔧 Configuration

### Backend Environment Variables
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True

# Database
DB_NAME=shopify_chatbot
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# OpenAI
OPENAI_API_KEY=sk-your-api-key

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend Environment Variables
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
NEXT_PUBLIC_APP_NAME=Merchants Community Chatbot
NEXT_PUBLIC_MAX_MESSAGE_LENGTH=2000
```

---

## 🔌 API Endpoints

### Chat
- `POST /api/v1/chat/` - Send message and get AI response

### Conversations
- `GET /api/v1/conversations/` - List all conversations
- `GET /api/v1/conversations/{id}/` - Get conversation details
- `DELETE /api/v1/conversations/{id}/delete/` - Delete conversation

### Health
- `GET /api/v1/health/` - Health check endpoint

---

## 🎯 Key Features

### Chat Functionality
- ✅ Send messages to AI
- ✅ Receive contextual responses
- ✅ Markdown formatting support
- ✅ Real-time updates
- ✅ Optimistic UI

### Conversation Management
- ✅ Create new conversations
- ✅ View conversation history
- ✅ Switch between conversations
- ✅ Delete conversations
- ✅ Auto-generated titles

### User Experience
- ✅ Responsive design
- ✅ Loading indicators
- ✅ Error handling
- ✅ Empty states
- ✅ Keyboard shortcuts
- ✅ Character counter

---

## 🧪 Testing

### Backend Testing
```bash
cd BE
python manage.py test
```

### Frontend Testing
```bash
cd FE
npm run type-check    # TypeScript checking
npm run lint          # ESLint
```

### Manual Testing
1. Send a message in new conversation
2. Create multiple conversations
3. Switch between conversations
4. Delete conversations
5. Test error handling
6. Test responsive design

---

## 🚀 Deployment

### Production Build

**Backend:**
```bash
cd BE
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

**Frontend:**
```bash
cd FE
npm run build
npm run start
```

### Environment Setup
- Set `DEBUG=False` in Django
- Use production database
- Configure proper CORS origins
- Set up SSL/HTTPS
- Use environment variables for secrets

---

## 📊 Performance

### Backend
- ⚡ Efficient database queries
- ⚡ Connection pooling
- ⚡ Vector search optimization
- ⚡ Response caching

### Frontend
- ⚡ Next.js optimization
- ⚡ Code splitting
- ⚡ Lazy loading
- ⚡ CSS purging

---

## 🐛 Troubleshooting

### Common Issues

**Cannot connect to backend:**
- Verify backend is running on port 8000
- Check CORS settings
- Verify .env.local in frontend

**Database connection error:**
- Ensure PostgreSQL is running
- Check database credentials
- Verify database exists

**OpenAI API error:**
- Check API key is valid
- Verify API quota
- Check internet connection

**Port already in use:**
- Kill process using the port
- Use alternative port

For detailed troubleshooting, see:
- [Backend Troubleshooting](BE/README.md#troubleshooting)
- [Frontend Troubleshooting](FE/INSTALLATION.md#troubleshooting)
- [Integration Guide](INTEGRATION_GUIDE.md#troubleshooting)

---

## 📈 Development Workflow

### Daily Development
```bash
# Terminal 1 - Backend
cd BE && make run

# Terminal 2 - Frontend
cd FE && npm run dev
```

### Making Changes

**Backend:**
1. Edit Python files in `BE/chatbot/`
2. Server auto-reloads
3. Test API endpoints
4. Check Django admin

**Frontend:**
1. Edit files in `FE/src/`
2. Browser auto-refreshes
3. Check browser console
4. Test UI interactions

---

## 🔮 Future Enhancements

### Potential Features
- 🔐 User authentication
- 🌐 WebSocket real-time updates
- 🔍 Advanced search
- 🎨 Dark mode
- 📤 Export conversations
- 📎 File attachments
- 🎤 Voice input
- 💬 Typing indicators
- 📊 Analytics dashboard
- 🌍 Internationalization

---

## 📝 Contributing

### Code Style
- Follow existing patterns
- Use TypeScript in frontend
- Follow PEP 8 in backend
- Write clear comments
- Add proper error handling

### Pull Request Process
1. Create feature branch
2. Make changes
3. Test thoroughly
4. Update documentation
5. Submit PR

---

## 📜 License

This project is part of the Data Impact merchants community analysis system.

---

## 🤝 Support

For issues or questions:

1. Check documentation in BE/ and FE/ folders
2. Review troubleshooting guides
3. Check browser/server logs
4. Contact development team

---

## 📞 Contact

For more information about this project, please contact the development team.

---

## ✅ Status

**Current Status**: ✅ **FULLY IMPLEMENTED & READY TO USE**

### Completed Components
- ✅ Backend API (Django REST Framework)
- ✅ Frontend UI (Next.js + TypeScript)
- ✅ Database models and migrations
- ✅ OpenAI integration
- ✅ Conversation management
- ✅ Responsive design
- ✅ Error handling
- ✅ Documentation

### Ready For
- ✅ Development
- ✅ Testing
- ✅ Staging deployment
- ✅ Production deployment

---

## 🎉 Getting Started Now

**New to the project? Start here:**

1. Read this README
2. Follow [Integration Guide](INTEGRATION_GUIDE.md)
3. Check [Backend Quick Start](BE/QUICKSTART.md)
4. Check [Frontend Quick Start](FE/QUICKSTART.md)
5. Start coding!

---

**Built with ❤️ using Django, Next.js, TypeScript, and OpenAI**

*Happy Coding! 🚀*
