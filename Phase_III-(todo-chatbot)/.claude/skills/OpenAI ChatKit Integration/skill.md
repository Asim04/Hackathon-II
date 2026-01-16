# Skill: OpenAI ChatKit Integration

Create the file: `.spec-kit/skills/chatkit-integration.md`

---

# Skill: OpenAI ChatKit Integration

## Description
Integrate OpenAI ChatKit into React/Next.js applications for building conversational interfaces quickly.

## What is ChatKit?
OpenAI ChatKit is a pre-built React component library for creating chat interfaces. It handles:
- Message display and formatting
- User input field
- Loading states
- Conversation UI
- Responsive design
- Typing indicators

## Capabilities
- Install and configure ChatKit
- Build chat UI components
- Handle message sending/receiving
- Display conversation history
- Show typing indicators
- Handle authentication
- Configure domain allowlist (production)
- Style chat interface with Tailwind

## Setup Steps

### 1. Installation
```bash
npm install @openai/chatkit
```

### 2. Environment Variables
```bash
# .env.local
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-here
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Domain Allowlist (Production Only)
For production deployment:
1. Deploy frontend to get URL (e.g., `https://your-app.vercel.app`)
2. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Click "Add domain"
4. Enter your frontend URL (without trailing slash)
5. Save and copy the domain key
6. Add to environment: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY=generated-key`

**Note:** Local development (`localhost`) works without domain allowlist.

## Code Patterns

### Basic ChatKit Setup
```typescript
// app/chat/page.tsx
'use client';

import { ChatKit } from '@openai/chatkit';
import { useState } from 'react';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;
    
    // Add user message to UI immediately
    const userMessage = { role: 'user', content: message };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    try {
      // Send to backend
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: message
        })
      });
      
      const data = await response.json();
      
      // Update conversation ID (first message)
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }
      
      // Add assistant response
      const assistantMessage = {
        role: 'assistant',
        content: data.response
      };
      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (error) {
      console.error('Chat error:', error);
      // Remove user message on error
      setMessages(prev => prev.slice(0, -1));
      alert('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="h-screen flex flex-col">
      <ChatKit
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
        placeholder="Ask me to add tasks, show your list, or mark tasks complete..."
      />
    </div>
  );
}
```

### With Authentication
```typescript
// app/chat/page.tsx
'use client';

import { ChatKit } from '@openai/chatkit';
import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { sendChatMessage } from '@/lib/chat-api';

export default function AuthenticatedChat() {
  const { user, token } = useAuth();
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  // Redirect if not authenticated
  useEffect(() => {
    if (!user) {
      window.location.href = '/login';
    }
  }, [user]);
  
  const handleSendMessage = async (message: string) => {
    if (!message.trim() || !token) return;
    
    const userMessage = { role: 'user', content: message };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    
    try {
      const response = await sendChatMessage({
        message,
        conversation_id: conversationId,
        token
      });
      
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }
      
      const assistantMessage = {
        role: 'assistant',
        content: response.response
      };
      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => prev.slice(0, -1));
      
      // Handle 401 (token expired)
      if (error.message.includes('401')) {
        window.location.href = '/login';
      }
    } finally {
      setIsLoading(false);
    }
  };
  
  if (!user) {
    return <div>Loading...</div>;
  }
  
  return (
    <div className="h-screen">
      <ChatKit
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
        domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
      />
    </div>
  );
}
```

### API Client
```typescript
// lib/chat-api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ChatRequest {
  message: string;
  conversation_id?: number;
  token: string;
}

interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: Array<{
    tool: string;
    arguments: string;
  }>;
}

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
    body: JSON.stringify({
      message,
      conversation_id
    })
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Chat API error: ${response.status} - ${errorText}`);
  }
  
  return response.json();
}
```

### Custom Styling
```typescript
// Styled ChatKit
<ChatKit
  messages={messages}
  onSendMessage={handleSendMessage}
  isLoading={isLoading}
  theme={{
    primaryColor: '#3b82f6',      // Blue
    backgroundColor: '#f9fafb',    // Light gray
    messageUserBg: '#3b82f6',      // User message background
    messageAssistantBg: '#e5e7eb', // Assistant message background
    messageColor: '#1f2937'        // Text color
  }}
  className="custom-chat"
/>
```

### Tailwind Customization
```css
/* globals.css */

.custom-chat {
  @apply rounded-lg shadow-lg border border-gray-200;
}

.custom-chat .message-user {
  @apply bg-blue-500 text-white rounded-lg p-3 max-w-md ml-auto;
}

.custom-chat .message-assistant {
  @apply bg-gray-200 text-gray-900 rounded-lg p-3 max-w-md mr-auto;
}

.custom-chat .input-field {
  @apply border-2 border-gray-300 rounded-lg p-2 focus:border-blue-500;
}

.custom-chat .send-button {
  @apply bg-blue-500 hover:bg-blue-600 text-white rounded-lg px-4 py-2;
}
```

### Complete Chat Page with Header
```typescript
// app/chat/page.tsx
'use client';

import { ChatKit } from '@openai/chatkit';
import { useState } from 'react';
import { useAuth } from '@/lib/auth';

export default function ChatPage() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const handleSendMessage = async (message: string) => {
    // Implementation from above...
  };
  
  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-xl font-bold">Todo Assistant</h1>
            <p className="text-sm text-blue-100">
              Manage your tasks with AI
            </p>
          </div>
          <div className="text-sm">
            👤 {user?.name || 'Guest'}
          </div>
        </div>
      </header>
      
      {/* Chat Interface */}
      <div className="flex-1 max-w-4xl mx-auto w-full overflow-hidden">
        <ChatKit
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
          placeholder="Try: 'Add a task to buy milk' or 'Show my tasks'"
          className="h-full"
        />
      </div>
      
      {/* Error Toast */}
      {error && (
        <div className="fixed bottom-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded shadow-lg">
          <button
            onClick={() => setError(null)}
            className="float-right font-bold ml-4"
          >
            ×
          </button>
          {error}
        </div>
      )}
    </div>
  );
}
```

### Loading State with Typing Indicator
```typescript
const [isTyping, setIsTyping] = useState(false);

const handleSendMessage = async (message: string) => {
  // Add user message
  setMessages(prev => [...prev, { role: 'user', content: message }]);
  setIsTyping(true);
  
  try {
    const response = await sendChatMessage(...);
    
    // Add assistant response
    setMessages(prev => [
      ...prev,
      { role: 'assistant', content: response.response }
    ]);
  } finally {
    setIsTyping(false);
  }
};

// In JSX
<ChatKit
  messages={messages}
  onSendMessage={handleSendMessage}
  isLoading={isTyping}
  loadingMessage="Assistant is thinking..."
/>
```

## Error Handling
```typescript
// Handle network errors
const handleSendMessage = async (message: string) => {
  try {
    const response = await sendChatMessage(...);
    // Success...
  } catch (error) {
    // Specific error handling
    if (error.message.includes('401')) {
      setError('Session expired. Please log in again.');
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
    } else if (error.message.includes('Network')) {
      setError('Network error. Please check your connection.');
    } else {
      setError('Failed to send message. Please try again.');
    }
    
    // Remove user message on error
    setMessages(prev => prev.slice(0, -1));
  }
};
```

## Conversation History Loading
```typescript
// Load conversation history on mount
useEffect(() => {
  const loadConversation = async () => {
    if (conversationId) {
      try {
        const response = await fetch(
          `${API_URL}/api/conversations/${conversationId}/messages`,
          {
            headers: { 'Authorization': `Bearer ${token}` }
          }
        );
        const data = await response.json();
        
        setMessages(data.messages);
      } catch (error) {
        console.error('Failed to load conversation:', error);
      }
    }
  };
  
  loadConversation();
}, [conversationId]);
```

## Responsive Design
```typescript
<div className="h-screen flex flex-col">
  {/* Mobile-friendly header */}
  <header className="bg-blue-600 text-white p-4 sm:p-6">
    <h1 className="text-lg sm:text-xl font-bold">Todo Assistant</h1>
  </header>
  
  {/* Responsive chat container */}
  <div className="flex-1 overflow-hidden px-2 sm:px-4 md:px-8">
    <ChatKit
      messages={messages}
      onSendMessage={handleSendMessage}
      className="h-full max-w-4xl mx-auto"
    />
  </div>
</div>
```

## Testing ChatKit Component
```typescript
// __tests__/chat.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import ChatPage from '@/app/chat/page';

describe('ChatPage', () => {
  it('renders chat interface', () => {
    render(<ChatPage />);
    expect(screen.getByPlaceholderText(/add tasks/i)).toBeInTheDocument();
  });
  
  it('sends message on submit', async () => {
    render(<ChatPage />);
    const input = screen.getByPlaceholderText(/add tasks/i);
    const sendButton = screen.getByRole('button', { name: /send/i });
    
    fireEvent.change(input, { target: { value: 'Add task: buy milk' } });
    fireEvent.click(sendButton);
    
    // Assert message appears
    expect(await screen.findByText(/buy milk/i)).toBeInTheDocument();
  });
});
```

## Dependencies
```json
{
  "dependencies": {
    "@openai/chatkit": "^1.0.0",
    "react": "^18.0.0",
    "next": "^14.0.0"
  }
}
```

## Key Takeaways
1. ✅ **Quick setup** - Pre-built UI components
2. ✅ **Domain allowlist** - Required for production
3. ✅ **Authentication** - Integrate with JWT tokens
4. ✅ **Error handling** - Graceful network failures
5. ✅ **Styling** - Customizable with Tailwind
6. ✅ **Responsive** - Mobile-friendly design