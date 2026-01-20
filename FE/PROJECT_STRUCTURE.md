# Project Structure Diagram

## Visual Directory Tree

```
FE/
│
├── 📋 Configuration Files
│   ├── package.json                 # Dependencies & scripts
│   ├── tsconfig.json                # TypeScript configuration
│   ├── tailwind.config.ts           # Tailwind CSS configuration
│   ├── next.config.js               # Next.js configuration
│   ├── postcss.config.js            # PostCSS configuration
│   ├── .eslintrc.json               # ESLint rules
│   ├── .gitignore                   # Git ignore patterns
│   ├── env.example                  # Environment variables template
│   └── Makefile                     # Make commands
│
├── 📚 Documentation
│   ├── README.md                    # Full project documentation
│   ├── QUICKSTART.md                # Quick start guide
│   ├── REVIEW_REPORT.md             # Implementation review
│   └── PROJECT_STRUCTURE.md         # This file
│
└── 📁 src/                          # Source code
    │
    ├── 📱 app/                      # Next.js App Router
    │   ├── layout.tsx               # Root layout component
    │   ├── page.tsx                 # Home page (main chat interface)
    │   └── globals.css              # Global styles & Tailwind imports
    │
    ├── 🎨 components/               # React UI Components
    │   │
    │   ├── chat/                    # Chat-related components
    │   │   ├── MessageBubble.tsx    # Single message display
    │   │   ├── MessageList.tsx      # Message list container
    │   │   ├── ChatInput.tsx        # Message input field
    │   │   └── index.ts             # Component exports
    │   │
    │   ├── sidebar/                 # Sidebar components
    │   │   ├── Sidebar.tsx          # Main sidebar container
    │   │   ├── ConversationList.tsx # Conversation list
    │   │   ├── ConversationItem.tsx # Single conversation item
    │   │   └── index.ts             # Component exports
    │   │
    │   └── index.ts                 # All components export
    │
    ├── 🔧 services/                 # API & Business Logic
    │   ├── api.ts                   # Base HTTP client (Axios)
    │   ├── chatService.ts           # Chat API methods
    │   └── index.ts                 # Service exports
    │
    ├── 🪝 hooks/                    # Custom React Hooks
    │   ├── useChat.ts               # Main chat state management
    │   └── index.ts                 # Hook exports
    │
    ├── 📝 types/                    # TypeScript Type Definitions
    │   └── index.ts                 # All type definitions
    │
    └── 🎯 constants/                # Configuration Constants
        ├── config.ts                # App & API configuration
        ├── messages.ts              # UI messages & labels
        └── index.ts                 # Constants exports
```

## Component Hierarchy

```
App (page.tsx)
│
├── Sidebar
│   ├── Header
│   │   ├── App Title
│   │   └── New Chat Button
│   │
│   ├── ConversationList
│   │   └── ConversationItem (multiple)
│   │       ├── Icon
│   │       ├── Title
│   │       ├── Timestamp
│   │       └── Delete Button
│   │
│   └── Footer
│
└── Main Chat Area
    ├── Error Banner (conditional)
    │
    ├── MessageList
    │   └── MessageBubble (multiple)
    │       ├── Avatar
    │       ├── Content (with markdown)
    │       └── Timestamp
    │
    └── ChatInput
        ├── Textarea
        ├── Character Counter
        └── Send Button
```

## Data Flow

```
┌─────────────────────────────────────────────────────────┐
│                      User Action                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Component Event                        │
│  (onClick, onChange, onSubmit)                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                useChat Hook Method                      │
│  (sendMessage, deleteConversation, etc.)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                 chatService Method                      │
│  (API call with proper error handling)                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   api.ts (Axios)                        │
│  (HTTP request with interceptors)                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Backend API (Django)                       │
│  POST /api/v1/chat/, GET /api/v1/conversations/        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  API Response                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Update React State                         │
│  (useState in useChat hook)                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              React Re-render                            │
│  (UI updates automatically)                            │
└─────────────────────────────────────────────────────────┘
```

## State Management Flow

```
useChat Hook
│
├── State Variables
│   ├── conversations: Conversation[]
│   ├── activeConversationId: number | null
│   ├── messages: Message[]
│   ├── isLoadingConversations: boolean
│   ├── isLoadingMessages: boolean
│   ├── isSending: boolean
│   └── error: string | null
│
├── Methods
│   ├── loadConversations()
│   ├── loadMessages(id)
│   ├── sendMessage(content)
│   ├── deleteConversation(id)
│   ├── startNewChat()
│   └── setActiveConversationId(id)
│
└── Effects
    ├── Load conversations on mount
    └── Load messages when active conversation changes
```

## File Relationships

```
page.tsx
  │
  ├── imports useChat from hooks/useChat.ts
  ├── imports Sidebar from components/sidebar
  ├── imports MessageList from components/chat
  └── imports ChatInput from components/chat

useChat.ts
  │
  └── imports chatService from services/chatService.ts

chatService.ts
  │
  ├── imports apiService from services/api.ts
  ├── imports API_ENDPOINTS from constants/config.ts
  └── imports types from types/index.ts

MessageBubble.tsx
  │
  ├── imports Message type from types/index.ts
  ├── imports date-fns for formatting
  └── imports react-markdown for rendering

ChatInput.tsx
  │
  ├── imports APP_CONFIG from constants/config.ts
  └── imports UI_MESSAGES from constants/messages.ts
```

## API Endpoints Mapping

```
Frontend Service          Backend Endpoint
─────────────────────────────────────────────────────────
chatService.sendMessage() → POST   /api/v1/chat/
chatService.getConversations() → GET    /api/v1/conversations/
chatService.getConversationDetail() → GET    /api/v1/conversations/{id}/
chatService.deleteConversation() → DELETE /api/v1/conversations/{id}/delete/
chatService.healthCheck() → GET    /api/v1/health/
```

## Constants Organization

```
constants/
│
├── config.ts
│   ├── API_CONFIG
│   │   ├── BASE_URL
│   │   ├── VERSION
│   │   └── TIMEOUT
│   │
│   ├── APP_CONFIG
│   │   ├── NAME
│   │   ├── MAX_MESSAGE_LENGTH
│   │   ├── MESSAGES_PER_PAGE
│   │   └── CONVERSATIONS_PER_PAGE
│   │
│   ├── UI_CONFIG
│   │   ├── SIDEBAR_WIDTH
│   │   ├── ANIMATION_DURATION
│   │   └── DEBOUNCE_DELAY
│   │
│   ├── MESSAGE_ROLES
│   │   ├── USER
│   │   ├── ASSISTANT
│   │   └── SYSTEM
│   │
│   └── API_ENDPOINTS
│       ├── HEALTH
│       ├── CHAT
│       ├── CONVERSATIONS
│       ├── CONVERSATION_DETAIL(id)
│       └── CONVERSATION_DELETE(id)
│
└── messages.ts
    ├── UI_MESSAGES
    │   ├── Welcome messages
    │   ├── Error messages
    │   ├── Success messages
    │   └── Loading messages
    │
    └── PLACEHOLDERS
        ├── Search placeholder
        └── Input placeholder
```

## TypeScript Types Structure

```
types/index.ts
│
├── Message
│   ├── id: number
│   ├── conversation_id: number
│   ├── role: 'user' | 'assistant' | 'system'
│   ├── content: string
│   └── created_at: string
│
├── Conversation
│   ├── id: number
│   ├── title: string
│   ├── created_at: string
│   ├── updated_at: string
│   ├── messages?: Message[]
│   └── message_count?: number
│
├── ChatRequest
│   ├── message: string
│   └── conversation_id?: number
│
├── ChatResponse
│   ├── conversation_id: number
│   ├── message: Message
│   └── conversation?: Conversation
│
├── ConversationsResponse
│   ├── conversations: Conversation[]
│   ├── total: number
│   ├── skip: number
│   └── limit: number
│
├── ApiError
│   ├── detail?: string
│   ├── message?: string
│   └── error?: string
│
├── ApiResponse<T>
│   ├── data?: T
│   ├── error?: ApiError
│   └── status: number
│
└── LoadingState
    ├── isLoading: boolean
    └── error?: string | null
```

## Environment Variables Flow

```
.env.local
    │
    ├── NEXT_PUBLIC_API_BASE_URL
    ├── NEXT_PUBLIC_API_VERSION
    ├── NEXT_PUBLIC_APP_NAME
    └── NEXT_PUBLIC_MAX_MESSAGE_LENGTH
    │
    ▼
process.env.NEXT_PUBLIC_*
    │
    ▼
constants/config.ts
    │
    ├── API_CONFIG
    └── APP_CONFIG
    │
    ▼
Used throughout the application
```

## Build & Deployment Flow

```
Source Code (TypeScript + React)
    │
    ├── npm run dev (Development)
    │   └── Next.js Dev Server (Hot Reload)
    │
    └── npm run build (Production)
        │
        ├── TypeScript Compilation
        ├── Tailwind CSS Processing
        ├── Next.js Optimization
        └── Static File Generation
        │
        ▼
    .next/ folder (Build Output)
        │
        ▼
    npm run start (Production Server)
        │
        ▼
    Deployed Application
```

---

This structure ensures:
- 🎯 Clear separation of concerns
- 📦 Modular, reusable components
- 🔧 Easy configuration management
- 🛡️ Type safety throughout
- 📚 Comprehensive documentation
- 🚀 Scalable architecture
