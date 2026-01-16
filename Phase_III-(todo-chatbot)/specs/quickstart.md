# Phase III Quickstart Guide

**Last Updated**: 2026-01-13
**Phase**: III - AI Chatbot
**Prerequisites**: Phase II completed (auth + task CRUD working)

---

## Overview

This guide walks you through setting up the Phase III AI chatbot locally for development and testing.

**What You'll Build**:
- Conversational AI interface for task management
- Natural language intent recognition
- MCP tools for database operations
- Stateless chat endpoint with conversation persistence

**Time to Complete**: ~30 minutes

---

## Prerequisites

### Required Software
- **Python**: 3.11 or higher
- **Node.js**: 18 or higher
- **PostgreSQL**: 14 or higher (or Neon account)
- **Git**: Latest version

### Required Accounts
- **OpenAI**: API key for Agents SDK ([get key](https://platform.openai.com/api-keys))
- **Neon**: PostgreSQL database ([sign up](https://neon.tech))
- **Better Auth**: Already configured in Phase II

### Verify Prerequisites
```bash
# Check Python version
python --version  # Should be 3.11+

# Check Node.js version
node --version  # Should be 18+

# Check PostgreSQL (if local)
psql --version  # Should be 14+
```

---

## Part 1: Backend Setup

### 1.1: Clone and Navigate
```bash
cd backend
```

### 1.2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 1.3: Install Dependencies
```bash
# Install Phase II dependencies (if not already installed)
pip install fastapi uvicorn sqlmodel psycopg2-binary alembic pydantic-settings better-auth

# Install Phase III dependencies
pip install openai mcp python-dotenv pytest pytest-asyncio httpx
```

### 1.4: Configure Environment Variables

Create `backend/.env`:
```bash
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host/database

# OpenAI API
OPENAI_API_KEY=sk-...

# Better Auth (from Phase II)
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:8000

# Environment
ENVIRONMENT=development
```

**Get Neon Database URL**:
1. Go to [Neon Console](https://console.neon.tech)
2. Create new project or select existing
3. Copy connection string from "Connection Details"
4. Paste into `DATABASE_URL`

**Get OpenAI API Key**:
1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create new secret key
3. Copy key (starts with `sk-`)
4. Paste into `OPENAI_API_KEY`

### 1.5: Run Database Migrations
```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Run Phase III migration (adds conversations and messages tables)
alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\dt"
# Should see: users, tasks, conversations, messages
```

### 1.6: Start Backend Server
```bash
# Start FastAPI server
uvicorn main:app --reload --port 8000

# Server should start at http://localhost:8000
# API docs available at http://localhost:8000/docs
```

**Verify Backend**:
```bash
# Test health endpoint
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

---

## Part 2: Frontend Setup

### 2.1: Navigate to Frontend
```bash
# Open new terminal
cd frontend
```

### 2.2: Install Dependencies
```bash
# Install Phase II dependencies (if not already installed)
npm install

# Install Phase III dependencies
npm install @openai/chatkit
```

### 2.3: Configure Environment Variables

Create `frontend/.env.local`:
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# OpenAI ChatKit (optional for local dev)
# NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...
```

**Note**: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is only required for production deployment. Local development works without it.

### 2.4: Start Frontend Server
```bash
# Start Next.js development server
npm run dev

# Server should start at http://localhost:3000
```

**Verify Frontend**:
1. Open browser to http://localhost:3000
2. You should see the landing page
3. Navigate to http://localhost:3000/login
4. Sign in with existing account (from Phase II)

---

## Part 3: Test Chat Functionality

### 3.1: Access Chat Interface
1. Navigate to http://localhost:3000/chat
2. You should see the chat interface (ChatKit component)
3. If not logged in, you'll be redirected to /login

### 3.2: Test Natural Language Commands

**Create Task**:
```
You: "I need to buy milk"
AI: "Got it! Added 'Buy milk' 📝"
```

**List Tasks**:
```
You: "What's on my list?"
AI: "You have 1 task: 1. Buy milk"
```

**Complete Task**:
```
You: "I finished buying milk"
AI: "Awesome! ✅ 'Buy milk' is complete!"
```

**Delete Task**:
```
You: "Delete the milk task"
AI: "Removed! 'Buy milk' deleted"
```

**Update Task**:
```
You: "Change task 1 to 'Buy almond milk'"
AI: "Perfect! Updated to 'Buy almond milk'"
```

### 3.3: Test Multi-Turn Conversation
```
You: "Add task to call dentist"
AI: "Got it! Added 'Call dentist' 📝"

You: "And add one for grocery shopping"
AI: "Added 'Grocery shopping' too!"

You: "What do I have now?"
AI: "You have 2 tasks: 1. Call dentist, 2. Grocery shopping"
```

### 3.4: Test Conversation Persistence

1. Send a message: "Add task to water plants"
2. Note the conversation ID in browser DevTools (Network tab)
3. Refresh the page
4. Send another message: "What did I just add?"
5. AI should remember: "You added 'Water plants'"

---

## Part 4: Run Tests

### 4.1: Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_mcp_tools.py

# Run with coverage
pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

**Expected Test Results**:
- ✅ test_models.py: Database model tests
- ✅ test_mcp_tools.py: MCP tool unit tests
- ✅ test_agent_intents.py: Intent recognition tests
- ✅ test_chat_endpoint.py: Chat API tests
- ✅ test_integration.py: End-to-end tests

### 4.2: Frontend Tests
```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- ChatInterface.test.tsx
```

---

## Part 5: Troubleshooting

### Issue: Database Connection Failed
**Symptoms**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solutions**:
1. Verify `DATABASE_URL` in `.env` is correct
2. Check Neon database is active (not paused)
3. Test connection: `psql $DATABASE_URL`
4. Verify firewall allows PostgreSQL connections

### Issue: OpenAI API Key Invalid
**Symptoms**: `openai.error.AuthenticationError: Incorrect API key`

**Solutions**:
1. Verify `OPENAI_API_KEY` in `.env` is correct
2. Check key starts with `sk-`
3. Verify key is active in OpenAI dashboard
4. Create new key if expired

### Issue: Chat Endpoint Returns 401
**Symptoms**: Chat requests fail with "Unauthorized"

**Solutions**:
1. Verify you're logged in (check localStorage for token)
2. Check JWT token is being sent in Authorization header
3. Verify `BETTER_AUTH_SECRET` matches between frontend and backend
4. Try logging out and logging back in

### Issue: MCP Tools Not Working
**Symptoms**: AI responds but tasks aren't created/updated

**Solutions**:
1. Check backend logs for tool execution errors
2. Verify database migrations ran successfully
3. Test MCP tools directly: `pytest tests/test_mcp_tools.py`
4. Check user_id is being injected correctly

### Issue: Conversation History Not Loading
**Symptoms**: AI doesn't remember previous messages

**Solutions**:
1. Verify `conversations` and `messages` tables exist
2. Check database indexes were created
3. Test conversation service: `pytest tests/test_conversation_service.py`
4. Verify conversation_id is being passed in requests

### Issue: Frontend Build Fails
**Symptoms**: `npm run build` fails with errors

**Solutions**:
1. Delete `node_modules` and `.next` folders
2. Run `npm install` again
3. Check Node.js version is 18+
4. Verify all dependencies installed correctly

---

## Part 6: Development Workflow

### Daily Development
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Tests (optional)
cd backend
pytest --watch
```

### Making Changes

**Backend Changes**:
1. Edit files in `backend/src/`
2. FastAPI auto-reloads on save
3. Run tests: `pytest`
4. Check API docs: http://localhost:8000/docs

**Frontend Changes**:
1. Edit files in `frontend/app/` or `frontend/components/`
2. Next.js auto-reloads on save
3. Run tests: `npm test`
4. Check browser console for errors

**Database Changes**:
1. Edit models in `backend/src/models.py`
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Review migration in `backend/alembic/versions/`
4. Apply migration: `alembic upgrade head`

### Debugging

**Backend Debugging**:
```python
# Add breakpoints in code
import pdb; pdb.set_trace()

# Or use VS Code debugger
# Create .vscode/launch.json with FastAPI configuration
```

**Frontend Debugging**:
- Use browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for API requests
- Use React DevTools extension

**Database Debugging**:
```bash
# Connect to database
psql $DATABASE_URL

# View conversations
SELECT * FROM conversations;

# View messages
SELECT * FROM messages ORDER BY created_at;

# View tasks
SELECT * FROM tasks;
```

---

## Part 7: Next Steps

### After Local Setup Works
1. ✅ Verify all tests pass
2. ✅ Test all natural language patterns
3. ✅ Test conversation persistence
4. ✅ Test user isolation (create second user, verify separation)
5. ✅ Review code quality (linting, type hints)

### Before Deployment
1. Run full test suite: `pytest && npm test`
2. Check test coverage: `pytest --cov`
3. Run linters: `ruff check . && npm run lint`
4. Test production build: `npm run build`
5. Review environment variables for production

### Deployment Guides
- **Backend**: See `docs/deploy-backend.md` (Railway)
- **Frontend**: See `docs/deploy-frontend.md` (Vercel)
- **Database**: See `docs/deploy-database.md` (Neon)

---

## Useful Commands

### Backend
```bash
# Start server
uvicorn main:app --reload

# Run tests
pytest

# Run specific test
pytest tests/test_mcp_tools.py::test_add_task

# Check code quality
ruff check .
black --check .

# Format code
black .

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Frontend
```bash
# Start dev server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint

# Format code
npm run format
```

### Database
```bash
# Connect to database
psql $DATABASE_URL

# View tables
\dt

# View table schema
\d conversations

# View indexes
\di

# Run query
SELECT * FROM conversations WHERE user_id = 'user_123';
```

---

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [OpenAI Agents SDK](https://platform.openai.com/docs/agents)
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [ChatKit Docs](https://platform.openai.com/docs/chatkit)

### Support
- **Issues**: Create issue in GitHub repository
- **Questions**: Ask in project Discord/Slack
- **Phase II Setup**: See `docs/phase2-quickstart.md`

---

## Success Checklist

- [ ] Backend server running at http://localhost:8000
- [ ] Frontend server running at http://localhost:3000
- [ ] Database migrations applied successfully
- [ ] Can create tasks via chat
- [ ] Can list tasks via chat
- [ ] Can complete tasks via chat
- [ ] Can delete tasks via chat
- [ ] Can update tasks via chat
- [ ] Conversations persist across page refreshes
- [ ] All backend tests pass
- [ ] All frontend tests pass
- [ ] User isolation working (separate accounts have separate data)

**If all items checked**: ✅ You're ready to develop Phase III features!

---

**Need Help?** Check the Troubleshooting section or create an issue in the repository.
