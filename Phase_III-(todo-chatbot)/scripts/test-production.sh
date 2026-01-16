#!/bin/bash
# Production Testing Script
# Usage: ./test-production.sh <backend-url> <frontend-url>
# Example: ./test-production.sh https://backend.railway.app https://frontend.vercel.app

set -e

BACKEND_URL=${1:-}
FRONTEND_URL=${2:-}

if [ -z "$BACKEND_URL" ] || [ -z "$FRONTEND_URL" ]; then
    echo "Usage: $0 <backend-url> <frontend-url>"
    echo "Example: $0 https://backend.railway.app https://frontend.vercel.app"
    exit 1
fi

echo "🧪 Production Testing Suite"
echo "============================"
echo "Backend: $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

# Test function
test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=${3:-200}
    local method=${4:-GET}
    local data=${5:-}
    local headers=${6:-}

    echo -n "Testing: $name... "

    if [ -n "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            ${headers:+-H "$headers"} \
            -d "$data" 2>/dev/null || echo "000")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            ${headers:+-H "$headers"} 2>/dev/null || echo "000")
    fi

    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$status_code" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $status_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} (Expected HTTP $expected_status, got $status_code)"
        if [ -n "$body" ]; then
            echo "  Response: $body"
        fi
        ((FAILED++))
        return 1
    fi
}

# 1. Backend Health Check
echo "📊 Backend Tests"
echo "----------------"
test_endpoint "Health Check" "$BACKEND_URL/health" 200

# 2. Backend API Documentation
test_endpoint "API Docs" "$BACKEND_URL/docs" 200

# 3. Frontend Health Check
echo ""
echo "🌐 Frontend Tests"
echo "-----------------"
test_endpoint "Homepage" "$FRONTEND_URL" 200
test_endpoint "Auth Page" "$FRONTEND_URL/auth/signin" 200

# 4. Authentication Flow
echo ""
echo "🔐 Authentication Tests"
echo "-----------------------"

# Generate random email for testing
TEST_EMAIL="test-$(date +%s)@example.com"
TEST_PASSWORD="TestPass123!"
TEST_NAME="Test User"

echo "Creating test user: $TEST_EMAIL"

# Signup
SIGNUP_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/auth/signup" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\",\"name\":\"$TEST_NAME\"}" 2>/dev/null)

if echo "$SIGNUP_RESPONSE" | grep -q "token"; then
    echo -e "${GREEN}✓ PASS${NC} Signup successful"
    ((PASSED++))

    # Extract token and user_id
    TOKEN=$(echo "$SIGNUP_RESPONSE" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    USER_ID=$(echo "$SIGNUP_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

    echo "  Token: ${TOKEN:0:20}..."
    echo "  User ID: $USER_ID"
else
    echo -e "${RED}✗ FAIL${NC} Signup failed"
    echo "  Response: $SIGNUP_RESPONSE"
    ((FAILED++))
    TOKEN=""
    USER_ID=""
fi

# Signin
if [ -n "$TOKEN" ]; then
    SIGNIN_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/auth/signin" \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}" 2>/dev/null)

    if echo "$SIGNIN_RESPONSE" | grep -q "token"; then
        echo -e "${GREEN}✓ PASS${NC} Signin successful"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} Signin failed"
        echo "  Response: $SIGNIN_RESPONSE"
        ((FAILED++))
    fi
fi

# 5. Task Operations
if [ -n "$TOKEN" ] && [ -n "$USER_ID" ]; then
    echo ""
    echo "📝 Task CRUD Tests"
    echo "------------------"

    # Create task
    CREATE_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/$USER_ID/tasks" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"title":"Test Task","description":"Testing production deployment"}' 2>/dev/null)

    if echo "$CREATE_RESPONSE" | grep -q "id"; then
        echo -e "${GREEN}✓ PASS${NC} Create task"
        ((PASSED++))
        TASK_ID=$(echo "$CREATE_RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2)
        echo "  Task ID: $TASK_ID"
    else
        echo -e "${RED}✗ FAIL${NC} Create task"
        echo "  Response: $CREATE_RESPONSE"
        ((FAILED++))
        TASK_ID=""
    fi

    # List tasks
    LIST_RESPONSE=$(curl -s "$BACKEND_URL/api/$USER_ID/tasks" \
        -H "Authorization: Bearer $TOKEN" 2>/dev/null)

    if echo "$LIST_RESPONSE" | grep -q "Test Task"; then
        echo -e "${GREEN}✓ PASS${NC} List tasks"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC} List tasks"
        echo "  Response: $LIST_RESPONSE"
        ((FAILED++))
    fi

    # Update task
    if [ -n "$TASK_ID" ]; then
        UPDATE_RESPONSE=$(curl -s -X PUT "$BACKEND_URL/api/$USER_ID/tasks/$TASK_ID" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d '{"title":"Updated Test Task"}' 2>/dev/null)

        if echo "$UPDATE_RESPONSE" | grep -q "Updated Test Task"; then
            echo -e "${GREEN}✓ PASS${NC} Update task"
            ((PASSED++))
        else
            echo -e "${RED}✗ FAIL${NC} Update task"
            echo "  Response: $UPDATE_RESPONSE"
            ((FAILED++))
        fi

        # Complete task
        COMPLETE_RESPONSE=$(curl -s -X PATCH "$BACKEND_URL/api/$USER_ID/tasks/$TASK_ID/complete" \
            -H "Authorization: Bearer $TOKEN" 2>/dev/null)

        if echo "$COMPLETE_RESPONSE" | grep -q "completed"; then
            echo -e "${GREEN}✓ PASS${NC} Complete task"
            ((PASSED++))
        else
            echo -e "${RED}✗ FAIL${NC} Complete task"
            echo "  Response: $COMPLETE_RESPONSE"
            ((FAILED++))
        fi

        # Delete task
        DELETE_RESPONSE=$(curl -s -X DELETE "$BACKEND_URL/api/$USER_ID/tasks/$TASK_ID" \
            -H "Authorization: Bearer $TOKEN" 2>/dev/null)

        if [ "$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BACKEND_URL/api/$USER_ID/tasks/$TASK_ID" \
            -H "Authorization: Bearer $TOKEN" 2>/dev/null)" = "204" ] || \
           echo "$DELETE_RESPONSE" | grep -q "deleted"; then
            echo -e "${GREEN}✓ PASS${NC} Delete task"
            ((PASSED++))
        else
            echo -e "${RED}✗ FAIL${NC} Delete task"
            echo "  Response: $DELETE_RESPONSE"
            ((FAILED++))
        fi
    fi
fi

# 6. Chat Endpoint
if [ -n "$TOKEN" ] && [ -n "$USER_ID" ]; then
    echo ""
    echo "💬 Chat Tests"
    echo "-------------"

    CHAT_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/$USER_ID/chat" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"message":"Hello, can you help me?","conversation_id":null}' 2>/dev/null)

    if echo "$CHAT_RESPONSE" | grep -q "conversation_id"; then
        echo -e "${GREEN}✓ PASS${NC} Chat endpoint"
        ((PASSED++))

        CONV_ID=$(echo "$CHAT_RESPONSE" | grep -o '"conversation_id":[0-9]*' | cut -d':' -f2)
        echo "  Conversation ID: $CONV_ID"

        # Test conversation persistence
        if [ -n "$CONV_ID" ]; then
            CHAT_RESPONSE_2=$(curl -s -X POST "$BACKEND_URL/api/$USER_ID/chat" \
                -H "Authorization: Bearer $TOKEN" \
                -H "Content-Type: application/json" \
                -d "{\"message\":\"Add a task to test chat\",\"conversation_id\":$CONV_ID}" 2>/dev/null)

            if echo "$CHAT_RESPONSE_2" | grep -q "conversation_id"; then
                echo -e "${GREEN}✓ PASS${NC} Conversation persistence"
                ((PASSED++))
            else
                echo -e "${RED}✗ FAIL${NC} Conversation persistence"
                echo "  Response: $CHAT_RESPONSE_2"
                ((FAILED++))
            fi
        fi
    else
        echo -e "${RED}✗ FAIL${NC} Chat endpoint"
        echo "  Response: $CHAT_RESPONSE"
        ((FAILED++))
    fi
fi

# 7. Security Tests
echo ""
echo "🔒 Security Tests"
echo "-----------------"

# Test unauthorized access
UNAUTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/$USER_ID/tasks" 2>/dev/null)
if [ "$UNAUTH_RESPONSE" = "401" ]; then
    echo -e "${GREEN}✓ PASS${NC} Unauthorized access blocked (HTTP 401)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} Unauthorized access not blocked (Expected 401, got $UNAUTH_RESPONSE)"
    ((FAILED++))
fi

# Test invalid token
INVALID_TOKEN_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/$USER_ID/tasks" \
    -H "Authorization: Bearer invalid-token" 2>/dev/null)
if [ "$INVALID_TOKEN_RESPONSE" = "401" ]; then
    echo -e "${GREEN}✓ PASS${NC} Invalid token rejected (HTTP 401)"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC} Invalid token not rejected (Expected 401, got $INVALID_TOKEN_RESPONSE)"
    ((FAILED++))
fi

# 8. Performance Tests
echo ""
echo "⚡ Performance Tests"
echo "--------------------"

# Measure response time
START_TIME=$(date +%s%N)
curl -s "$BACKEND_URL/health" > /dev/null
END_TIME=$(date +%s%N)
RESPONSE_TIME=$(( (END_TIME - START_TIME) / 1000000 ))

if [ $RESPONSE_TIME -lt 300 ]; then
    echo -e "${GREEN}✓ PASS${NC} Response time: ${RESPONSE_TIME}ms (< 300ms)"
    ((PASSED++))
else
    echo -e "${YELLOW}⚠ WARN${NC} Response time: ${RESPONSE_TIME}ms (> 300ms)"
    ((PASSED++))
fi

# Summary
echo ""
echo "================================"
echo "📊 Test Summary"
echo "================================"
echo -e "Total Tests: $((PASSED + FAILED))"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo ""
    echo "✅ Production deployment is healthy"
    echo ""
    echo "Next steps:"
    echo "  1. Test the frontend manually: $FRONTEND_URL"
    echo "  2. Test chat interface: $FRONTEND_URL/chat"
    echo "  3. Monitor logs for errors"
    echo "  4. Set up monitoring and alerts"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo "Please review the failures above and:"
    echo "  1. Check backend logs: railway logs (or render logs)"
    echo "  2. Verify environment variables are set correctly"
    echo "  3. Ensure database migrations have run"
    echo "  4. Check CORS configuration"
    exit 1
fi
