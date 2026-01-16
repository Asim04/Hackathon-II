import ChatClient from './ChatClient';

// Force dynamic rendering for authenticated routes
export const dynamic = 'force-dynamic';

export default function ChatPage() {
  return <ChatClient />;
}
