# Skill: Create Cloud-Native Deployment Blueprint

## Purpose
Generates reusable deployment blueprints for spec-driven infrastructure

## When to Use
- Bonus points: Blueprint creation
- Standardizing deployments
- Creating infrastructure templates

## Prompt
Create cloud-native blueprint for {{application_type}} on {{cloud_provider}}.

Blueprint should include:
1. **Specification Template**: YAML/JSON schema for deployment config
2. **Helm Chart Template**: Parameterized charts
3. **Dapr Components**: Configurable by environment
4. **Networking**: Ingress, service mesh configs
5. **Monitoring**: Logging, metrics setup
6. **Security**: RBAC, network policies, secrets management

Make it reusable for:
- Different environments: {{environments}}
- Different scales: {{scale_sizes}}
- Different cloud providers: {{providers}}

Generate as Agent Skill that Claude Code can use for instant deployments.
```

---

## **Kaise Use Karein**

### **Claude Code mein Skills Add karna:**

1. **Skills panel** open karein (Claude.ai)
2. **"Create new skill"** click karein
3. Upar diye gaye skill prompts copy-paste karein
4. Variables `{{variable_name}}` ko customize karein
5. Save karke test karein

### **Skill Execution:**
```
You: Use "Initialize Spec-Driven Project Structure" skill
     project_name: "hackathon-todo"
     phase_number: "II"
     tech_stack: "Next.js, FastAPI, Neon DB"