# Skill: Design Database Schema

## Purpose
Creates complete database schema specifications with relationships and indexes

## When to Use
- Adding new data models
- Modifying existing schemas
- Planning database migrations

## Prompt
Design database schema for {{feature_name}} using {{orm}} and {{database}}.

Requirements:
{{requirements}}

Include:
1. **Tables**: All fields with types, constraints, defaults
2. **Relationships**: Foreign keys, junction tables
3. **Indexes**: Performance-critical lookups
4. **Migrations**: Creation order, dependencies
5. **Seed Data**: Initial/test data if needed

Consider:
- User isolation (multi-tenant): {{user_isolation_required}}
- Existing models: {{existing_models}}
- Query patterns: {{query_patterns}}

Format as /specs/database/{{feature_name}}-schema.md with SQL examples.