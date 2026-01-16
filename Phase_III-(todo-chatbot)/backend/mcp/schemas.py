"""
JSON Schemas for MCP tool input validation.

All schemas follow JSON Schema Draft 7 specification.
"""

# Schema for add_task tool
ADD_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "UUID of the user creating the task"
        },
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200,
            "description": "Task title (1-200 characters)"
        },
        "description": {
            "type": "string",
            "maxLength": 1000,
            "description": "Optional task description (max 1000 characters)"
        }
    },
    "required": ["user_id", "title"],
    "additionalProperties": False
}

# Schema for list_tasks tool
LIST_TASKS_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "UUID of the user"
        },
        "status": {
            "type": "string",
            "enum": ["all", "pending", "completed"],
            "default": "all",
            "description": "Filter tasks by status"
        }
    },
    "required": ["user_id"],
    "additionalProperties": False
}

# Schema for complete_task tool
COMPLETE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "UUID of the user"
        },
        "task_id": {
            "type": "integer",
            "minimum": 1,
            "description": "ID of the task to complete"
        }
    },
    "required": ["user_id", "task_id"],
    "additionalProperties": False
}

# Schema for delete_task tool
DELETE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "UUID of the user"
        },
        "task_id": {
            "type": "integer",
            "minimum": 1,
            "description": "ID of the task to delete"
        }
    },
    "required": ["user_id", "task_id"],
    "additionalProperties": False
}

# Schema for update_task tool
UPDATE_TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string",
            "description": "UUID of the user"
        },
        "task_id": {
            "type": "integer",
            "minimum": 1,
            "description": "ID of the task to update"
        },
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200,
            "description": "New task title (optional)"
        },
        "description": {
            "type": "string",
            "maxLength": 1000,
            "description": "New task description (optional)"
        }
    },
    "required": ["user_id", "task_id"],
    "additionalProperties": False
}
