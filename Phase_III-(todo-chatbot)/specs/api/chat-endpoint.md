# API: Chat Endpoint

## Endpoint
```
POST /api/{user_id}/chat
```

## Authentication
```
Authorization: Bearer <jwt_token>
```

## Request
```json
{
  "conversation_id": 123,
  "message": "Add task to buy groceries"
}
```

## Response
```json
{
  "conversation_id": 123,
  "response": "Got it! I've added 'Buy groceries' 📝",
  "tool_calls": [
    {"tool": "add_task", "arguments": "{...}"}
  ]
}
```

## Flow
1. Validate JWT
2. Get/create conversation
3. Fetch history (DB)
4. Store user message
5. Run AI agent with MCP tools
6. Store assistant response
7. Return response

## Examples

### Start conversation
```http
POST /api/user123/chat
{
  "message": "Add task to buy milk"
}
```
Response: `{"conversation_id": 456, "response": "Done! Added 'Buy milk'"}`

### Continue conversation
```http
POST /api/user123/chat
{
  "conversation_id": 456,
  "message": "What's on my list?"
}
```
Response: `{"conversation_id": 456, "response": "You have 1 task: Buy milk"}`

## Errors
- 401: Invalid token
- 403: user_id mismatch
- 404: Conversation not found
- 500: Processing failed

## Stateless
- Fetches all context from DB
- Stores all results
- Any server handles any request
