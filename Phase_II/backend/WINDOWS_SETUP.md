# Windows Setup Guide for FastAPI Backend

This guide provides Windows-specific instructions for setting up the FastAPI backend.

## Prerequisites

- **Python 3.11+** - [Download from python.org](https://www.python.org/downloads/)
- **Git** - [Download from git-scm.com](https://git-scm.com/download/win)
- **PostgreSQL** (optional) - For local database, or use Neon cloud database

## Quick Start

### 1. Clone Repository

```powershell
git clone <repository-url>
cd todo-app\backend
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: This project uses `psycopg[binary]` instead of `asyncpg` for better Windows compatibility. The binary version includes pre-compiled PostgreSQL drivers, avoiding the need for Microsoft C++ Build Tools.

### 4. Configure Environment Variables

```powershell
copy .env.example .env
```

Edit `.env` with your configuration:

```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/todo_db
JWT_SECRET_KEY=<generated-key>
BETTER_AUTH_SECRET=<generated-key>
ENVIRONMENT=development
DEBUG=True
```

**Generate secret keys**:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Run this command twice to generate two different keys.

### 5. Set Up Database

**Option A: Use Neon Cloud Database** (Recommended)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Update `DATABASE_URL` in `.env`:
   ```env
   DATABASE_URL=postgresql+psycopg://user:password@ep-xxx.neon.tech/dbname?sslmode=require
   ```

**Option B: Use Local PostgreSQL**

1. Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Create a database:
   ```powershell
   createdb todo_db
   ```
3. Update `DATABASE_URL` in `.env`:
   ```env
   DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/todo_db
   ```

### 6. Run Database Migrations

**Using psql (local PostgreSQL)**:
```powershell
psql -d todo_db -f migrations\001_initial.sql
```

**Using Neon (cloud)**:
```powershell
psql "your-neon-connection-string" -f migrations\001_initial.sql
```

### 7. Start Development Server

```powershell
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

### 8. Verify API is Running

Open your browser and navigate to:
- **API Root**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs

## Windows-Specific Notes

### Database Driver (psycopg vs asyncpg)

This project uses **psycopg[binary]** instead of **asyncpg** for the following reasons:

1. **No C++ Compiler Required**: `psycopg[binary]` includes pre-compiled binaries, avoiding the need for Microsoft C++ Build Tools
2. **Easier Installation**: Works out-of-the-box on Windows without additional setup
3. **Full Async Support**: Provides the same async/await functionality as asyncpg
4. **Production Ready**: Officially recommended by SQLAlchemy for PostgreSQL

**Connection String Format**:
- psycopg: `postgresql+psycopg://...`
- asyncpg: `postgresql+asyncpg://...` (requires C++ compiler on Windows)

### Common Windows Issues

#### Issue: "python: command not found"

**Solution**: Ensure Python is added to PATH during installation, or use `py` instead of `python`:
```powershell
py -m venv venv
```

#### Issue: "Scripts\activate: cannot be loaded because running scripts is disabled"

**Solution**: Enable script execution in PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Issue: "psql: command not found"

**Solution**: Add PostgreSQL bin directory to PATH:
1. Find PostgreSQL installation directory (e.g., `C:\Program Files\PostgreSQL\15\bin`)
2. Add to PATH environment variable
3. Restart terminal

#### Issue: Database connection refused

**Solution**:
1. Verify PostgreSQL service is running:
   ```powershell
   Get-Service -Name postgresql*
   ```
2. Start service if stopped:
   ```powershell
   Start-Service -Name postgresql-x64-15
   ```
3. Check `DATABASE_URL` in `.env` is correct

### Development Workflow

#### Activate Virtual Environment

Every time you open a new terminal:
```powershell
cd todo-app\backend
venv\Scripts\activate
```

#### Run Development Server

```powershell
uvicorn main:app --reload --port 8000
```

#### Run Tests

```powershell
pytest
```

#### Check Code Quality

```powershell
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .
```

### Using Docker (Alternative)

If you prefer to avoid Windows-specific issues, use Docker:

1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Create `Dockerfile` in backend directory
3. Run with Docker Compose

This approach provides a consistent Linux environment regardless of your Windows setup.

## Testing the API

### Using PowerShell

**1. Register a new user**:
```powershell
$body = @{
    name = "Test User"
    email = "test@example.com"
    password = "SecurePass123!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/signup" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

**2. Sign in**:
```powershell
$body = @{
    email = "test@example.com"
    password = "SecurePass123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/signin" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$token = $response.access_token
$userId = $response.user.id
```

**3. Create a task**:
```powershell
$body = @{
    title = "Buy groceries"
    description = "Milk, eggs, bread"
} | ConvertTo-Json

$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/$userId/tasks" `
    -Method POST `
    -ContentType "application/json" `
    -Headers $headers `
    -Body $body
```

**4. List tasks**:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/$userId/tasks" `
    -Method GET `
    -Headers $headers
```

### Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the request body
5. Click "Execute"
6. View the response

## Deployment

### Deploy to Railway

1. Create Railway account at [railway.app](https://railway.app)
2. Create new project
3. Connect GitHub repository
4. Set root directory to `backend/`
5. Add environment variables:
   - `DATABASE_URL` (from Neon)
   - `JWT_SECRET_KEY`
   - `BETTER_AUTH_SECRET`
   - `ENVIRONMENT=production`
6. Deploy automatically on push

Railway will use the `Procfile` to start the server.

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **psycopg Documentation**: https://www.psycopg.org/psycopg3/docs/
- **Neon Documentation**: https://neon.tech/docs
- **Railway Documentation**: https://docs.railway.app/

## Support

For issues or questions:
1. Check the [main README](README.md)
2. Review the [API specification](../specs/1-fastapi-backend/spec.md)
3. Check the [implementation plan](../specs/1-fastapi-backend/plan.md)
4. Open an issue on GitHub

---

**Happy coding on Windows! 🚀**
