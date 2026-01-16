# Todo App - Project Overview

## Current Phase: Phase III - AI Chatbot
Transform web app into intelligent conversational interface using AI agents and MCP.

## Tech Stack
- Frontend: Next.js 16+ + OpenAI ChatKit
- Backend: FastAPI + OpenAI Agents SDK
- MCP Server: Official MCP SDK
- Database: Neon PostgreSQL (SQLModel)
- Auth: Better Auth with JWT

## Key Features
- Natural language task management
- Conversational AI interface
- MCP tools (add, list, complete, delete, update tasks)
- Stateless chat with database persistence
- Multi-turn conversations

## Architecture Principles
1. Stateless server (all state in database)
2. MCP tools (standardized AI interface)
3. Agent-based orchestration
4. Context-aware conversations

## Success Criteria
- Create tasks via chat: "Add task to buy milk"
- List tasks: "What's on my list?"
- Complete tasks: "Mark task 1 as done"
- Delete tasks: "Delete meeting task"
- Update tasks: "Change task 2 to 'Call mom'"
- Conversations persist across sessions
- Server stateless (survives restarts)
