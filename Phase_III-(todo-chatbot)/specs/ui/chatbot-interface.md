# ChatKit UI Specification

## Pages

### `/app/chat/page.tsx`
Chat interface with:
- Header (app name, user info)
- ChatKit component (messages, input)
- Error handling (toast notifications)
- Loading indicators
- Responsive design

## Components

### ChatKit Integration
```tsx
<ChatKit
  messages={messages}
  onSendMessage={handleSendMessage}
  isLoading={isLoading}
  domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
  placeholder="Ask me to add tasks, show your list..."
/>
```

### Message Flow
1. User types message
2. Display immediately (optimistic UI)
3. Send to `/api/chat` with JWT
4. Show loading indicator
5. Receive response
6. Display assistant message
7. Update conversation_id

## API Client
```typescript
// lib/chat-api.ts
export async function sendChatMessage({
  message,
  conversation_id,
  token
}: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${API_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message, conversation_id })
  });
  return response.json();
}
```

## Styling
- Tailwind CSS
- User messages: right-aligned, blue background
- Assistant messages: left-aligned, gray background
- Responsive (mobile + desktop)
- Typing indicator during loading

## Error Handling
- Network errors: "Failed to send. Try again."
- 401 errors: Redirect to login
- Show error toast (dismissible)
- Remove user message on error

## Authentication
- Check user logged in
- Redirect to /login if not
- Attach JWT to all requests
- Handle token expiry
