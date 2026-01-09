# Developer Quickstart Guide

**Feature**: Multi-User Todo Application Backend API
**Last Updated**: 2026-01-08

## Overview

This guide will help you set up the FastAPI backend locally for development and testing. Follow these steps to get the API running on your machine.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **pip** - Python package manager (included with Python)
- **Git** - Version control
- **PostgreSQL** (optional) - For local database, or use Neon cloud database

**Recommended Tools**:
- **VS Code** with Python extension
- **Postman** or **curl** for API testing
- **pgAdmin** or **psql** for database management

---

## Setup Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-app
git checkout 1-fastapi-backend
```

### 2. Navigate to Backend Directory

```bash
cd backend
```

### 3. Create Virtual Environment

**On macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages**:
- fastapi[all] - Web framework
- sqlmodel - ORM
- asyncpg - PostgreSQL driver
- python-jose[cryptography] - JWT handling
- passlib[bcrypt] - Password hashing
- uvicorn[standard] - ASGI server
- pytest - Testing framework
- httpx - Async HTTP client for tests

### 5. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here-generate-with-command-below
BETTER_AUTH_SECRET=your-better-auth-secret-here

# Application Configuration
ENVIRONMENT=development
DEBUG=True
```

**Generate secure secret keys**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Run this command twice to generate two different keys for `JWT_SECRET_KEY` and `BETTER_AUTH_SECRET`.

### 6. Set Up Database

**Option A: Use Neon Cloud Database** (Recommended)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Update `DATABASE_URL` in `.env` with the Neon connection string

**Option B: Use Local PostgreSQL**

1. Install PostgreSQL locally
2. Create a database:
   ```bash
   createdb todo_db
   ```
3. Update `DATABASE_URL` in `.env`:
   ```env
   DATABASE_URL=postgresql+asyncpg://localhost:5432/todo_db
   ```

### 7. Run Database Migrations

Execute the SQL migration script to create tables:

```bash
# Using psql (local PostgreSQL)
psql -d todo_db -f migrations/001_initial.sql

# Using Neon (cloud)
psql "your-neon-connection-string" -f migrations/001_initial.sql
```

**Verify tables created**:
```bash
psql -d todo_db -c "\dt"
```

You should see `users` and `tasks` tables.

### 8. Start the Development Server

```bash
uvicorn main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 9. Verify API is Running

Open your browser and navigate to:

- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc (ReDoc)

---

## Testing the API

### Using Swagger UI (Recommended for Beginners)

1. Open http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"
6. View the response

### Using curl

**1. Register a new user**:
```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected response** (201 Created):
```json
{
  "message": "User created successfully",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**2. Sign in**:
```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "name": "Test User",
    "created_at": "2026-01-08T12:00:00Z"
  }
}
```

**3. Create a task** (requires authentication):
```bash
# Save the token from sign-in response
TOKEN="your-jwt-token-here"
USER_ID="your-user-id-here"

curl -X POST http://localhost:8000/api/$USER_ID/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Buy groceries",
    "description": "Milk, eggs, bread"
  }'
```

**Expected response** (201 Created):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-08T12:05:00Z",
  "updated_at": "2026-01-08T12:05:00Z"
}
```

**4. List tasks**:
```bash
curl -X GET http://localhost:8000/api/$USER_ID/tasks \
  -H "Authorization: Bearer $TOKEN"
```

**5. Toggle task completion**:
```bash
TASK_ID=1

curl -X PATCH http://localhost:8000/api/$USER_ID/tasks/$TASK_ID/complete \
  -H "Authorization: Bearer $TOKEN"
```

**6. Delete task**:
```bash
curl -X DELETE http://localhost:8000/api/$USER_ID/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN"
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

View coverage report: `open htmlcov/index.html`

### Run Specific Test File

```bash
pytest tests/test_auth.py
pytest tests/test_tasks.py
```

### Run with Verbose Output

```bash
pytest -v
```

---

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
└── README.md              # Project documentation
```

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "Connection refused" when connecting to database

**Solution**:
1. Verify PostgreSQL is running: `pg_isready`
2. Check `DATABASE_URL` in `.env` is correct
3. Ensure database exists: `createdb todo_db`

### Issue: "Invalid JWT token" errors

**Solution**:
1. Verify `JWT_SECRET_KEY` in `.env` matches the key used to generate tokens
2. Check token hasn't expired (7-day validity)
3. Ensure `Authorization: Bearer <token>` header is correctly formatted

### Issue: "CORS error" when calling from frontend

**Solution**: Verify frontend origin is in CORS allowed origins list in `main.py`:
```python
origins = [
    "http://localhost:3000",  # Add your frontend URL
]
```

---

## Development Workflow

### 1. Make Code Changes

Edit files in `backend/` directory. The server will auto-reload with `--reload` flag.

### 2. Test Changes

```bash
# Run tests
pytest

# Test specific endpoint
curl -X GET http://localhost:8000/health
```

### 3. Check Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add new endpoint"
git push origin 1-fastapi-backend
```

---

## Deployment

### Deploy to Railway

1. Create Railway account at [railway.app](https://railway.app)
2. Create new project
3. Connect GitHub repository
4. Select `backend/` as root directory
5. Add environment variables:
   - `DATABASE_URL` (from Neon)
   - `JWT_SECRET_KEY`
   - `BETTER_AUTH_SECRET`
6. Deploy automatically on push

Railway will use the `Procfile` to start the server:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Next Steps

1. **Implement remaining endpoints** - Follow tasks.md for implementation order
2. **Write tests** - Achieve >80% code coverage
3. **Integrate with frontend** - Test with Next.js application
4. **Deploy to production** - Railway + Neon setup
5. **Monitor performance** - Add logging and metrics

---

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Neon Documentation**: https://neon.tech/docs
- **Railway Documentation**: https://docs.railway.app/
- **JWT.io**: https://jwt.io/ (decode and verify tokens)

---

## Support

For issues or questions:
1. Check the [API documentation](http://localhost:8000/docs)
2. Review the [specification](../spec.md)
3. Check the [implementation plan](../plan.md)
4. Open an issue on GitHub

---

**Happy coding! 🚀**
