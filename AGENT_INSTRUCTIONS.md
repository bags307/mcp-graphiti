# AI Agent Instructions for Graphiti MCP Server

## Overview

You are working with a Graphiti MCP (Model Context Protocol) Server that provides knowledge graph capabilities. This system extracts entities and relationships from text, storing them in Neo4j for persistent memory and intelligent retrieval.

## Essential Reading

Before working with this codebase, familiarize yourself with these documents in order:

1. **Quick Start**: `project_assets/rules/ai-agents/graphiti-quick-reference.md`
   - MCP tool reference with examples
   - Common parameters and patterns
   - Quick lookup for all available tools

2. **Core Guidelines**: `project_assets/rules/ai-agents/graphiti-mcp-core-rules.md`
   - Comprehensive usage guide
   - Entity extraction principles
   - Memory management best practices

3. **Common Patterns**: `project_assets/rules/ai-agents/graphiti-common-patterns.md`
   - Proven extraction patterns
   - Search strategies
   - Data organization examples

4. **Troubleshooting**: `project_assets/rules/ai-agents/graphiti-troubleshooting.md`
   - Common issues and solutions
   - Error message reference
   - Debugging approaches

5. **Schema Maintenance**: `project_assets/rules/ai-agents/graphiti-knowledge-graph-maintenance.md`
   - How to propose schema changes
   - Evolution procedures
   - Validation checklists

## Key Principles

### 1. Always Search First
Before adding any information, search the knowledge graph to avoid duplicates and understand context:

```python
# Check for existing preferences
existing = await mcp__graphiti__search_nodes(
    query="relevant terms",
    entity="Preference"
)

# Check for procedures
procedures = await mcp__graphiti__search_nodes(
    query="process name",
    entity="Procedure"
)
```

### 2. Capture Information Immediately
When users express preferences, make decisions, or share important information, store it right away:

```python
await mcp__graphiti__add_episode(
    name="User Preference: Code Style",
    episode_body="User prefers 4-space indentation for Python",
    format="text"
)
```

### 3. Use Structured Data
For complex information, use JSON format to enable automatic entity extraction:

```python
await mcp__graphiti__add_episode(
    name="Project Configuration",
    episode_body={
        "project": {"name": "API v2", "status": "active"},
        "team": ["Alice", "Bob"],
        "deadline": "2024-Q2"
    },
    format="json"
)
```

### 4. Think in Graphs
Model information as nodes (entities) and edges (relationships):
- Entities: Things that exist independently (Person, Project, Component)
- Relationships: Connections between entities (OWNS, DEPENDS_ON, IMPLEMENTS)

## Project-Specific Schemas

Each project may have its own schema defining unique entities and relationships. Always check for a project-specific schema at:
`project_assets/rules/ai-agents/examples/graphiti-[project-name]-schema.md`

If working on a specific project, the project schema overrides general guidelines.

## Common MCP Tools

### Essential Tools You'll Use Most

1. **Search for Context**
   ```python
   nodes = await mcp__graphiti__search_nodes(query="search terms")
   facts = await mcp__graphiti__search_facts(query="relationships")
   ```

2. **Add Information**
   ```python
   await mcp__graphiti__add_episode(name="Title", episode_body=content, format="text|json")
   ```

3. **Review Recent Activity**
   ```python
   episodes = await mcp__graphiti__get_episodes(last_n=10)
   ```

## Best Practices

1. **Be Specific**: Use clear, descriptive names for episodes and entities
2. **Preserve Context**: Include relevant metadata and relationships
3. **Stay Consistent**: Follow established patterns in the codebase
4. **Document Decisions**: Record technical decisions and rationale
5. **Update Incrementally**: Build knowledge progressively
6. **Validate Before Adding**: Always check if information already exists
7. **Handle Errors Gracefully**: Implement retry logic and validation

## Working with the Codebase

### Key Files and Directories

- `graphiti_mcp_server.py`: Main MCP server implementation
- `entities/`: Entity definitions organized by category
- `project_assets/rules/`: Documentation and guidelines
- `.env`: Configuration (Neo4j credentials, API keys)
- `docker-compose.yml`: Service definitions

### Development Workflow

1. **Start Services**: `graphiti up -d`
2. **Check Status**: Verify services at http://localhost:8000/graphiti/status
3. **View Neo4j**: Browse graph at http://localhost:7474
4. **Reload Services**: `graphiti reload <container>` after changes

### Entity Definition Pattern

Entities follow a structured format with AI persona, task, context, and instructions:

```python
class MyEntity(BaseModel):
    """
    AI Persona: Expert at identifying X
    Task: Extract information about Y
    Context: Used for Z purposes
    Instructions: 
    1. Look for patterns...
    2. Extract when...
    """
    name: str = Field(description="Entity name")
    property: str = Field(description="Property description")
```

## Important Reminders

1. **OpenRouter Support**: The server supports OpenRouter with special Cerebras handling that injects "JSON" into prompts for structured output
2. **Security**: Never use weak passwords in production (NEO4J_PASSWORD)
3. **Graph Clearing**: The clear_graph tool requires explicit confirmation and destroys ALL data
4. **Project Isolation**: Each project has its own group_id for data separation

## Getting Help

- **Documentation**: Start with the quick reference guide
- **Patterns**: Check common patterns for proven solutions  
- **Troubleshooting**: Consult the troubleshooting guide for issues
- **Schema Changes**: Follow the maintenance guide for evolution

Remember: The knowledge graph is your persistent memory. Use it consistently to build rich, interconnected understanding across sessions.