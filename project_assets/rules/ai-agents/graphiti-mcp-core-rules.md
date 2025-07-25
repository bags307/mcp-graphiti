# Graphiti MCP Tools Guide for AI Agents

## Quick Start for AI Agents

This guide helps AI agents effectively use Graphiti MCP server tools for entity extraction and knowledge graph management. Graphiti transforms conversations and data into a richly connected knowledge network.

### Essential MCP Tools

1. **mcp__graphiti__search_nodes** - Search for entities in the knowledge graph
2. **mcp__graphiti__search_facts** - Search for relationships between entities  
3. **mcp__graphiti__add_episode** - Add new information to the graph
4. **mcp__graphiti__get_episodes** - Retrieve recent episodes
5. **mcp__graphiti__delete_entity_edge** - Remove relationships
6. **mcp__graphiti__delete_episode** - Remove episodes

### Before Starting Any Task

Always search the knowledge graph first to understand existing context:

```python
# Search for relevant preferences
await mcp__graphiti__search_nodes(
    query="user preferences coding style",
    entity="Preference",
    max_nodes=10
)

# Search for established procedures
await mcp__graphiti__search_nodes(
    query="deployment process",
    entity="Procedure", 
    max_nodes=5
)

# Search for relationships
await mcp__graphiti__search_facts(
    query="component dependencies",
    max_facts=10
)
```

## Understanding Graphiti Rule Structure

There are three types of rules in the Graphiti ecosystem:

1. **Core Rules (this document)**: General guidelines for using Graphiti tools
2. **Project-Specific Schema**: Located at `project_assets/rules/ai-agents/examples/graphiti-[project-name]-schema.md`
3. **Schema Maintenance**: Located at `project_assets/rules/ai-agents/graphiti-knowledge-graph-maintenance.md`

**Important**: Project-specific rules always override general rules when there's a conflict.

## Entity Extraction Principles

### 1. Use Structured Extraction Patterns

Each entity definition follows this format:
- **AI Persona**: Role and expertise
- **Task Definition**: What to extract
- **Context**: Background information
- **Instructions**: Step-by-step extraction process
- **Output Format**: Expected structure

### 2. Maintain Entity Integrity

- Each entity must have a unique, non-overlapping purpose
- Avoid creating duplicate entities with similar meanings
- Ensure clear boundaries between entity types

### 3. Extract Only Explicit Information

```python
# GOOD: Extract what's clearly stated
await mcp__graphiti__add_episode(
    name="User Preference",
    episode_body="I prefer using TypeScript for all new projects",
    format="text"
)

# BAD: Making assumptions
# Don't assume user dislikes JavaScript just because they prefer TypeScript
```

### 4. Handle Ambiguity Properly

When information is unclear:
- Acknowledge the ambiguity in your extraction
- Don't fabricate missing details
- Use optional fields appropriately

## Working with Episodes

### Adding Text Episodes

```python
# Simple text episode
await mcp__graphiti__add_episode(
    name="Architecture Decision",
    episode_body="We decided to use microservices architecture for better scalability",
    format="text",
    source_description="team meeting notes"
)
```

### Adding Structured Data Episodes

```python
# JSON format for automatic entity extraction
episode_data = {
    "company": {
        "name": "TechCorp",
        "industry": "Software",
        "founded": 2020
    },
    "products": [
        {
            "name": "CloudSync",
            "category": "SaaS",
            "description": "Real-time data synchronization"
        }
    ]
}

await mcp__graphiti__add_episode(
    name="Company Profile",
    episode_body=episode_data,  # Pass dict directly
    format="json"
)
```

### Best Practices for Episodes

1. **Use descriptive names** that summarize the content
2. **Choose appropriate format**:
   - `text`: Plain conversational content
   - `json`: Structured data with clear entities
   - `message`: Chat-style interactions
3. **Add source_description** for context
4. **Keep episodes focused** on a single topic or event

## Agent Memory Management

### Search Before Action

```python
# Before implementing a feature, check for existing patterns
nodes = await mcp__graphiti__search_nodes(
    query="authentication implementation",
    max_nodes=10
)

# Check for related facts
facts = await mcp__graphiti__search_facts(
    query="authentication dependencies",
    max_facts=10
)
```

### Capture Information Immediately

When users express preferences, requirements, or decisions:

```python
# Capture preference immediately
await mcp__graphiti__add_episode(
    name="Code Style Preference",
    episode_body="User prefers 2-space indentation and trailing commas in JavaScript",
    format="text"
)

# For complex requirements, use structured format
requirement_data = {
    "requirement": {
        "name": "API Rate Limiting",
        "type": "non-functional",
        "description": "API must handle 1000 requests per minute",
        "priority": "high"
    }
}

await mcp__graphiti__add_episode(
    name="Performance Requirement",
    episode_body=requirement_data,
    format="json"
)
```

### Document Procedures Clearly

```python
procedure_data = {
    "procedure": {
        "name": "Database Migration Process",
        "steps": [
            "1. Backup current database",
            "2. Run migration scripts in staging",
            "3. Verify data integrity",
            "4. Apply to production during maintenance window"
        ],
        "prerequisites": ["Admin access", "Maintenance window scheduled"],
        "estimated_time": "2 hours"
    }
}

await mcp__graphiti__add_episode(
    name="Database Migration Procedure",
    episode_body=procedure_data,
    format="json"
)
```

## Advanced Search Techniques

### Hybrid Search Capabilities

Graphiti uses multiple search strategies:
- **Vector similarity**: Semantic meaning matching
- **Full-text search**: Exact keyword matching
- **Graph traversal**: Relationship-based discovery

### Effective Search Queries

```python
# Search with entity filtering
preferences = await mcp__graphiti__search_nodes(
    query="testing framework choices",
    entity="Preference",
    max_nodes=5
)

# Center search around a specific node
related_nodes = await mcp__graphiti__search_nodes(
    query="related components",
    center_node_uuid="uuid-of-main-component",
    max_nodes=10
)

# Search facts with context
dependencies = await mcp__graphiti__search_facts(
    query="module dependencies",
    center_node_uuid="uuid-of-module",
    max_facts=15
)
```

## Error Handling and Troubleshooting

### Common Issues and Solutions

1. **Episode not being processed**:
   - Check format parameter matches content type
   - Ensure episode_body is properly formatted
   - Verify server connection and permissions

2. **Search returning no results**:
   - Try broader search terms
   - Remove entity filter to search all types
   - Check if data exists with get_episodes

3. **Invalid JSON in episodes**:
   - Pass Python dict/list directly, not JSON string
   - Ensure all required fields are present
   - Validate structure before submission

### Debugging Tips

```python
# Check recent episodes to verify processing
recent = await mcp__graphiti__get_episodes(
    last_n=5
)

# Verify entity was created
nodes = await mcp__graphiti__search_nodes(
    query="exact entity name",
    max_nodes=1
)
```

## Best Practices Summary

1. **Always search before adding** to avoid duplicates
2. **Use structured data** (JSON format) for complex information
3. **Be specific** in entity and relationship definitions
4. **Document reasoning** in episode names and descriptions
5. **Maintain consistency** with established patterns
6. **Handle errors gracefully** with proper validation
7. **Keep episodes focused** and atomic
8. **Use appropriate search filters** for better results
9. **Track conversation context** across interactions
10. **Update knowledge incrementally** as new information emerges

## Parameter Guidelines

### add_episode Parameters
- **name**: Descriptive title (required)
- **episode_body**: Content as string or dict (required)
- **format**: "text", "json", or "message" (default: "text")
- **source_description**: Context about the source (optional)
- **group_id**: Usually omit - let system use defaults
- **uuid**: Usually omit - auto-generated

### search_nodes Parameters
- **query**: Search terms (required)
- **entity**: Filter by entity type like "Preference", "Procedure" (optional)
- **max_nodes**: Limit results, default 10 (optional)
- **center_node_uuid**: Search around specific node (optional)
- **group_ids**: Filter by groups (optional)

### search_facts Parameters
- **query**: Search terms (required)
- **max_facts**: Limit results, default 10 (optional)
- **center_node_uuid**: Search around specific node (optional)
- **group_ids**: Filter by groups (optional)

Remember: The knowledge graph is your persistent memory. Use it consistently to build a rich, interconnected understanding of the project and user preferences.