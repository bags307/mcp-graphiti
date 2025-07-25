# Graphiti Schema: [PROJECT_NAME] Project

This document defines the knowledge graph schema for the [PROJECT_NAME] project.

**Core Rules**: See `project_assets/rules/ai-agents/graphiti-mcp-core-rules.md` for general Graphiti usage
**Maintenance**: See `project_assets/rules/ai-agents/graphiti-knowledge-graph-maintenance.md` for updating this schema

## 1. Project Overview

**Purpose**: [Brief description of what this project's knowledge graph tracks]
**Domain**: [e.g., Software Development, Product Management, Customer Support]
**Key Concepts**: [List 3-5 main concepts this graph captures]

## 2. Defined Entities

### Core Entities

#### Entity: `ExampleEntity`
**Purpose**: [What this entity represents in one sentence]

**Properties**:
- `name` (string, required): [Description]
- `description` (string, optional): [Description]
- `status` (enum: active|inactive|pending): [Description]
- `created_date` (string, ISO date): [Description]

**Example Instance**:
```json
{
  "type": "ExampleEntity",
  "name": "Sample Instance",
  "description": "This is an example",
  "status": "active",
  "created_date": "2024-01-20"
}
```

**Extraction Rules**:
- Look for phrases like "[specific patterns]"
- Extract when user mentions "[keywords]"
- Required context: [what must be present]

#### Entity: `AnotherEntity`
**Purpose**: [What this entity represents]

**Properties**:
- `id` (string, required): Unique identifier
- `category` (string, required): Classification
- [Add more properties as needed]

**Example Instance**:
```json
{
  "type": "AnotherEntity",
  "id": "ANE-001",
  "category": "primary"
}
```

### Domain-Specific Entities

[Add entities specific to your project domain]

## 3. Defined Relationships (Facts)

### Relationship: `RELATES_TO`
**Pattern**: (ExampleEntity) --[RELATES_TO]--> (AnotherEntity)

**Properties on Edge**:
- `relationship_type` (string): Nature of relationship
- `strength` (enum: strong|moderate|weak): Connection strength

**Example Fact**:
```
(ExampleEntity: "Instance A") --[RELATES_TO {relationship_type: "depends", strength: "strong"}]--> (AnotherEntity: "Instance B")
```

**Extraction Conditions**:
- When user says "A depends on B"
- When "A requires B" is mentioned
- When "B is a prerequisite for A"

### Relationship: `OWNS`
**Pattern**: (Person) --[OWNS]--> (ExampleEntity)

**Properties on Edge**:
- `since` (string, ISO date): Ownership start date
- `role` (string): Type of ownership

**Example Fact**:
```
(Person: "John Doe") --[OWNS {since: "2024-01-01", role: "maintainer"}]--> (ExampleEntity: "Core Module")
```

[Add more relationships as needed]

## 4. Extraction Guidelines

### General Principles
1. **Explicit over Implicit**: Only extract what's clearly stated
2. **Consistency**: Use the same entity for the same concept
3. **Completeness**: Include all required properties
4. **Context**: Preserve important contextual information

### Entity-Specific Guidelines

**For ExampleEntity**:
- Always capture the status if mentioned
- Default to "active" status if not specified
- Use full names, not abbreviations

**For AnotherEntity**:
- Generate IDs in format "ANE-XXX" if not provided
- Categories must be from predefined list

### Relationship Guidelines

**For RELATES_TO**:
- Default strength to "moderate" if unclear
- Always specify relationship_type
- Bidirectional relationships need two facts

**For OWNS**:
- Current date for "since" if not specified
- "role" defaults to "owner" if not stated

## 5. Common Patterns

### Pattern: New Item Creation
When user says "Create a new [entity]" or "Add [entity]":
```json
{
  "episode_name": "Creating [Entity Name]",
  "entities": {
    "new_item": {
      "type": "ExampleEntity",
      "name": "[Provided Name]",
      "status": "pending",
      "created_date": "[Today's Date]"
    }
  }
}
```

### Pattern: Relationship Establishment
When user indicates connection between entities:
```json
{
  "episode_name": "Linking [Entity A] to [Entity B]",
  "entities": {
    "entity_a": {"type": "ExampleEntity", "name": "[A]"},
    "entity_b": {"type": "AnotherEntity", "id": "[B]"}
  },
  "relationships": [
    {
      "from": "entity_a",
      "to": "entity_b",
      "type": "RELATES_TO",
      "properties": {
        "relationship_type": "[specific type]",
        "strength": "[determined strength]"
      }
    }
  ]
}
```

## 6. Validation Rules

1. **Required Fields**: All entities must have required properties
2. **Enum Values**: Only use defined enum values
3. **Date Formats**: Use ISO format (YYYY-MM-DD)
4. **ID Formats**: Follow specified patterns
5. **Relationship Validity**: Both nodes must exist

## 7. Project-Specific Conventions

### Naming Conventions
- Entities: PascalCase (e.g., `ProjectTask`)
- Properties: snake_case (e.g., `due_date`)
- Relationships: UPPER_SNAKE_CASE (e.g., `ASSIGNED_TO`)

### Default Values
- Status fields: Default to lowest/initial state
- Dates: Use current date for creation timestamps
- Booleans: Default to false unless specified

### Edge Cases
- [Describe how to handle ambiguous situations]
- [Specify fallback behaviors]

## 8. Integration Notes

### With Other Systems
- [How this schema relates to external systems]
- [Data mapping considerations]

### With Other Projects
- [Shared entity types across projects]
- [Cross-project relationship rules]

## 9. Future Evolution

Potential additions being considered:
- [ ] Entity: `FutureEntity` - For tracking [purpose]
- [ ] Relationship: `FUTURE_RELATIONSHIP` - To connect [entities]
- [ ] Property: Add `priority` to ExampleEntity

## 10. Examples Repository

### Full Episode Examples

#### Example 1: Complete Entity Creation
```json
{
  "name": "Project Setup",
  "episode_body": {
    "project": {
      "type": "Project",
      "name": "API Redesign",
      "description": "Modernize REST API",
      "status": "active"
    },
    "team_members": [
      {"type": "Person", "name": "Alice"},
      {"type": "Person", "name": "Bob"}
    ],
    "relationships": [
      {"from": "Alice", "to": "project", "type": "WORKS_ON"},
      {"from": "Bob", "to": "project", "type": "WORKS_ON"}
    ]
  },
  "format": "json"
}
```

[Add more comprehensive examples]

---

**Note**: This schema is a living document. Update it as the project evolves and new patterns emerge. Always validate changes against existing data to ensure compatibility.