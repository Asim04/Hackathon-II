# Quick Deployment Guide

This is a condensed guide for deploying the Todo Chatbot application to production. For detailed instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

## Prerequisites

- [ ] OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- [ ] Neon PostgreSQL database ([Create one here](https://console.neon.tech/))
- [ ] Railway account ([Sign up](https://railway.app/)) or Render/Fly.io
- [ ] Vercel account ([Sign up](https://vercel.com/))

## Quick Start (5 minutes)

### 1. Setup Database (Neon)

```bash
# 1. Create Neon project at https://console.neon.tech/
# 2. Copy connection string
# 3. Convert format:
#    From: postgresql://user:pass@host/db
#    To:   postgresql+psycopg://user:pass@host/db?sslmode=require
```

### 2. Deploy Backend (Railway)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Navigate to backend
cd backend

# Initialize project
railway init

# Set environment variables
railway variables set DATABASE_URL="postgresql+psycopg://..."
railway variables set OPENAI_API_KEY="sk-proj-..."
railway variables set JWT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
railway variables set BETTER_AUTH_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
railway variables set ENVIRONMENT="production"
railway variables set DEBUG="False"

# Deploy
railway up

# Get URL
railway domain

# Run migrations
railway run python -m alembic upgrade head

# Test
curl https://your-backend.railway.app/health
```

**Or use the deployment script:**

```bash
cd backend
bash scripts/deploy-railway.sh production
```

### 3. Deploy Frontend (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Navigate to frontend
cd frontend

# Set environment variables
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://your-backend.railway.app

vercel env add BETTER_AUTH_SECRET production
# Enter: <same-as-backend-better-auth-secret>

vercel env add BETTER_AUTH_URL production
# Enter: https://your-frontend.vercel.app (you'll get this after first deploy)

vercel env add NODE_ENV production
# Enter: production

# Deploy
vercel --prod

# Test
open https://your-frontend.vercel.app
```

**Or use the deployment script:**

```bash
cd frontend
bash scripts/deploy-vercel.sh production
```

### 4. Test Production

```bash
# Run automated tests
bash scripts/test-production.sh \
  https://your-backend.railway.app \
  https://your-frontend.vercel.app
```

**Manual testing:**

1. Visit `https://your-frontend.vercel.app`
2. Sign up with a new account
3. Navigate to `/chat`
4. Send message: "Add a task to test deployment"
5. Verify AI responds and task is created

## Environment Variables Reference

### Backend (Railway)

```bash
DATABASE_URL=postgresql+psycopg://user:pass@host/db?sslmode=require
OPENAI_API_KEY=sk-proj-...
JWT_SECRET_KEY=<generate-with-secrets.token_urlsafe(32)>
BETTER_AUTH_SECRET=<generate-with-secrets.token_urlsafe(32)>
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (Vercel)

```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
BETTER_AUTH_SECRET=<same-as-backend>
BETTER_AUTH_URL=https://your-frontend.vercel.app
NODE_ENV=production
```

## Troubleshooting

### Backend not responding

```bash
# Check logs
railway logs

# Common issues:
# - DATABASE_URL format incorrect (must use postgresql+psycopg://)
# - OPENAI_API_KEY invalid or quota exceeded
# - Migrations not run
```

### Frontend can't reach backend

```bash
# Verify NEXT_PUBLIC_API_URL is set correctly
vercel env ls production

# Check CORS_ORIGINS in backend includes frontend URL
railway variables get CORS_ORIGINS
```

### Authentication fails

```bash
# Verify BETTER_AUTH_SECRET matches between frontend and backend
railway variables get BETTER_AUTH_SECRET
vercel env ls production | grep BETTER_AUTH_SECRET
```

### Database connection fails

```bash
# Test connection
railway run python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); print('Connected!')"

# Check format (must include ?sslmode=require for Neon)
railway variables get DATABASE_URL
```

## Alternative Deployment Options

### Backend: Render

```bash
# 1. Go to https://dashboard.render.com/
# 2. New → Web Service
# 3. Connect GitHub repo
# 4. Configure:
#    - Build: pip install -r requirements.txt
#    - Start: uvicorn main:app --host 0.0.0.0 --port $PORT
# 5. Add environment variables
# 6. Deploy
```

### Backend: Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
cd backend
fly launch
fly secrets set DATABASE_URL="..." OPENAI_API_KEY="..." ...
fly deploy
```

### Backend: Koyeb

```bash
# 1. Go to https://app.koyeb.com/
# 2. Create Service
# 3. Connect GitHub repo
# 4. Configure environment variables
# 5. Deploy
```

## Post-Deployment Checklist

- [ ] Backend health check passes (`/health` returns 200)
- [ ] Frontend loads successfully
- [ ] User can sign up and sign in
- [ ] User can create tasks via dashboard
- [ ] User can chat with AI at `/chat`
- [ ] AI can create, list, complete, delete, update tasks
- [ ] User isolation works (users can't see others' data)
- [ ] HTTPS enabled on both frontend and backend
- [ ] Environment variables secured (not in code)
- [ ] Database backups configured
- [ ] Monitoring/logging enabled

## Monitoring

### View Logs

```bash
# Backend (Railway)
railway logs --tail

# Frontend (Vercel)
vercel logs <deployment-url>
```

### Database Monitoring

- Neon Dashboard: https://console.neon.tech/
- Monitor connection count, CPU, memory
- Configure automatic backups

### Application Monitoring (Optional)

- **Sentry**: Error tracking
- **LogRocket**: Session replay
- **Datadog**: Infrastructure monitoring

## Rollback

### Backend

```bash
# Railway
railway deployments
railway rollback <deployment-id>

# Render: Use dashboard → Deployments → Rollback
# Fly.io: fly releases rollback <version>
```

### Frontend

```bash
# Vercel
vercel ls
vercel promote <previous-deployment-url>

# Or use dashboard → Deployments → Promote to Production
```

## Support

- **Documentation**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Email**: support@yourdomain.com

## Next Steps

1. Configure custom domain (optional)
2. Set up monitoring and alerts
3. Enable automatic backups
4. Configure CI/CD pipeline
5. Set up staging environment
6. Document runbook for common issues

---

**Deployment Time**: ~10-15 minutes
**Cost**: Free tier available on all platforms
**Support**: Community + Documentation
