#!/bin/bash
# Backend Deployment Script for Railway
# Usage: ./deploy-backend.sh [environment]
# Example: ./deploy-backend.sh production

set -e  # Exit on error

ENVIRONMENT=${1:-production}

echo "🚀 Deploying Backend to Railway ($ENVIRONMENT)"
echo "================================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if logged in
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway. Please run: railway login"
    exit 1
fi

echo "✅ Railway CLI ready"

# Navigate to backend directory
cd "$(dirname "$0")/.."

# Verify required files exist
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

if [ ! -f "main.py" ]; then
    echo "❌ main.py not found"
    exit 1
fi

echo "✅ Required files found"

# Check environment variables
echo ""
echo "📋 Checking environment variables..."

REQUIRED_VARS=("DATABASE_URL" "OPENAI_API_KEY" "JWT_SECRET_KEY" "BETTER_AUTH_SECRET")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if ! railway variables get "$var" &> /dev/null; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo "⚠️  Missing environment variables:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "Set them with: railway variables set $var=<value>"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ All required environment variables set"
fi

# Run tests before deployment
echo ""
echo "🧪 Running tests..."
if command -v pytest &> /dev/null; then
    if ! pytest tests/ -v --tb=short; then
        echo "❌ Tests failed. Aborting deployment."
        read -p "Deploy anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        echo "✅ Tests passed"
    fi
else
    echo "⚠️  pytest not found, skipping tests"
fi

# Deploy to Railway
echo ""
echo "🚀 Deploying to Railway..."
railway up

# Get deployment URL
echo ""
echo "🔗 Getting deployment URL..."
DEPLOYMENT_URL=$(railway domain)

if [ -z "$DEPLOYMENT_URL" ]; then
    echo "⚠️  No domain configured. Generate one with: railway domain"
else
    echo "✅ Deployment URL: $DEPLOYMENT_URL"
fi

# Run database migrations
echo ""
echo "📊 Running database migrations..."
if railway run python -m alembic upgrade head; then
    echo "✅ Migrations completed"
else
    echo "⚠️  Migration failed or not configured"
fi

# Health check
echo ""
echo "🏥 Running health check..."
sleep 10  # Wait for deployment to be ready

if [ -n "$DEPLOYMENT_URL" ]; then
    if curl -f "$DEPLOYMENT_URL/health" &> /dev/null; then
        echo "✅ Health check passed"
        echo ""
        echo "🎉 Deployment successful!"
        echo "   URL: $DEPLOYMENT_URL"
        echo "   Health: $DEPLOYMENT_URL/health"
        echo "   Docs: $DEPLOYMENT_URL/docs"
    else
        echo "❌ Health check failed"
        echo "   Check logs with: railway logs"
        exit 1
    fi
else
    echo "⚠️  Skipping health check (no domain configured)"
fi

echo ""
echo "📝 Next steps:"
echo "   1. Test the API: curl $DEPLOYMENT_URL/health"
echo "   2. View logs: railway logs"
echo "   3. Update frontend NEXT_PUBLIC_API_URL to: $DEPLOYMENT_URL"
echo ""
