# Quick Start Guide - Frontend

Get the chatbot frontend up and running in 5 minutes!

## Prerequisites

✅ Node.js 18+ installed
✅ Backend API running at http://localhost:8000

## Step 1: Install Dependencies

```bash
cd FE
npm install
```

## Step 2: Configure Environment

Copy the environment example:

```bash
cp env.example .env.local
```

The default configuration should work if your backend is on port 8000:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
```

## Step 3: Start Development Server

```bash
npm run dev
```

## Step 4: Open in Browser

Navigate to: **http://localhost:3000**

## What You'll See

1. **Sidebar** - Shows conversation history
2. **Chat Area** - Main conversation interface
3. **New Chat Button** - Start a new conversation
4. **Message Input** - Type your questions here

## Try It Out

1. Click **"New Chat"** button
2. Type a question like: *"How do I set up shipping?"*
3. Press **Enter** to send
4. Watch the AI respond with relevant information

## Common Commands

```bash
# Development
npm run dev

# Production build
npm run build
npm run start

# Type checking
npm run type-check

# Linting
npm run lint
```

## Troubleshooting

### Cannot connect to API

**Problem**: Error messages about network connection

**Solution**: 
1. Make sure backend is running: `cd BE && make run`
2. Check backend URL in `.env.local`

### Port 3000 already in use

**Solution**: Use a different port
```bash
PORT=3001 npm run dev
```

### Missing dependencies

**Solution**: Clean install
```bash
rm -rf node_modules package-lock.json
npm install
```

## Keyboard Shortcuts

- **Enter** - Send message
- **Shift + Enter** - New line in message

## Features to Try

✨ Send multiple messages in a conversation
✨ Create multiple conversations
✨ Delete old conversations
✨ View conversation history
✨ Test markdown formatting in responses

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Explore the codebase structure
- Customize the UI in `src/constants/`
- Add new features in `src/components/`

## Need Help?

Check the full documentation in README.md or contact the development team.

Happy chatting! 🚀
