# Skill: Generate Helm Chart

## Purpose
Creates production-grade Kubernetes Helm charts with best practices

## When to Use
- Phase IV local deployment
- Phase V cloud deployment
- Creating reusable deployment blueprints

## Prompt
Generate Helm chart for {{application_name}} with these services:
{{services_list}}

Include:
1. **Chart.yaml**: Metadata, version, dependencies
2. **values.yaml**: Configurable parameters
3. **templates/deployment.yaml**: For each service
4. **templates/service.yaml**: ClusterIP/LoadBalancer configs
5. **templates/ingress.yaml**: Routing rules if needed
6. **templates/configmap.yaml**: Non-secret configs
7. **templates/secret.yaml**: Sensitive data (reference only)
8. **templates/hpa.yaml**: Horizontal pod autoscaling if {{autoscaling_required}}

Configuration:
- Replicas: {{replica_count}}
- Resource limits: {{resource_limits}}
- Health checks: {{health_check_paths}}
- Environment: {{environment}} (minikube/cloud)

Follow Kubernetes best practices for {{cluster_type}}.