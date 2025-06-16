# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Lightweight ChatGPT-like chat application with Django backend and Nuxt frontend. 
Features persistent chat storage, streaming LLM responses, and dark/light theme support. 
Users can create chats, select from multiple LLM models, and receive real-time streaming responses.

### Backend

- **Django 5** with django-ninja API framework
- **Chat Models**: Chat (uid, headline, model, timestamp) and Prompt (status, input/output text)
- **LLM Integration**: pydantic-ai for model abstraction with dummy model implementation
- **Async Worker**: LLM worker processes queued prompts with streaming output
- **API Endpoints**: Chat CRUD, model selection, prompt creation
- **Database**: SQLite (development) / PostgreSQL (production)

### Frontend

- **Framework**: Nuxt 3 with Vue 3 (SPA mode, SSR disabled)
- **Styling**: Bootstrap 5 + custom SCSS with T3.chat-inspired design
- **Theme**: Dark/light mode toggle with CSS custom properties
- **Icons**: Bootstrap Icons throughout the UI
- **API Integration**: Custom composable (`useApi.js`) with singleton pattern
- **Notifications**: Vue Toastification for user feedback
- **Note**: We do not use SSR - all frontend is on client side

#### Frontend Structure:
- `app.vue`: Root component with global theme management
- `pages/`: File-based routing (`index.vue`, `chats/[uid].vue`)
- `components/`: Chat components (Sidebar, Conversation, Message, Input)
- `composables/`: API utilities and theme management
- `assets/scss/`: Custom SCSS with Bootstrap integration and theming

#### Key Features:
- **ChatGPT-like Interface**: Sidebar for chat history, main area for conversation
- **Real-time Streaming**: Live message updates with polling for running prompts
- **Model Selection**: Dropdown to choose LLM model when creating chats
- **Dark/Light Theme**: Toggle with localStorage persistence and system preference detection
- **Responsive Design**: T3.chat-inspired modern UI with smooth transitions
- **Message Avatars**: User and assistant avatars with status indicators

## Development Setup

### Running the Application
These are started by user:
```bash
# Backend (Terminal 1)
cd backend
uvicorn asgi:application --reload

# LLM Worker (Terminal 2) 
cd backend
python manage.py worker_llm

# Frontend (Terminal 3)
cd frontend
npm run dev
```

### Key Files
- **Backend Models**: `chat/models.py` (Chat, Prompt)
- **API Endpoints**: `backend/api/main.py` 
- **LLM Worker**: `chat/worker.py` (processes prompts with pydantic-ai)
- **LLM Models**: `llms/dummy.py` (dummy model implementation)
- **Frontend API**: `composables/useApi.js`
- **Theme Management**: `app.vue` (global theme state)
- **Styling**: `assets/scss/main.scss` (Bootstrap + custom theming)

## Code Guidelines

- Do not use semicolons in JavaScript
- After changing Python files, run "ruff check" and "ruff format"
- Use Python 3.12+ type hints (list[X] instead of List[X], dict[X, Y] instead of Dict[X, Y])
- Use SCSS variables for Bootstrap compilation, CSS custom properties for dynamic theming