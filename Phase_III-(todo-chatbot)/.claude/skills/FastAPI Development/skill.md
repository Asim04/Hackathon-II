# Skill: FastAPI Development

Create the file: `.spec-kit/skills/fastapi-development.md`

---

# Skill: FastAPI Development

## Description
Expertise in building RESTful APIs using FastAPI framework.

## Capabilities
- Create FastAPI applications
- Define route handlers with proper decorators
- Implement request/response models with Pydantic
- Handle path parameters and query parameters
- Implement middleware
- Error handling with HTTPException
- CORS configuration
- Dependency injection
- Background tasks

## Best Practices
- Use async/await for I/O operations
- Type hints for all functions
- Pydantic models for validation
- Proper HTTP status codes
- Comprehensive error messages
- API versioning in routes
- Request/response logging

## Code Patterns

### Basic Endpoint
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str | None = None

@app.post("/api/tasks", status_code=201)
async def create_task(task: Task):
    # Implementation
    return {"id": 1, **task.dict()}
```

### Authentication Middleware
```python
from fastapi import Request, HTTPException, Depends
import jwt

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")

async def verify_token(request: Request):
    """Verify JWT token from Authorization header"""
    auth_header = request.headers.get("Authorization", "")
    
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = auth_header.replace("Bearer ", "")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/tasks")
async def get_tasks(user_id: str = Depends(verify_token)):
    # user_id is extracted from token
    tasks = await fetch_user_tasks(user_id)
    return tasks
```

### Error Handling
```python
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"error": "validation_error", "message": str(exc)}
    )

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: int):
    task = await fetch_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

### CORS Configuration
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Dependencies
- fastapi
- uvicorn
- pydantic
- python-jose (for JWT)