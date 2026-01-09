# Skill: Configure Dapr Components

## Purpose
Creates Dapr component configurations for microservices building blocks

## When to Use
- Phase V event-driven architecture
- Adding Pub/Sub, State, Bindings
- Abstracting infrastructure

## Prompt
Create Dapr component configuration for {{component_type}}:

**Pub/Sub (Kafka)**:
- Brokers: {{kafka_brokers}}
- Topics: {{topics_list}}
- Consumer group: {{consumer_group}}

**State Store (PostgreSQL)**:
- Connection string: (reference secret)
- Table name: {{table_name}}

**Secrets (Kubernetes)**:
- Secret names: {{secret_names}}

**Bindings (Cron/Jobs API)**:
- Schedule: {{cron_schedule}}
- Callback endpoint: {{callback_path}}

**Service Invocation**:
- App ID: {{app_id}}
- Namespace: {{namespace}}

Generate complete YAML component files for {{environment}} (local/cloud).
Include metadata, spec, and proper secret referencing.