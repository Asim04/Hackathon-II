# Skill: Containerize Application

## Purpose
Creates production-ready Dockerfiles and docker-compose configurations

## When to Use
- Phase IV containerization
- Preparing for Kubernetes deployment
- Local development setup

## Prompt
Create Docker configuration for {{service_name}} ({{service_type}}: frontend/backend/database).

Requirements:
- Base image: {{base_image}}
- Runtime: {{runtime}}
- Port: {{port}}
- Environment variables: {{env_vars}}
- Build optimization: Multi-stage builds, layer caching
- Security: Non-root user, minimal dependencies

For docker-compose.yml include:
- All services: {{services_list}}
- Networks and volumes
- Health checks
- Restart policies
- Environment variable files

Optimize for:
- Build speed: {{build_speed_priority}}
- Image size: {{image_size_priority}}
- Development vs Production: {{environment}}