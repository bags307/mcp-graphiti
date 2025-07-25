# Graphiti MCP Tools Quick Reference

## Available Tools

### 🔍 Search Tools

#### mcp__graphiti__search_nodes
Search for entities in the knowledge graph.

```python
await mcp__graphiti__search_nodes(
    query="search terms",           # Required: What to search for
    entity="Preference",           # Optional: Filter by entity type
    max_nodes=10,                  # Optional: Limit results (default: 10)
    center_node_uuid="uuid",       # Optional: Search around specific node
    group_ids=["group1"]          # Optional: Filter by groups
)
```

**Common entity filters**: `"Preference"`, `"Procedure"`, `"Requirement"`, `"Goal"`, `"Project"`

#### mcp__graphiti__search_facts
Search for relationships between entities.

```python
await mcp__graphiti__search_facts(
    query="search terms",          # Required: What to search for
    max_facts=10,                  # Optional: Limit results (default: 10)
    center_node_uuid="uuid",       # Optional: Search around specific node
    group_ids=["group1"]          # Optional: Filter by groups
)
```

### ✏️ Write Tools

#### mcp__graphiti__add_episode
Add new information to the knowledge graph.

```python
# Text format (default)
await mcp__graphiti__add_episode(
    name="Episode Title",          # Required: Descriptive name
    episode_body="Content here",   # Required: The actual content
    format="text",                 # Optional: "text"|"json"|"message"
    source_description="context",  # Optional: Where this came from
    entity_subset=["Entity1"],     # Optional: Limit entity extraction
    group_id="group",             # Optional: Usually omit
    uuid="custom-uuid"            # Optional: Usually omit
)

# JSON format (auto-extracts entities)
await mcp__graphiti__add_episode(
    name="Structured Data",
    episode_body={                 # Pass dict directly
        "user": {"name": "John", "role": "Developer"},
        "preference": "Dark mode"
    },
    format="json"
)
```

### 📖 Read Tools

#### mcp__graphiti__get_episodes
Retrieve recent episodes.

```python
await mcp__graphiti__get_episodes(
    group_id="group",             # Optional: Specific group
    last_n=10                     # Optional: Number to retrieve (default: 10)
)
```

#### mcp__graphiti__get_entity_edge
Get specific entity relationship by UUID.

```python
await mcp__graphiti__get_entity_edge(
    uuid="edge-uuid"              # Required: UUID of the edge
)
```

### 🗑️ Delete Tools

#### mcp__graphiti__delete_episode
Remove an episode from the graph.

```python
await mcp__graphiti__delete_episode(
    uuid="episode-uuid"           # Required: UUID of episode to delete
)
```

#### mcp__graphiti__delete_entity_edge
Remove a relationship from the graph.

```python
await mcp__graphiti__delete_entity_edge(
    uuid="edge-uuid"              # Required: UUID of edge to delete
)
```

### ⚠️ Danger Zone

#### mcp__graphiti__clear_graph
**WARNING**: Permanently deletes ALL data in the graph!

```python
# First call - get authorization code
response = await mcp__graphiti__clear_graph()
# Returns: {"auth_code": "a1b2c3d4"}

# Second call - confirm deletion
await mcp__graphiti__clear_graph(
    auth="a1b2c3d4_DELETE_THIS_GRAPH"  # Code + "_DELETE_THIS_GRAPH"
)
```

## Common Patterns

### 1. Search Before Adding
```python
# Always check for existing information
existing = await mcp__graphiti__search_nodes(
    query="deployment process",
    entity="Procedure"
)

if not existing["nodes"]:
    # Safe to add new procedure
    await mcp__graphiti__add_episode(
        name="Deployment Procedure",
        episode_body="Steps for deployment...",
        format="text"
    )
```

### 2. Capture User Preferences
```python
await mcp__graphiti__add_episode(
    name="Code Style Preference",
    episode_body="User prefers tabs over spaces for Python code",
    format="text"
)
```

### 3. Document Complex Procedures
```python
procedure_data = {
    "procedure": {
        "name": "Code Review Process",
        "steps": [
            "Create pull request",
            "Automated tests must pass",
            "Two approvals required",
            "Merge to main branch"
        ],
        "requirements": ["All tests passing", "No merge conflicts"]
    }
}

await mcp__graphiti__add_episode(
    name="Code Review Procedure",
    episode_body=procedure_data,
    format="json"
)
```

### 4. Track Project Information
```python
project_data = {
    "project": {
        "name": "API Redesign",
        "status": "in_progress",
        "team": ["Alice", "Bob", "Charlie"],
        "deadline": "2024-Q2",
        "goals": [
            "Improve response times by 50%",
            "Add GraphQL support"
        ]
    }
}

await mcp__graphiti__add_episode(
    name="API Redesign Project",
    episode_body=project_data,
    format="json"
)
```

### 5. Search with Context
```python
# Find related information
main_node = await mcp__graphiti__search_nodes(
    query="authentication service"
)

if main_node["nodes"]:
    node_uuid = main_node["nodes"][0]["uuid"]
    
    # Find related facts
    related = await mcp__graphiti__search_facts(
        query="dependencies",
        center_node_uuid=node_uuid
    )
```

## Entity Types Reference

### Core Entities
- **Preference**: User preferences and choices
- **Procedure**: Step-by-step processes
- **Requirement**: Needs and specifications  
- **Goal**: Objectives and targets
- **Project**: Initiatives and their details
- **Action**: Discrete performable actions
- **Developer**: Developer context and patterns
- **Tool**: Available tools and utilities

### Development Entities
- **TechnicalDecision**: Architecture choices
- **BugReport**: Issues and errors
- **CodeChange**: Modifications to code

### Interaction Entities
- **InteractionModel**: Interaction patterns
- **Feedback**: User or system feedback

### Resource Entities
- **Artifact**: Files, datasets, models
- **Documentation**: Guides and references
- **Resource**: General assets

## Format Parameter Guide

### text (default)
Use for conversational content, notes, and general information.
```python
episode_body="User said they prefer React over Vue"
```

### json
Use for structured data that should auto-extract entities.
```python
episode_body={
    "decision": {
        "type": "framework",
        "chosen": "Next.js",
        "alternatives": ["Gatsby", "Remix"],
        "reason": "Better SEO support"
    }
}
```

### message
Use for chat-style interactions with role indicators.
```python
episode_body="User: How do I deploy?\nAssistant: Use the deploy.sh script\nUser: Thanks!"
```

## Tips for Effective Usage

1. **Be Specific in Queries**: More specific queries return better results
2. **Use Entity Filters**: Filter by entity type for targeted searches
3. **Leverage JSON Format**: Structure complex information for better extraction
4. **Name Episodes Clearly**: Use descriptive names for easy retrieval
5. **Add Source Context**: Include source_description for traceability
6. **Batch Related Information**: Group related facts in single episodes
7. **Check Before Adding**: Always search to avoid duplicates
8. **Use UUIDs Sparingly**: Let system generate them unless specific need
9. **Handle Errors Gracefully**: Check response status and retry if needed
10. **Clean Up When Needed**: Use delete tools to remove outdated information

## Error Response Patterns

Most tools return responses in this format:
```python
# Success
{"message": "Operation successful", "data": {...}}

# Error  
{"error": "Error description", "details": {...}}
```

Always check for error responses and handle appropriately.