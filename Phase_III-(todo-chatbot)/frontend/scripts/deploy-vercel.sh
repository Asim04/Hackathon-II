#!/bin/bash
# Frontend Deployment Script for Vercel
# Usage: ./deploy-frontend.sh [environment]
# Example: ./deploy-frontend.sh production

set -e  # Exit on error

ENVIRONMENT=${1:-production}

echo "🚀 Deploying Frontend to Vercel ($ENVIRONMENT)"
echo "================================================"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if logged in
if ! vercel whoami &> /dev/null; then
    echo "❌ Not logged in to Vercel. Please run: vercel login"
    exit 1
fi

echo "✅ Vercel CLI ready"

# Navigate to frontend directory
cd "$(dirname "$0")/.."

# Verify required files exist
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found"
    exit 1
fi

if [ ! -f "next.config.js" ] && [ ! -f "next.config.mjs" ]; then
    echo "❌ next.config.js not found"
    exit 1
fi

echo "✅ Required files found"

# Check environment variables
echo ""
echo "📋 Checking environment variables..."

REQUIRED_VARS=("NEXT_PUBLIC_API_URL" "BETTER_AUTH_SECRET" "BETTER_AUTH_URL")
MISSING_VARS=()

for var in "${REQUIRED_VARS[@]}"; do
    if ! vercel env ls production | grep -q "$var"; then
        MISSING_VARS+=("$var")
    fi
done

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo "⚠️  Missing environment variables in Vercel:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    echo ""
    echo "Set them with: vercel env add $var production"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ All required environment variables set"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Run build locally to catch errors
echo ""
echo "🔨 Building locally..."
if npm run build; then
    echo "✅ Build successful"
else
    echo "❌ Build failed. Fix errors before deploying."
    exit 1
fi

# Run linter
echo ""
echo "🔍 Running linter..."
if npm run lint; then
    echo "✅ Linting passed"
else
    echo "⚠️  Linting issues found"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Deploy to Vercel
echo ""
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🚀 Deploying to production..."
    vercel --prod
else
    echo "🚀 Deploying to preview..."
    vercel
fi

# Get deployment URL
echo ""
echo "🔗 Getting deployment URL..."
DEPLOYMENT_URL=$(vercel ls --json | jq -r '.[0].url' 2>/dev/null || echo "")

if [ -z "$DEPLOYMENT_URL" ]; then
    echo "⚠️  Could not retrieve deployment URL"
    echo "   Check with: vercel ls"
else
    DEPLOYMENT_URL="https://$DEPLOYMENT_URL"
    echo "✅ Deployment URL: $DEPLOYMENT_URL"

    # Health check
    echo ""
    echo "🏥 Running health check..."
    sleep 15  # Wait for deployment to be ready

    if curl -f "$DEPLOYMENT_URL" &> /dev/null; then
        echo "✅ Health check passed"
        echo ""
        echo "🎉 Deployment successful!"
        echo "   URL: $DEPLOYMENT_URL"
        echo "   Dashboard: https://vercel.com/dashboard"
    else
        echo "⚠️  Health check failed (site may still be deploying)"
        echo "   Check status: vercel inspect $DEPLOYMENT_URL"
    fi
fi

echo ""
echo "📝 Next steps:"
echo "   1. Test the site: open $DEPLOYMENT_URL"
echo "   2. Test authentication flow"
echo "   3. Test chat interface at $DEPLOYMENT_URL/chat"
echo "   4. Configure custom domain (optional): vercel domains add yourdomain.com"
echo ""
