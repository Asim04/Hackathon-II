# MCP Tools

## Principles
1. Stateless (no memory)
2. Database-backed
3. User-scoped (require user_id)
4. Consistent response format
5. Graceful errors

---

## Tool 1: add_task

### Input
```json
{
  "user_id": "string",
  "title": "string (1-200 chars)",
  "description": "string (optional, max 1000)"
}
```

### Output
```json
{"task_id": 5, "status": "created", "title": "Buy groceries"}
```

### Example
Input: `{"user_id": "user123", "title": "Buy groceries"}`
Output: `{"task_id": 5, "status": "created", "title": "Buy groceries"}`

---

## Tool 2: list_tasks

### Input
```json
{
  "user_id": "string",
  "status": "all|pending|completed"
}
```

### Output
```json
[
  {"id": 1, "title": "Buy groceries", "completed": false},
  {"id": 2, "title": "Call dentist", "completed": false}
]
```

---

## Tool 3: complete_task

### Input
```json
{
  "user_id": "string",
  "task_id": 123
}
```

### Output
```json
{"task_id": 3, "status": "completed", "title": "Call dentist"}
```

---

## Tool 4: delete_task

### Input
```json
{
  "user_id": "string",
  "task_id": 123
}
```

### Output
```json
{"task_id": 2, "status": "deleted", "title": "Old meeting"}
```

---

## Tool 5: update_task

### Input
```json
{
  "user_id": "string",
  "task_id": 123,
  "title": "string (optional)",
  "description": "string (optional)"
}
```

### Output
```json
{"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}
```

---

## Error Format
```json
{
  "error": "not_found|validation_error|internal_error",
  "message": "Task 99 not found"
}
```

## Security
- Verify user_id
- Filter by user_id
- Prevent cross-user access
- Validate inputs (JSON Schema)
