# Graphiti Troubleshooting Guide

## Common Issues and Solutions

### Issue: Episode Not Being Processed

**Symptoms**:
- Episode added but no entities extracted
- No error returned but data not in graph
- Search doesn't find expected results

**Diagnostic Steps**:
```python
# 1. Verify episode was created
recent = await mcp__graphiti__get_episodes(last_n=5)
# Check if your episode appears

# 2. Check episode format
# Look for format mismatch - did you use "json" with text content?

# 3. Verify entity extraction worked
# Search for entities that should have been created
nodes = await mcp__graphiti__search_nodes(
    query="expected entity name",
    max_nodes=5
)
```

**Common Causes & Solutions**:

1. **Wrong format parameter**
```python
# BAD: JSON string with text format
await mcp__graphiti__add_episode(
    name="Test",
    episode_body='{"key": "value"}',  # String, not dict!
    format="text"  # Wrong format
)

# GOOD: Dict with json format
await mcp__graphiti__add_episode(
    name="Test",
    episode_body={"key": "value"},  # Dict, not string!
    format="json"
)
```

2. **Entity not in schema**
- Check if entity type is defined in project schema
- May need to add entity definition first

3. **Malformed JSON structure**
```python
# BAD: Deeply nested, unclear structure
{"data": {"wrapper": {"actual": {"entity": "value"}}}}

# GOOD: Clear entity structure
{"entity_type": {"name": "value", "property": "data"}}
```

### Issue: Search Returns No Results

**Symptoms**:
- Search returns empty results when data should exist
- Known entities not found
- Facts/relationships missing

**Diagnostic Steps**:
```python
# 1. Try broader search
results = await mcp__graphiti__search_nodes(
    query="partial name",  # Not too specific
    max_nodes=20
)

# 2. Remove filters
results = await mcp__graphiti__search_nodes(
    query="search term"
    # No entity filter, no group filter
)

# 3. Check recent episodes
episodes = await mcp__graphiti__get_episodes(last_n=10)
# Verify data was actually added
```

**Common Causes & Solutions**:

1. **Too specific query**
```python
# BAD: Very specific query
await mcp__graphiti__search_nodes(
    query="UserAuthenticationServiceHandlerModule"
)

# GOOD: Broader terms
await mcp__graphiti__search_nodes(
    query="authentication service"
)
```

2. **Wrong entity filter**
```python
# BAD: Wrong entity type
await mcp__graphiti__search_nodes(
    query="login process",
    entity="Preference"  # Should be Procedure
)

# GOOD: Correct entity type
await mcp__graphiti__search_nodes(
    query="login process",
    entity="Procedure"
)
```

3. **Group ID mismatch**
- Check if using correct group_id
- Try without group filter first

### Issue: Duplicate Entities Created

**Symptoms**:
- Multiple entities with same/similar names
- Relationships split across duplicates
- Confusion about which entity to use

**Prevention**:
```python
# Always search before adding
async def add_entity_safely(name, data):
    # Search for exact match
    existing = await mcp__graphiti__search_nodes(
        query=f'"{name}"',  # Exact match with quotes
        max_nodes=1
    )
    
    if existing["nodes"]:
        print(f"Entity exists: {existing['nodes'][0]['uuid']}")
        return existing["nodes"][0]
    else:
        # Safe to create
        result = await mcp__graphiti__add_episode(
            name=f"Creating {name}",
            episode_body=data,
            format="json"
        )
        return result
```

**Cleanup**:
```python
# Find duplicates
all_entities = await mcp__graphiti__search_nodes(
    query="duplicate name",
    max_nodes=50
)

# Identify which to keep (usually oldest or most connected)
# Delete duplicates
for dup in duplicates:
    await mcp__graphiti__delete_entity_edge(uuid=dup["uuid"])
```

### Issue: JSON Parsing Errors

**Symptoms**:
- "Invalid JSON" errors
- "Expected dict, got str" errors
- Silent failures with JSON format

**Common Mistakes**:

1. **Passing JSON string instead of dict**
```python
# BAD
episode_body = '{"name": "value"}'  # String
format = "json"

# GOOD
episode_body = {"name": "value"}  # Dict
format = "json"
```

2. **Invalid JSON structure**
```python
# BAD: Python-specific syntax
episode_body = {
    'name': 'value',
    'items': set([1, 2, 3]),  # Sets not JSON-serializable
    'date': datetime.now()    # Datetime objects not serializable
}

# GOOD: JSON-compatible types
episode_body = {
    'name': 'value',
    'items': [1, 2, 3],      # List instead of set
    'date': '2024-01-20'     # String date
}
```

### Issue: Relationship Extraction Failed

**Symptoms**:
- Entities created but no relationships
- Facts search returns empty
- Graph appears disconnected

**Diagnostic Approach**:
```python
# 1. Verify entities exist
entity1 = await mcp__graphiti__search_nodes(query="Entity One")
entity2 = await mcp__graphiti__search_nodes(query="Entity Two")

# 2. Search for facts between them
if entity1["nodes"] and entity2["nodes"]:
    facts = await mcp__graphiti__search_facts(
        query="",
        center_node_uuid=entity1["nodes"][0]["uuid"]
    )
```

**Better Relationship Definition**:
```python
# Explicit relationship structure
await mcp__graphiti__add_episode(
    name="Component Dependencies",
    episode_body={
        "entities": {
            "auth": {"type": "service", "name": "Auth Service"},
            "db": {"type": "database", "name": "User DB"}
        },
        "relationships": [
            {
                "from": "auth",
                "to": "db",
                "type": "DEPENDS_ON",
                "reason": "Needs user data"
            }
        ]
    },
    format="json"
)
```

### Issue: Performance Problems

**Symptoms**:
- Slow search responses
- Timeouts on large queries
- Memory issues with big datasets

**Solutions**:

1. **Limit search scope**
```python
# Use specific filters
results = await mcp__graphiti__search_nodes(
    query="specific term",
    entity="SpecificType",
    max_nodes=10  # Reasonable limit
)
```

2. **Batch large operations**
```python
# Break large datasets into chunks
for chunk in chunks(large_data, size=50):
    await mcp__graphiti__add_episode(
        name=f"Batch {i}",
        episode_body=chunk,
        format="json"
    )
    # Small delay between batches
    await asyncio.sleep(0.5)
```

3. **Use targeted searches**
```python
# Search around known entities
facts = await mcp__graphiti__search_facts(
    query="specific relationship",
    center_node_uuid=known_uuid,
    max_facts=10
)
```

### Issue: Authentication/Connection Errors

**Symptoms**:
- "Connection refused" errors
- "Unauthorized" responses
- Intermittent connection issues

**Checks**:
1. Verify MCP server is running
2. Check correct port (8000 for root, 8001+ for projects)
3. Confirm authentication if required
4. Check network connectivity

### Issue: Schema Validation Errors

**Symptoms**:
- "Entity type not recognized"
- "Invalid property for entity"
- Schema mismatch errors

**Solution Process**:
1. Check project schema file
2. Verify entity definition matches schema
3. Update schema if needed (see maintenance guide)
4. Ensure using correct project context

## Error Message Reference

### "Episode X queued for processing"
- **Meaning**: Episode successfully submitted
- **Action**: Wait briefly, then search for extracted entities

### "Entity type 'X' not found in schema"
- **Meaning**: Trying to filter by undefined entity type
- **Action**: Check schema or remove entity filter

### "No nodes found matching query"
- **Meaning**: Search returned empty (not an error)
- **Action**: Broaden search terms or check if data exists

### "Invalid JSON format"
- **Meaning**: episode_body doesn't match format="json"
- **Action**: Pass dict/list, not string, for JSON format

### "Rate limit exceeded"
- **Meaning**: Too many requests too quickly
- **Action**: Add delays between operations

## Prevention Best Practices

1. **Always Validate Before Adding**
```python
def validate_episode_data(data, format_type):
    if format_type == "json":
        assert isinstance(data, (dict, list)), "JSON format requires dict or list"
    elif format_type == "text":
        assert isinstance(data, str), "Text format requires string"
    return True
```

2. **Use Consistent Naming**
```python
# Establish naming conventions
ENTITY_NAME_PATTERN = "PascalCase"
RELATIONSHIP_PATTERN = "UPPER_SNAKE_CASE"
PROPERTY_PATTERN = "snake_case"
```

3. **Implement Retry Logic**
```python
async def robust_add_episode(name, body, format="text", retries=3):
    for attempt in range(retries):
        try:
            return await mcp__graphiti__add_episode(
                name=name,
                episode_body=body,
                format=format
            )
        except Exception as e:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```

4. **Log Operations**
```python
# Keep track of operations for debugging
operations_log = []

def log_operation(op_type, params, result):
    operations_log.append({
        "timestamp": datetime.now(),
        "operation": op_type,
        "parameters": params,
        "result": result
    })
```

## When All Else Fails

1. **Check the basics**:
   - Is the MCP server running?
   - Are you connected to the right server/port?
   - Is the data in the expected format?

2. **Simplify the problem**:
   - Try a minimal example
   - Remove all optional parameters
   - Test with known-good data

3. **Inspect the data flow**:
   - Add episode with unique marker
   - Search for that exact marker
   - Trace where it appears (or doesn't)

4. **Review logs**:
   - Check server logs for errors
   - Look for processing exceptions
   - Verify data transformations

Remember: Most issues stem from format mismatches, incorrect entity types, or overly specific searches. Start simple and build complexity gradually.