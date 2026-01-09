# Skill: Implement MCP Server

## Purpose
Creates complete MCP server with tools following Official MCP SDK patterns

## When to Use
- Phase III AI chatbot integration
- Adding AI agent capabilities
- Exposing backend operations as tools

## Prompt
Implement MCP server for {{feature_name}} with these tools:
{{tools_list}}

For each tool generate:
1. **Tool Schema**: Name, description, parameters with JSON Schema
2. **Implementation**: Python function using Official MCP SDK
3. **Database Integration**: {{orm}} queries for {{database}}
4. **Error Handling**: Validation, not found, conflicts
5. **Response Format**: Consistent success/error structure

Requirements:
- User isolation: Filter by {{user_id_field}}
- Stateless: All state in {{database}}
- Authentication: Verify {{auth_token}}
- Validation: {{validation_rules}}

Tech stack: {{mcp_stack}}
Follow Official MCP SDK best practices.