# Merchants Community Chatbot - Frontend

A modern, responsive chatbot interface built with Next.js 14, TypeScript, and Tailwind CSS. This frontend application integrates with the Django REST API backend to provide an interactive chat experience for querying Shopify Community data.

## Features

- ✨ Modern chatbot interface with real-time messaging
- 💬 Conversation management (create, view, delete)
- 📱 Responsive design with mobile support
- 🎨 Beautiful UI with Tailwind CSS
- ⚡ Fast and optimized with Next.js 14
- 📝 Markdown support for AI responses
- 🔄 Optimistic UI updates
- 🎯 TypeScript for type safety
- 🏗️ Clean, modular architecture

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: React Icons
- **Markdown**: React Markdown
- **Date Formatting**: date-fns

## Project Structure

```
FE/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page (main chat)
│   │   └── globals.css        # Global styles
│   │
│   ├── components/            # React components
│   │   ├── chat/              # Chat-related components
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── index.ts
│   │   └── sidebar/           # Sidebar components
│   │       ├── Sidebar.tsx
│   │       ├── ConversationList.tsx
│   │       ├── ConversationItem.tsx
│   │       └── index.ts
│   │
│   ├── services/              # API and business logic
│   │   ├── api.ts            # Base HTTP client
│   │   ├── chatService.ts    # Chat API methods
│   │   └── index.ts
│   │
│   ├── hooks/                 # Custom React hooks
│   │   ├── useChat.ts        # Chat state management
│   │   └── index.ts
│   │
│   ├── types/                 # TypeScript definitions
│   │   └── index.ts
│   │
│   └── constants/             # Configuration constants
│       ├── config.ts          # App configuration
│       ├── messages.ts        # UI messages
│       └── index.ts
│
├── public/                    # Static assets
├── package.json              # Dependencies
├── tsconfig.json             # TypeScript config
├── tailwind.config.ts        # Tailwind config
├── next.config.js            # Next.js config
├── .env.local                # Environment variables
└── README.md                 # This file
```

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm, yarn, or pnpm
- Backend API running on http://localhost:8000

### Installation

1. Navigate to the FE directory:

```bash
cd FE
```

2. Install dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
```

3. Configure environment variables:

```bash
cp env.example .env.local
```

Edit `.env.local` and update the values:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1
NEXT_PUBLIC_APP_NAME=Merchants Community Chatbot
NEXT_PUBLIC_MAX_MESSAGE_LENGTH=2000
```

### Development

Run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm run start
```

### Type Checking

```bash
npm run type-check
```

### Linting

```bash
npm run lint
```

## Architecture Overview

### Component Structure

The application follows a modular component structure:

- **Chat Components**: Handle message display and input
- **Sidebar Components**: Manage conversation list and navigation
- **Hooks**: Custom React hooks for state management
- **Services**: API integration layer
- **Constants**: Centralized configuration

### State Management

The application uses React hooks for state management:

- `useChat`: Main hook managing chat state and operations
- Local component state for UI interactions

### API Integration

All API calls go through a centralized service layer:

- `api.ts`: Base HTTP client with interceptors
- `chatService.ts`: Chat-specific API methods

### Type Safety

TypeScript interfaces ensure type safety across the application:

- `Message`: Chat message structure
- `Conversation`: Conversation structure
- `ChatRequest/Response`: API request/response types

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_BASE_URL` | Backend API base URL | `http://localhost:8000` |
| `NEXT_PUBLIC_API_VERSION` | API version | `v1` |
| `NEXT_PUBLIC_APP_NAME` | Application name | `Merchants Community Chatbot` |
| `NEXT_PUBLIC_MAX_MESSAGE_LENGTH` | Max message length | `2000` |

## API Endpoints Used

The frontend integrates with these backend endpoints:

- `POST /api/v1/chat/` - Send chat message
- `GET /api/v1/conversations/` - List conversations
- `GET /api/v1/conversations/{id}/` - Get conversation details
- `DELETE /api/v1/conversations/{id}/delete/` - Delete conversation
- `GET /api/v1/health/` - Health check

## Features in Detail

### Chat Interface

- Real-time message display
- User and assistant message bubbles
- Markdown rendering for AI responses
- Auto-scroll to latest message
- Loading indicators
- Error handling

### Conversation Management

- Create new conversations
- View conversation history
- Delete conversations with confirmation
- Active conversation highlighting
- Time-ago timestamps

### User Experience

- Optimistic UI updates
- Error boundaries
- Loading states
- Responsive design
- Keyboard shortcuts (Enter to send, Shift+Enter for newline)
- Character counter
- Input validation

## Customization

### Styling

Modify `tailwind.config.ts` to customize colors and theme:

```typescript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      },
    },
  },
}
```

### Constants

Update `src/constants/config.ts` for app-wide settings:

```typescript
export const APP_CONFIG = {
  NAME: 'Your App Name',
  MAX_MESSAGE_LENGTH: 2000,
  // ...
};
```

### UI Messages

Modify `src/constants/messages.ts` to customize text:

```typescript
export const UI_MESSAGES = {
  WELCOME: 'Your welcome message',
  // ...
};
```

## Troubleshooting

### API Connection Issues

1. Verify backend is running on the correct port
2. Check `NEXT_PUBLIC_API_BASE_URL` in `.env.local`
3. Verify CORS settings in backend

### Build Errors

1. Clear Next.js cache: `rm -rf .next`
2. Remove node_modules: `rm -rf node_modules`
3. Reinstall dependencies: `npm install`

### Type Errors

1. Run type check: `npm run type-check`
2. Verify TypeScript version compatibility

## Performance Optimization

- Code splitting with Next.js dynamic imports
- Image optimization (if needed)
- CSS optimization with Tailwind purge
- API response caching (can be added)
- Lazy loading for conversations

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Follow the existing code structure
2. Use TypeScript strict mode
3. Follow component naming conventions
4. Add proper error handling
5. Document complex logic
6. Test thoroughly before committing

## License

This project is part of the Merchants Community Crawl system.

## Support

For issues or questions, please contact the development team.
