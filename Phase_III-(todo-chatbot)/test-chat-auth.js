/**
 * Test script for chat authentication flow
 *
 * This script tests:
 * 1. User can sign up and get auth token
 * 2. Authenticated user can access chat endpoint
 * 3. Unauthenticated request to chat fails with 401
 * 4. Chat page loads without premature redirects
 */

const API_URL = 'http://127.0.0.1:8000';
const FRONTEND_URL = 'http://localhost:3000';

// Test colors
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[36m',
};

function log(message, color = colors.reset) {
  console.log(`${color}${message}${colors.reset}`);
}

// Generate unique email for testing
const testEmail = `test_${Date.now()}@example.com`;
const testPassword = 'TestPassword123!';

async function testSignup() {
  log('\n=== Test 1: User Signup & Signin ===', colors.blue);

  try {
    // Signup
    const signupResponse = await fetch(`${API_URL}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: testEmail,
        password: testPassword,
        name: 'Test User',
      }),
    });

    if (!signupResponse.ok) {
      const error = await signupResponse.text();
      throw new Error(`Signup failed: ${signupResponse.status} - ${error}`);
    }

    const signupData = await signupResponse.json();
    log('✓ Signup successful', colors.green);
    log(`  User ID: ${signupData.user_id}`, colors.reset);

    // Signin to get token
    const signinResponse = await fetch(`${API_URL}/api/auth/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: testEmail,
        password: testPassword,
      }),
    });

    if (!signinResponse.ok) {
      const error = await signinResponse.text();
      throw new Error(`Signin failed: ${signinResponse.status} - ${error}`);
    }

    const signinData = await signinResponse.json();
    log('✓ Signin successful', colors.green);
    log(`  Token: ${signinData.access_token.substring(0, 20)}...`, colors.reset);

    return {
      token: signinData.access_token,
      userId: signupData.user_id,
    };
  } catch (error) {
    log(`✗ Signup/Signin failed: ${error.message}`, colors.red);
    throw error;
  }
}

async function testChatAuthenticated(token, userId) {
  log('\n=== Test 2: Authenticated Chat Access ===', colors.blue);

  try {
    const response = await fetch(`${API_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        message: 'Hello, can you list my tasks?',
        conversation_id: null,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Chat request failed: ${response.status} - ${error}`);
    }

    const data = await response.json();
    log('✓ Chat endpoint accessible with auth token', colors.green);
    log(`  Response: ${data.message.substring(0, 50)}...`, colors.reset);
    log(`  Conversation ID: ${data.conversation_id}`, colors.reset);

    return data.conversation_id;
  } catch (error) {
    log(`✗ Chat access failed: ${error.message}`, colors.red);
    throw error;
  }
}

async function testChatUnauthenticated() {
  log('\n=== Test 3: Unauthenticated Chat Access ===', colors.blue);

  try {
    // Use a fake UUID for testing
    const fakeUserId = '00000000-0000-0000-0000-000000000000';
    const response = await fetch(`${API_URL}/api/${fakeUserId}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: 'Hello',
        conversation_id: null,
      }),
    });

    if (response.status === 401) {
      log('✓ Unauthenticated request correctly rejected (401)', colors.green);
      return true;
    } else {
      log(`✗ Expected 401, got ${response.status}`, colors.red);
      return false;
    }
  } catch (error) {
    log(`✗ Unexpected error: ${error.message}`, colors.red);
    return false;
  }
}

async function testFrontendChatPage() {
  log('\n=== Test 4: Frontend Chat Page ===', colors.blue);

  try {
    const response = await fetch(`${FRONTEND_URL}/chat`);

    if (response.ok) {
      log('✓ Chat page loads without errors', colors.green);
      log(`  Status: ${response.status}`, colors.reset);

      // Check if it's not immediately redirecting (would be 307/308)
      if (response.status === 200) {
        log('✓ No immediate redirect (status 200)', colors.green);
      }

      return true;
    } else {
      log(`✗ Chat page failed to load: ${response.status}`, colors.red);
      return false;
    }
  } catch (error) {
    log(`✗ Frontend test failed: ${error.message}`, colors.red);
    return false;
  }
}

async function runTests() {
  log('Starting Chat Authentication Tests', colors.yellow);
  log(`API URL: ${API_URL}`, colors.reset);
  log(`Frontend URL: ${FRONTEND_URL}`, colors.reset);

  let allPassed = true;

  try {
    // Test 1: Signup
    const { token, userId } = await testSignup();

    // Test 2: Authenticated chat access
    await testChatAuthenticated(token, userId);

    // Test 3: Unauthenticated chat access
    const test3Passed = await testChatUnauthenticated();
    if (!test3Passed) allPassed = false;

    // Test 4: Frontend chat page
    const test4Passed = await testFrontendChatPage();
    if (!test4Passed) allPassed = false;

  } catch (error) {
    log(`\n✗ Test suite failed: ${error.message}`, colors.red);
    allPassed = false;
  }

  // Summary
  log('\n' + '='.repeat(50), colors.yellow);
  if (allPassed) {
    log('✓ All tests passed!', colors.green);
    log('\nManual verification needed:', colors.yellow);
    log('1. Open browser to http://localhost:3000', colors.reset);
    log('2. Sign in with existing account', colors.reset);
    log('3. Click "Chat" button in navigation', colors.reset);
    log('4. Verify: No redirect to signin, chat loads immediately', colors.reset);
    log('5. Refresh page: Should stay on chat, not redirect', colors.reset);
  } else {
    log('✗ Some tests failed', colors.red);
  }
  log('='.repeat(50), colors.yellow);
}

// Run tests
runTests().catch(error => {
  log(`\nFatal error: ${error.message}`, colors.red);
  process.exit(1);
});
