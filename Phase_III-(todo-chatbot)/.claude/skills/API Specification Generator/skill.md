# Skill: Generate API Specification

## Purpose
Creates complete REST API or MCP tool specifications

## When to Use
- Designing backend endpoints
- Creating MCP tools for AI agents
- Documenting API contracts

## Prompt
Generate API specification for {{api_type}} (REST/MCP) endpoints for {{feature_name}}.

For REST APIs include:
- Base URL
- Authentication method: {{auth_method}}
- All endpoints with HTTP methods
- Request/response schemas
- Status codes and error handling
- Query parameters and filters

For MCP Tools include:
- Tool name and purpose
- Input parameters with types and validation
- Return schema
- Example inputs/outputs
- Error cases

Current tech stack: {{backend_stack}}
Database: {{database_type}}
Authentication: {{auth_system}}

Save to /specs/api/{{feature_name}}-endpoints.md