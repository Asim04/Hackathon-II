# Deployment Guide - Todo Chatbot Application

This guide covers deploying the Todo Chatbot application to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Variables](#environment-variables)
3. [Database Setup](#database-setup)
4. [Backend Deployment](#backend-deployment)
5. [Frontend Deployment](#frontend-deployment)
6. [Production Testing](#production-testing)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- [ ] OpenAI API key with sufficient quota
- [ ] Neon PostgreSQL database (or compatible PostgreSQL 14+)
- [ ] Railway/Render/Fly.io account (for backend)
- [ ] Vercel account (for frontend)
- [ ] Domain name (optional, for custom domain)

---

## Environment Variables

### Backend Environment Variables

**Required Variables:**

```bash
# Database Configuration
DATABASE_URL=postgresql+psycopg://user:password@host:5432/dbname
# Example: postgresql+psycopg://user:pass@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-...
# Get from: https://platform.openai.com/api-keys

# Authentication Secrets
JWT_SECRET_KEY=<generate-secure-random-string>
BETTER_AUTH_SECRET=<generate-secure-random-string>

# Application Configuration
ENVIRONMENT=production
DEBUG=False
```

**Optional Variables:**

```bash
# Cohere API (optional, for alternative LLM)
COHERE_API_KEY=<your-cohere-key>

# Logging
LOG_LEVEL=INFO

# CORS Origins (comma-separated)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Generate Secure Secrets:**

```bash
# For JWT_SECRET_KEY and BETTER_AUTH_SECRET
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or using OpenSSL
openssl rand -base64 32
```

### Frontend Environment Variables

**Required Variables:**

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
# Must be the public URL of your deployed backend

# Better Auth Configuration
BETTER_AUTH_SECRET=<same-as-backend-better-auth-secret>
BETTER_AUTH_URL=https://your-frontend.vercel.app
# Must match your Vercel deployment URL

# Environment
NODE_ENV=production
```

**Optional Variables:**

```bash
# OpenAI ChatKit Domain Key (if using ChatKit)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=<your-domain-key>
# Get from: https://platform.openai.com/chatkit
```

---

## Database Setup

### 1. Create Neon Database

1. Go to [Neon Console](https://console.neon.tech/)
2. Create a new project
3. Copy the connection string
4. Update format for psycopg:
   ```
   postgresql+psycopg://user:pass@host/dbname?sslmode=require
   ```

### 2. Run Database Migrations

**Option A: From Local Machine**

```bash
cd backend

# Set DATABASE_URL to production database
export DATABASE_URL="postgresql+psycopg://..."

# Run migrations
python -m alembic upgrade head

# Or create tables directly
python -c "from db import init_db; import asyncio; asyncio.run(init_db())"
```

**Option B: From Deployed Backend**

```bash
# SSH into your Railway/Render container
railway run bash  # or render ssh

# Run migrations
python -m alembic upgrade head
```

### 3. Verify Database Schema

```sql
-- Connect to your Neon database
psql "postgresql://..."

-- Check tables exist
\dt

-- Expected tables:
-- users, tasks, conversations, messages
```

---

## Backend Deployment

### Option 1: Railway (Recommended)

**Step 1: Install Railway CLI**

```bash
npm install -g @railway/cli
railway login
```

**Step 2: Initialize Project**

```bash
cd backend
railway init
```

**Step 3: Configure Environment Variables**

```bash
# Set all required environment variables
railway variables set DATABASE_URL="postgresql+psycopg://..."
railway variables set OPENAI_API_KEY="sk-proj-..."
railway variables set JWT_SECRET_KEY="<generated-secret>"
railway variables set BETTER_AUTH_SECRET="<generated-secret>"
railway variables set ENVIRONMENT="production"
railway variables set DEBUG="False"
```

**Step 4: Deploy**

```bash
railway up
```

**Step 5: Get Deployment URL**

```bash
railway domain
# Copy the URL (e.g., https://your-app.railway.app)
```

**Step 6: Run Database Migrations**

```bash
railway run python -m alembic upgrade head
```

**Step 7: Verify Health Check**

```bash
curl https://your-app.railway.app/health
# Expected: {"status":"healthy","timestamp":"...","version":"1.0.8"}
```

### Option 2: Render

**Step 1: Create Web Service**

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: todo-chatbot-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Step 2: Set Environment Variables**

Add all required environment variables in the Render dashboard.

**Step 3: Deploy**

Render will automatically deploy on git push.

### Option 3: Fly.io

**Step 1: Install Fly CLI**

```bash
curl -L https://fly.io/install.sh | sh
fly auth login
```

**Step 2: Initialize Fly App**

```bash
cd backend
fly launch
# Follow prompts, select region
```

**Step 3: Set Secrets**

```bash
fly secrets set DATABASE_URL="postgresql+psycopg://..."
fly secrets set OPENAI_API_KEY="sk-proj-..."
fly secrets set JWT_SECRET_KEY="<generated-secret>"
fly secrets set BETTER_AUTH_SECRET="<generated-secret>"
fly secrets set ENVIRONMENT="production"
fly secrets set DEBUG="False"
```

**Step 4: Deploy**

```bash
fly deploy
```

### Option 4: Koyeb

**Step 1: Create Service**

1. Go to [Koyeb Dashboard](https://app.koyeb.com/)
2. Click "Create Service"
3. Select "GitHub" and connect repository
4. Configure:
   - **Branch**: main
   - **Build**: Dockerfile
   - **Port**: 8000

**Step 2: Set Environment Variables**

Add all required environment variables in the Koyeb dashboard.

**Step 3: Deploy**

Koyeb will automatically deploy.

---

## Frontend Deployment

### Vercel Deployment (Recommended)

**Step 1: Install Vercel CLI**

```bash
npm install -g vercel
vercel login
```

**Step 2: Deploy from Local**

```bash
cd frontend
vercel
```

**Step 3: Set Environment Variables**

```bash
# Production environment variables
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://your-backend.railway.app

vercel env add BETTER_AUTH_SECRET production
# Enter: <same-as-backend>

vercel env add BETTER_AUTH_URL production
# Enter: https://your-frontend.vercel.app

vercel env add NODE_ENV production
# Enter: production
```

**Step 4: Deploy to Production**

```bash
vercel --prod
```

**Step 5: Configure Custom Domain (Optional)**

```bash
vercel domains add yourdomain.com
# Follow DNS configuration instructions
```

### Alternative: Deploy via GitHub Integration

**Step 1: Connect Repository**

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Select the `frontend` directory as root

**Step 2: Configure Build Settings**

- **Framework Preset**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

**Step 3: Set Environment Variables**

Add all required environment variables in the Vercel dashboard under "Settings" → "Environment Variables".

**Step 4: Deploy**

Vercel will automatically deploy on git push to main branch.

---

## Production Testing

### 1. Backend Health Check

```bash
# Test health endpoint
curl https://your-backend.railway.app/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-01-14T...",
  "version": "1.0.8"
}
```

### 2. Authentication Flow

```bash
# Test signup
curl -X POST https://your-backend.railway.app/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!",
    "name": "Test User"
  }'

# Test signin
curl -X POST https://your-backend.railway.app/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'

# Save the token from response
```

### 3. Task Operations

```bash
# Set your JWT token
TOKEN="<jwt-token-from-signin>"
USER_ID="<user-id-from-signin>"

# Create task
curl -X POST https://your-backend.railway.app/api/$USER_ID/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task",
    "description": "Testing production deployment"
  }'

# List tasks
curl https://your-backend.railway.app/api/$USER_ID/tasks \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Chat Endpoint

```bash
# Test chat endpoint
curl -X POST https://your-backend.railway.app/api/$USER_ID/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries",
    "conversation_id": null
  }'

# Expected: AI response with task creation confirmation
```

### 5. Frontend Testing

**Manual Testing Checklist:**

- [ ] Navigate to https://your-frontend.vercel.app
- [ ] Sign up with new account
- [ ] Sign in with credentials
- [ ] Navigate to /dashboard
- [ ] Create a task via form
- [ ] Navigate to /chat
- [ ] Send message: "Show me my tasks"
- [ ] Verify AI responds with task list
- [ ] Send message: "Add a task to test deployment"
- [ ] Verify task is created
- [ ] Send message: "Mark the test task as complete"
- [ ] Verify task is marked complete
- [ ] Sign out
- [ ] Verify redirect to signin page

### 6. Performance Testing

```bash
# Test response times
time curl https://your-backend.railway.app/health

# Load test (requires Apache Bench)
ab -n 100 -c 10 https://your-backend.railway.app/health

# Expected: < 300ms average response time
```

### 7. Error Handling

```bash
# Test invalid authentication
curl https://your-backend.railway.app/api/$USER_ID/tasks \
  -H "Authorization: Bearer invalid-token"

# Expected: 401 Unauthorized

# Test invalid user access
curl https://your-backend.railway.app/api/wrong-user-id/tasks \
  -H "Authorization: Bearer $TOKEN"

# Expected: 403 Forbidden
```

---

## Troubleshooting

### Backend Issues

**Issue: Database connection fails**

```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Should be: postgresql+psycopg://user:pass@host/db?sslmode=require

# Test connection
python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); print('Connected!')"
```

**Issue: OpenAI API errors**

```bash
# Verify API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check quota
# Go to: https://platform.openai.com/usage
```

**Issue: CORS errors**

```bash
# Check CORS_ORIGINS environment variable
# Should include your frontend URL

# Update in Railway/Render dashboard:
CORS_ORIGINS=https://your-frontend.vercel.app
```

**Issue: 500 Internal Server Error**

```bash
# Check logs
railway logs  # or render logs, fly logs

# Common causes:
# - Missing environment variables
# - Database migration not run
# - Invalid DATABASE_URL format
```

### Frontend Issues

**Issue: API calls fail**

```bash
# Check NEXT_PUBLIC_API_URL
# Must be public backend URL, not localhost

# Verify in browser console:
console.log(process.env.NEXT_PUBLIC_API_URL)
```

**Issue: Authentication fails**

```bash
# Verify BETTER_AUTH_SECRET matches backend
# Check BETTER_AUTH_URL matches Vercel deployment URL

# Test in browser:
localStorage.getItem('auth-token')
```

**Issue: Build fails on Vercel**

```bash
# Check build logs in Vercel dashboard
# Common causes:
# - Missing dependencies in package.json
# - TypeScript errors
# - Environment variables not set
```

### Database Issues

**Issue: Tables not created**

```bash
# Run migrations manually
railway run python -m alembic upgrade head

# Or create tables directly
railway run python -c "from db import init_db; import asyncio; asyncio.run(init_db())"
```

**Issue: Connection pool exhausted**

```bash
# Increase connection pool size in Neon dashboard
# Or add to DATABASE_URL:
?pool_size=20&max_overflow=10
```

---

## Post-Deployment Checklist

- [ ] Backend health check passes
- [ ] Database migrations completed
- [ ] All environment variables set correctly
- [ ] Frontend can reach backend API
- [ ] Authentication flow works end-to-end
- [ ] Task CRUD operations work
- [ ] Chat interface responds correctly
- [ ] User isolation verified (users can't see others' data)
- [ ] Error handling works (401, 403, 404, 500)
- [ ] Performance meets targets (< 2s chat response)
- [ ] HTTPS enabled on both frontend and backend
- [ ] Custom domain configured (if applicable)
- [ ] Monitoring/logging enabled
- [ ] Backup strategy in place for database

---

## Monitoring and Maintenance

### Logging

**Backend Logs:**

```bash
# Railway
railway logs --tail

# Render
render logs <service-id>

# Fly.io
fly logs
```

**Frontend Logs:**

```bash
# Vercel
vercel logs <deployment-url>
```

### Database Monitoring

- Monitor connection count in Neon dashboard
- Set up alerts for high CPU/memory usage
- Enable query performance insights
- Configure automatic backups

### Application Monitoring

**Recommended Tools:**

- **Sentry**: Error tracking and performance monitoring
- **LogRocket**: Session replay and debugging
- **Datadog**: Infrastructure and application monitoring
- **Better Stack**: Log aggregation and alerting

### Backup Strategy

**Database Backups:**

- Neon provides automatic daily backups
- Configure retention period (7-30 days)
- Test restore procedure monthly

**Code Backups:**

- GitHub repository is source of truth
- Tag releases: `git tag v1.0.0`
- Keep deployment history in Vercel/Railway

---

## Rollback Procedure

### Backend Rollback

**Railway:**

```bash
# List deployments
railway deployments

# Rollback to previous
railway rollback <deployment-id>
```

**Render:**

- Go to dashboard → Select service → Deployments
- Click "Rollback" on previous successful deployment

**Fly.io:**

```bash
# List releases
fly releases

# Rollback
fly releases rollback <version>
```

### Frontend Rollback

**Vercel:**

```bash
# List deployments
vercel ls

# Promote previous deployment
vercel promote <deployment-url>
```

Or via dashboard:
- Go to project → Deployments
- Click "Promote to Production" on previous deployment

### Database Rollback

**Neon:**

- Go to dashboard → Branches
- Restore from backup point-in-time
- Update DATABASE_URL to new branch

---

## Security Checklist

- [ ] All secrets stored in environment variables (not in code)
- [ ] HTTPS enabled on all endpoints
- [ ] JWT tokens have reasonable expiration (24 hours)
- [ ] CORS configured to allow only frontend domain
- [ ] Database uses SSL/TLS connections
- [ ] Rate limiting enabled on API endpoints
- [ ] Input validation on all user inputs
- [ ] SQL injection protection (using SQLModel ORM)
- [ ] XSS protection (React escapes by default)
- [ ] CSRF protection (JWT in Authorization header)
- [ ] Secrets rotation policy in place
- [ ] Regular dependency updates scheduled

---

## Support and Resources

**Documentation:**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs)
- [Neon Docs](https://neon.tech/docs)

**Community:**
- GitHub Issues: [Your Repository]
- Discord: [Your Server]
- Email: support@yourdomain.com

---

## Version History

- **v1.0.0** (2026-01-14): Initial production deployment
  - Backend: FastAPI with OpenAI Agents SDK
  - Frontend: Next.js 16 with ChatKit
  - Database: Neon PostgreSQL
  - Features: Task CRUD, AI Chat Interface, JWT Auth
