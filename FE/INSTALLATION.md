# Installation & Setup Guide

Complete step-by-step guide to get the frontend running.

---

## Prerequisites

Before you begin, ensure you have:

- ✅ **Node.js** 18.x or higher ([Download](https://nodejs.org/))
- ✅ **npm** (comes with Node.js) or **yarn** or **pnpm**
- ✅ **Git** (for cloning the repository)
- ✅ **Backend API** running on port 8000

### Check Prerequisites

```bash
# Check Node.js version (should be 18+)
node --version

# Check npm version
npm --version

# Check if backend is running
curl http://localhost:8000/api/v1/health/
```

---

## Step 1: Navigate to Frontend Directory

```bash
cd FE
```

---

## Step 2: Install Dependencies

Choose your preferred package manager:

### Using npm (recommended)
```bash
npm install
```

### Using yarn
```bash
yarn install
```

### Using pnpm
```bash
pnpm install
```

**Expected Output:**
```
added 245 packages, and audited 246 packages in 15s
```

---

## Step 3: Configure Environment

### Option A: Copy from example
```bash
# On Windows
copy env.example .env.local

# On macOS/Linux
cp env.example .env.local
```

### Option B: Create manually

Create a file named `.env.local` in the `FE/` directory:

```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

# App Configuration
NEXT_PUBLIC_APP_NAME=Merchants Community Chatbot
NEXT_PUBLIC_MAX_MESSAGE_LENGTH=2000
```

### Important Notes:

- `NEXT_PUBLIC_API_BASE_URL`: Must match your backend URL
- All variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- Never commit `.env.local` to version control (it's in `.gitignore`)

---

## Step 4: Start Development Server

```bash
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 14.1.0
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Ready in 2.5s
```

---

## Step 5: Open in Browser

Navigate to: **http://localhost:3000**

You should see:
- ✅ Sidebar on the left
- ✅ "New Chat" button
- ✅ Chat interface in the center
- ✅ Welcome message

---

## Step 6: Test the Application

### Test 1: Send a Message
1. Click the "New Chat" button
2. Type a question: *"How do I set up shipping?"*
3. Press Enter or click the send button
4. Wait for AI response

### Test 2: View Conversations
1. Send a few messages
2. Check sidebar for conversation history
3. Click on a conversation to view it

### Test 3: Delete Conversation
1. Hover over a conversation in the sidebar
2. Click the trash icon
3. Confirm deletion

---

## Verification Checklist

After installation, verify:

- [ ] Development server starts without errors
- [ ] Page loads at http://localhost:3000
- [ ] No console errors in browser
- [ ] Can send a message
- [ ] Receives response from backend
- [ ] Conversations appear in sidebar
- [ ] Can delete conversations

---

## Troubleshooting

### Issue 1: Port 3000 Already in Use

**Error:**
```
Error: listen EADDRINUSE: address already in use :::3000
```

**Solution:**
```bash
# Use a different port
PORT=3001 npm run dev

# Or kill the process using port 3000
# On Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# On macOS/Linux
lsof -ti:3000 | xargs kill -9
```

---

### Issue 2: Module Not Found

**Error:**
```
Module not found: Can't resolve '@/components/...'
```

**Solution:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

### Issue 3: Cannot Connect to API

**Error in browser:**
```
Network error. Please check your connection.
```

**Solution:**
1. Verify backend is running:
   ```bash
   curl http://localhost:8000/api/v1/health/
   ```

2. Check `.env.local` has correct backend URL:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   ```

3. Check CORS settings in backend (Django settings):
   ```python
   CORS_ALLOWED_ORIGINS = [
       "http://localhost:3000",
   ]
   ```

4. Restart both servers:
   ```bash
   # Terminal 1 - Backend
   cd BE
   make run

   # Terminal 2 - Frontend
   cd FE
   npm run dev
   ```

---

### Issue 4: TypeScript Errors

**Error:**
```
Type error: Cannot find module '@/types' or its corresponding type declarations
```

**Solution:**
```bash
# Check TypeScript configuration
npm run type-check

# If errors persist, clean and rebuild
rm -rf .next
npm run dev
```

---

### Issue 5: Tailwind Styles Not Applied

**Error:**
Styles are not showing correctly

**Solution:**
1. Check `globals.css` has Tailwind imports:
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

2. Restart dev server:
   ```bash
   npm run dev
   ```

---

## Additional Commands

### Build for Production
```bash
npm run build
```

### Start Production Server
```bash
npm run start
```

### Run Linter
```bash
npm run lint
```

### Type Check
```bash
npm run type-check
```

### Clean Build
```bash
# Remove build artifacts
rm -rf .next
rm -rf out
rm -rf node_modules
npm install
```

---

## Using Makefile (Alternative)

If you prefer using Make:

```bash
# Install dependencies
make install

# Start development
make dev

# Build for production
make build

# Start production
make start

# Run linter
make lint

# Type check
make type-check

# Clean everything
make clean
```

---

## Development Workflow

### Daily Development
```bash
# 1. Start backend (Terminal 1)
cd BE
make run

# 2. Start frontend (Terminal 2)
cd FE
npm run dev

# 3. Open browser
# http://localhost:3000
```

### Before Committing
```bash
# Check for type errors
npm run type-check

# Check for lint errors
npm run lint

# Test production build
npm run build
```

---

## Environment-Specific Setup

### Development
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

### Staging
```env
NEXT_PUBLIC_API_BASE_URL=https://staging-api.example.com
```

### Production
```env
NEXT_PUBLIC_API_BASE_URL=https://api.example.com
```

---

## Docker Setup (Optional)

Create `Dockerfile` in `FE/`:

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t chatbot-frontend .
docker run -p 3000:3000 chatbot-frontend
```

---

## Performance Tips

1. **Use Production Build**
   ```bash
   npm run build
   npm run start
   ```

2. **Enable Compression** (add to `next.config.js`):
   ```js
   module.exports = {
     compress: true,
   }
   ```

3. **Optimize Images** (use Next.js Image component):
   ```tsx
   import Image from 'next/image'
   ```

---

## Next Steps

After successful installation:

1. ✅ Read [README.md](README.md) for detailed documentation
2. ✅ Check [QUICKSTART.md](QUICKSTART.md) for quick tips
3. ✅ Review [REVIEW_REPORT.md](REVIEW_REPORT.md) for implementation details
4. ✅ Explore [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for architecture

---

## Getting Help

If you encounter issues not covered here:

1. Check the browser console for errors
2. Check the terminal for server errors
3. Review the backend logs
4. Verify environment variables
5. Check network requests in browser DevTools

---

## Success! 🎉

You should now have a fully functional chatbot frontend running. Start chatting and exploring the Shopify Community data!

**Happy Coding!** 🚀
