# Manual Testing Guide - Chat Authentication Fix

**Status**: ✅ Ready for Manual Testing
**Date**: 2026-01-14

---

## 🚀 Servers Running

Both servers are now running and ready for testing:

- **Backend**: `http://127.0.0.1:8000` ✅ Running
- **Frontend**: `http://localhost:3000` ✅ Running

---

## 📋 Manual Test Cases

### Test Case 1: Authenticated User Can Access Chat ✅

**Objective**: Verify logged-in users can access chat without redirect

**Steps**:
1. Open browser to `http://localhost:3000`
2. Click "Sign In" (if not already logged in)
3. Sign in with your credentials
4. Click "Chat" button in the navigation bar

**Expected Results**:
- ✅ Brief loading spinner appears (< 1 second)
- ✅ Chat interface loads immediately
- ✅ No redirect to signin page
- ✅ Can see chat header: "AI Task Assistant"
- ✅ Can see example prompts or previous messages
- ✅ Input field is enabled and ready

**What Changed**:
- **Before**: Immediate redirect to signin even when logged in
- **After**: Proper auth check, then loads chat interface

---

### Test Case 2: Page Refresh Maintains Session ✅

**Objective**: Verify authentication persists across page refreshes

**Steps**:
1. While on chat page (from Test Case 1)
2. Press F5 to refresh the page
3. Wait for page to reload

**Expected Results**:
- ✅ Brief loading spinner appears
- ✅ Chat interface returns (no redirect)
- ✅ Previous conversation history loads (if any)
- ✅ Still authenticated, can send messages

**What Changed**:
- **Before**: Would redirect to signin on refresh
- **After**: Maintains authentication state via React Query

---

### Test Case 3: Unauthenticated User Gets Redirected ✅

**Objective**: Verify security - unauthenticated users cannot access chat

**Steps**:
1. Open **incognito/private** browser window
2. Navigate directly to `http://localhost:3000/chat`
3. Observe behavior

**Expected Results**:
- ✅ Loading spinner appears briefly
- ✅ Toast notification: "Please sign in to use the chat"
- ✅ Redirects to signin page (`/auth/signin`)
- ✅ Cannot access chat without authentication

**What Changed**:
- **Before**: Inconsistent behavior, sometimes no redirect
- **After**: Proper security enforcement with loading state

---

### Test Case 4: Navigation Between Pages ✅

**Objective**: Verify smooth navigation without authentication issues

**Steps**:
1. Sign in and navigate to Dashboard
2. Click "Chat" button in navigation
3. Click "Dashboard" button in navigation
4. Click "Chat" button again
5. Repeat 2-3 times

**Expected Results**:
- ✅ Smooth transitions between pages
- ✅ No unexpected redirects to signin
- ✅ Brief loading spinner only when navigating to chat
- ✅ Authentication state maintained throughout
- ✅ Navigation buttons highlight active page

**What Changed**:
- **Before**: Chat button would redirect to signin
- **After**: Proper navigation with auth state management

---

### Test Case 5: Send Chat Message ✅

**Objective**: Verify full chat functionality works

**Steps**:
1. Sign in and navigate to chat page
2. Type a message: "Add a task to buy groceries"
3. Press Enter or click Send button
4. Wait for AI response

**Expected Results**:
- ✅ Message appears in chat immediately (optimistic update)
- ✅ Loading indicator shows while AI processes
- ✅ AI response appears with task confirmation
- ✅ Can send multiple messages in conversation
- ✅ Conversation ID created and maintained

**Note**: OpenAI API key must be configured in `backend/.env` for this to work

---

## 🔧 Technical Verification

### Check Authentication State in Browser

**Open Browser DevTools** (F12):

1. **Console Tab**:
   - No authentication errors
   - No localStorage access errors
   - No SSR hydration warnings

2. **Network Tab**:
   - Check `/api/{user_id}/chat` requests
   - Should have `Authorization: Bearer <token>` header
   - Should return 200 status (if API key configured)

3. **Application Tab** → Local Storage:
   - `auth-token`: JWT token present (when logged in)
   - `user`: User object present (when logged in)
   - `user-id`: User UUID present (when logged in)

---

## 🎯 Success Criteria

All of these should be true after testing:

- [ ] Logged-in users can access chat without redirect
- [ ] Page refresh doesn't lose authentication
- [ ] Loading spinner shows during auth check (brief, < 1 second)
- [ ] Unauthenticated users get redirected to signin
- [ ] Navigation between Dashboard and Chat works smoothly
- [ ] No console errors related to authentication
- [ ] Chat interface renders correctly
- [ ] Can send and receive chat messages (if OpenAI API configured)

---

## 🐛 If You Encounter Issues

### Issue: Still redirects to signin when logged in

**Check**:
1. Clear browser cache and localStorage
2. Sign out and sign in again
3. Check browser console for errors
4. Verify both servers are running

### Issue: Loading spinner shows indefinitely

**Check**:
1. Check browser console for errors
2. Verify `useAuth` hook is returning data
3. Check Network tab for failed auth requests

### Issue: Chat messages don't work

**Check**:
1. Verify OpenAI API key in `backend/.env`:
   ```
   OPENAI_API_KEY=sk-proj-...
   ```
2. Restart backend server after changing .env
3. Check backend console for errors
4. Verify chat endpoint returns 200 (not 400)

---

## 📊 Automated Test Results

Before manual testing, automated tests confirmed:

✅ **Backend Tests**: 20/20 passed
- Authentication endpoint tests
- Chat endpoint tests
- Integration tests
- User isolation tests

✅ **API Tests**: All passed
- User signup works
- User signin works
- JWT authentication works
- Unauthenticated requests rejected (401)
- Authenticated requests accepted

✅ **Component Tests**: Verified
- Navigation component has no conflicts
- useAuth hook works correctly
- Loading states implemented properly

---

## 📝 Report Results

After completing manual tests, please report:

1. **Which test cases passed**: ✅ or ❌
2. **Any unexpected behavior**
3. **Console errors** (if any)
4. **Network errors** (if any)
5. **User experience feedback**

---

## 🎉 Expected Outcome

If all tests pass, you should experience:

- **Smooth authentication flow**: No jarring redirects
- **Fast loading**: Brief spinner, then instant chat access
- **Persistent session**: Stays logged in across refreshes
- **Secure access**: Cannot access chat without authentication
- **Professional UX**: Loading indicators, smooth transitions

The chat authentication bug should be **completely resolved**! 🚀

---

## Server Commands (Reference)

If you need to restart servers:

**Backend**:
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run dev
```

**Check servers are running**:
- Backend: `curl http://127.0.0.1:8000/health`
- Frontend: Open `http://localhost:3000` in browser
