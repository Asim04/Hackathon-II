/**
 * Chat API Client
 *
 * Provides functions for interacting with the chat API endpoints.
 */

import api from './api';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: number | null;
}

export interface ChatResponse {
  conversation_id: number;
  message: string;
  tool_calls: Array<{
    tool: string;
    arguments: Record<string, any>;
    result: Record<string, any>;
  }>;
}

export interface Conversation {
  id: number;
  created_at: string;
  updated_at: string;
  message_count: number;
}

/**
 * Send a chat message to the AI assistant
 */
export async function sendChatMessage(
  userId: string,
  request: ChatRequest
): Promise<ChatResponse> {
  const response = await api.post(`/api/${userId}/chat`, request);
  return response.data;
}

/**
 * List all conversations for the user
 */
export async function listConversations(userId: string): Promise<Conversation[]> {
  const response = await api.get(`/api/${userId}/chat/conversations`);
  return response.data;
}

/**
 * Delete a conversation
 */
export async function deleteConversation(
  userId: string,
  conversationId: number
): Promise<void> {
  await api.delete(`/api/${userId}/chat/conversations/${conversationId}`);
}
