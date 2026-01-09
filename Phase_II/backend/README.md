# Multi-User Todo Application Backend API

FastAPI backend with JWT authentication for a multi-user todo application.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Task Management**: Full CRUD operations for personal tasks
- **User Isolation**: Strict user-level data isolation at database query level
- **Async Architecture**: Non-blocking I/O with async/await patterns
- **OpenAPI Documentation**: Auto-generated API documentation at `/docs`

## Tech Stack

- **Framework**: FastAPI 0.104+
- **ORM**: SQLModel 0.0.14+ (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL 15+ (Neon Serverless)
- **Authentication**: JWT (python-jose) + Bcrypt (passlib)
- **Server**: Uvicorn (ASGI)

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL (or Neon cloud database)
- pip

### Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Generate secret keys**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Run database migrations**:
   ```bash
   psql "your-database-url" -f migrations/001_initial.sql
   ```

6. **Start development server**:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

7. **Access API documentation**:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Sign in and receive JWT token

### Tasks (requires authentication)
- `GET /api/{user_id}/tasks` - List user's tasks (with optional status filter)
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{task_id}` - Get task details
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

### Utility
- `GET /health` - Health check
- `GET /` - API information

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── db.py                   # Database connection
├── models.py               # SQLModel database models
├── routes/
│   ├── auth.py            # Authentication endpoints
│   └── tasks.py           # Task CRUD endpoints
├── middleware/
│   └── jwt_auth.py        # JWT verification
├── utils/
│   ├── password.py        # Password hashing
│   └── jwt.py             # JWT token utilities
├── schemas/
│   ├── auth.py            # Auth request/response schemas
│   └── task.py            # Task request/response schemas
├── migrations/
│   └── 001_initial.sql    # Database schema
├── tests/
│   ├── conftest.py        # Test fixtures
│   ├── test_auth.py       # Auth endpoint tests
│   └── test_tasks.py      # Task endpoint tests
├── .env                   # Environment variables (gitignored)
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Deployment

### Railway

1. Create Railway account at [railway.app](https://railway.app)
2. Create new project and connect GitHub repository
3. Set root directory to `backend/`
4. Add environment variables (DATABASE_URL, JWT_SECRET_KEY, BETTER_AUTH_SECRET)
5. Deploy automatically on push

Railway will use the `Procfile` to start the server.

## Development

For detailed setup instructions, API testing examples, and troubleshooting, see:
- [Developer Quickstart Guide](../specs/1-fastapi-backend/quickstart.md)
- [API Specification](../specs/1-fastapi-backend/spec.md)
- [Implementation Plan](../specs/1-fastapi-backend/plan.md)
- [OpenAPI Contract](../specs/1-fastapi-backend/contracts/openapi.yaml)

## Security

- JWT tokens expire after 7 days
- Passwords hashed with bcrypt (10 rounds)
- User isolation enforced at database query level
- CORS configured for specific origins only
- All protected endpoints require valid JWT token

## License

MIT
