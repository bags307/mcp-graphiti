# Graphiti Common Patterns and Solutions

## Entity Extraction Patterns

### Pattern 1: User Preferences

**Signals to Look For**:
- "I prefer..."
- "I like to..."
- "Always use..."
- "Never do..."
- "My favorite is..."

**Extraction Example**:
```python
# Input: "I prefer using async/await over callbacks in JavaScript"
await mcp__graphiti__add_episode(
    name="JavaScript Async Preference",
    episode_body={
        "preference": {
            "category": "javascript_patterns",
            "preferred": "async/await",
            "avoided": "callbacks",
            "strength": "strong"
        }
    },
    format="json"
)
```

### Pattern 2: Step-by-Step Procedures

**Signals to Look For**:
- "First..., then..., finally..."
- "The process is..."
- "To do X, you need to..."
- Numbered lists
- Sequential instructions

**Extraction Example**:
```python
# Input: "To deploy: 1) Run tests 2) Build the app 3) Push to staging 4) Verify 5) Push to prod"
await mcp__graphiti__add_episode(
    name="Deployment Procedure",
    episode_body={
        "procedure": {
            "name": "Standard Deployment",
            "steps": [
                {"order": 1, "action": "Run tests", "command": "npm test"},
                {"order": 2, "action": "Build application", "command": "npm run build"},
                {"order": 3, "action": "Deploy to staging", "command": "deploy staging"},
                {"order": 4, "action": "Verify staging", "command": "verify staging"},
                {"order": 5, "action": "Deploy to production", "command": "deploy prod"}
            ],
            "prerequisites": ["All tests passing", "Code reviewed"]
        }
    },
    format="json"
)
```

### Pattern 3: Technical Decisions

**Signals to Look For**:
- "We decided to use..."
- "We chose X over Y because..."
- "The architecture will be..."
- "We're going with..."

**Extraction Example**:
```python
# Input: "We decided to use PostgreSQL over MongoDB because we need ACID compliance"
await mcp__graphiti__add_episode(
    name="Database Selection Decision",
    episode_body={
        "technical_decision": {
            "area": "database",
            "chosen": "PostgreSQL",
            "alternatives": ["MongoDB", "MySQL"],
            "reasons": ["ACID compliance required", "Complex relationships", "SQL familiarity"],
            "date": "2024-01-15"
        }
    },
    format="json"
)
```

### Pattern 4: Bug Reports and Issues

**Signals to Look For**:
- "There's a bug..."
- "X is broken"
- "Getting an error..."
- "X doesn't work when..."
- Error messages

**Extraction Example**:
```python
# Input: "Login fails with 500 error when email contains special characters"
await mcp__graphiti__add_episode(
    name="Login Bug Report",
    episode_body={
        "bug_report": {
            "component": "Authentication",
            "severity": "high",
            "description": "Login fails with HTTP 500 error",
            "conditions": "When email contains special characters like + or .",
            "error_message": "Internal Server Error (500)",
            "reported_date": "2024-01-20"
        }
    },
    format="json"
)
```

### Pattern 5: Requirements and Constraints

**Signals to Look For**:
- "Must have..."
- "Should support..."
- "Needs to..."
- "Required to..."
- "Cannot exceed..."

**Extraction Example**:
```python
# Input: "The API must handle 1000 requests per second and respond within 200ms"
await mcp__graphiti__add_episode(
    name="API Performance Requirements",
    episode_body={
        "requirement": {
            "type": "performance",
            "component": "API",
            "criteria": [
                {"metric": "throughput", "value": 1000, "unit": "requests/second"},
                {"metric": "latency", "value": 200, "unit": "milliseconds", "percentile": "p99"}
            ],
            "priority": "critical"
        }
    },
    format="json"
)
```

## Relationship Patterns

### Pattern 1: Dependencies

**Common Relationships**:
- Component A DEPENDS_ON Component B
- Service X REQUIRES Service Y
- Module M IMPORTS Module N

**Example**:
```python
# When user mentions: "The auth service needs the user database to be running"
await mcp__graphiti__add_episode(
    name="Service Dependencies",
    episode_body={
        "services": {
            "auth_service": {"type": "service", "name": "Authentication Service"},
            "user_db": {"type": "database", "name": "User Database"}
        },
        "relationships": [
            {"from": "auth_service", "to": "user_db", "type": "DEPENDS_ON"}
        ]
    },
    format="json"
)
```

### Pattern 2: Ownership and Responsibility

**Common Relationships**:
- Developer OWNS Component
- Team MAINTAINS Service
- Person RESPONSIBLE_FOR Task

**Example**:
```python
# When user mentions: "Alice is the lead developer for the payment module"
await mcp__graphiti__add_episode(
    name="Module Ownership",
    episode_body={
        "entities": {
            "alice": {"type": "developer", "name": "Alice", "role": "Lead Developer"},
            "payment_module": {"type": "component", "name": "Payment Module"}
        },
        "relationships": [
            {"from": "alice", "to": "payment_module", "type": "OWNS", "since": "2023-06"}
        ]
    },
    format="json"
)
```

### Pattern 3: Implementation Relationships

**Common Relationships**:
- Component IMPLEMENTS Requirement
- Feature SATISFIES Goal
- Solution ADDRESSES Problem

**Example**:
```python
# When user mentions: "The caching layer implements the performance requirement"
await mcp__graphiti__add_episode(
    name="Requirement Implementation",
    episode_body={
        "entities": {
            "caching_layer": {"type": "component", "name": "Redis Cache Layer"},
            "perf_req": {"type": "requirement", "name": "Sub-100ms response time"}
        },
        "relationships": [
            {"from": "caching_layer", "to": "perf_req", "type": "IMPLEMENTS"}
        ]
    },
    format="json"
)
```

## Search Strategy Patterns

### Pattern 1: Contextual Search

**When to Use**: Need to find related information around a known entity

```python
# First, find the main entity
main_result = await mcp__graphiti__search_nodes(
    query="payment service",
    max_nodes=1
)

if main_result["nodes"]:
    # Then search for related information
    uuid = main_result["nodes"][0]["uuid"]
    
    # Find dependencies
    deps = await mcp__graphiti__search_facts(
        query="depends on",
        center_node_uuid=uuid
    )
    
    # Find related procedures
    procs = await mcp__graphiti__search_nodes(
        query="deployment configuration",
        center_node_uuid=uuid,
        entity="Procedure"
    )
```

### Pattern 2: Progressive Refinement

**When to Use**: Initial search too broad or too narrow

```python
# Start broad
results = await mcp__graphiti__search_nodes(
    query="authentication",
    max_nodes=20
)

# If too many results, refine with entity filter
if len(results["nodes"]) > 10:
    results = await mcp__graphiti__search_nodes(
        query="authentication",
        entity="Procedure",
        max_nodes=10
    )

# If still not specific enough, add more context
if len(results["nodes"]) > 5:
    results = await mcp__graphiti__search_nodes(
        query="authentication login flow",
        entity="Procedure",
        max_nodes=5
    )
```

### Pattern 3: Fact-First Search

**When to Use**: Looking for relationships rather than entities

```python
# Search for all "implements" relationships
implementations = await mcp__graphiti__search_facts(
    query="implements",
    max_facts=20
)

# Extract unique components that implement something
implementing_components = set()
for fact in implementations["facts"]:
    implementing_components.add(fact["source_node_uuid"])

# Get details about those components
for uuid in implementing_components:
    node = await mcp__graphiti__search_nodes(
        query="",
        center_node_uuid=uuid,
        max_nodes=1
    )
```

## Data Organization Patterns

### Pattern 1: Hierarchical Information

**When to Use**: Representing parent-child or nested relationships

```python
# Organization structure
await mcp__graphiti__add_episode(
    name="Team Structure",
    episode_body={
        "organization": {
            "name": "Engineering",
            "teams": [
                {
                    "name": "Backend",
                    "lead": "Bob",
                    "members": ["Alice", "Charlie"]
                },
                {
                    "name": "Frontend", 
                    "lead": "Dana",
                    "members": ["Eve", "Frank"]
                }
            ]
        }
    },
    format="json"
)
```

### Pattern 2: Timeline-Based Information

**When to Use**: Tracking events, changes, or history

```python
# Project timeline
await mcp__graphiti__add_episode(
    name="Project Milestones",
    episode_body={
        "project": "API v2",
        "timeline": [
            {"date": "2024-01-01", "event": "Project kickoff"},
            {"date": "2024-02-15", "event": "Design complete"},
            {"date": "2024-04-01", "event": "Beta release"},
            {"date": "2024-05-01", "event": "Production release"}
        ]
    },
    format="json"
)
```

### Pattern 3: Configuration and Settings

**When to Use**: Storing system or user configurations

```python
# System configuration
await mcp__graphiti__add_episode(
    name="Production Environment Config",
    episode_body={
        "environment": "production",
        "configuration": {
            "database": {
                "type": "postgresql",
                "pool_size": 20,
                "timeout": 30
            },
            "cache": {
                "type": "redis",
                "ttl": 3600,
                "max_memory": "2GB"
            },
            "api": {
                "rate_limit": 1000,
                "timeout": 60
            }
        }
    },
    format="json"
)
```

## Error Handling Patterns

### Pattern 1: Validation Before Adding

```python
# Check if entity already exists
existing = await mcp__graphiti__search_nodes(
    query=f'name:"{exact_name}"',
    max_nodes=1
)

if existing["nodes"]:
    print(f"Entity already exists: {existing['nodes'][0]['uuid']}")
    # Update existing entity instead of creating duplicate
else:
    # Safe to create new entity
    await mcp__graphiti__add_episode(...)
```

### Pattern 2: Handling Large Datasets

```python
# Break large data into chunks
large_dataset = [...] # Many items

chunk_size = 50
for i in range(0, len(large_dataset), chunk_size):
    chunk = large_dataset[i:i + chunk_size]
    
    await mcp__graphiti__add_episode(
        name=f"Data Import Chunk {i//chunk_size + 1}",
        episode_body={
            "batch_number": i//chunk_size + 1,
            "items": chunk
        },
        format="json"
    )
```

### Pattern 3: Retry Logic

```python
async def add_episode_with_retry(name, body, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = await mcp__graphiti__add_episode(
                name=name,
                episode_body=body,
                format="json"
            )
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            # Wait before retry
            await asyncio.sleep(2 ** attempt)
```

## Best Practices Summary

1. **Use Structured Data**: JSON format enables better entity extraction
2. **Be Specific**: Clear, specific names and descriptions improve searchability
3. **Avoid Duplication**: Always search before adding
4. **Group Related Data**: Combine related information in single episodes
5. **Use Consistent Naming**: Follow project conventions for entities and relationships
6. **Include Metadata**: Add dates, sources, and context
7. **Handle Errors Gracefully**: Validate, retry, and provide fallbacks
8. **Think in Graphs**: Model data as nodes and relationships
9. **Progressive Enhancement**: Start simple, add complexity as needed
10. **Document Patterns**: Record successful patterns for team reuse