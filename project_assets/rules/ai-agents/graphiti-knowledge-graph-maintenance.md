# Graphiti Knowledge Graph Maintenance Guide for AI Agents

## Purpose

This guide helps AI agents maintain and evolve project-specific knowledge graph schemas. It provides step-by-step procedures for proposing and implementing schema changes.

## When to Use This Guide

Use this guide when you need to:
- Add new entity types to a project
- Define new relationships between entities
- Modify existing entity properties
- Update extraction rules for a project

## Schema Files Location

Project schemas are located at:
`project_assets/rules/ai-agents/examples/graphiti-[project-name]-schema.md`

## Decision Process for Schema Changes

### Step 1: Identify the Need

Before making any changes, determine if modification is truly needed:

```
Is the information I need to store covered by existing entities?
├─ YES → Use existing entities (no schema change needed)
└─ NO → Continue to Step 2

Can the information be represented as a relationship (fact)?
├─ YES → Check if relationship type exists
│   ├─ YES → Use existing relationship
│   └─ NO → Need to define new relationship type
└─ NO → Need new entity type
```

### Step 2: Verify Current Schema

Always check the current project schema before proposing changes:

```python
# Example verification process
1. Read current schema file
2. List all defined entities
3. List all defined relationships
4. Check if proposed addition already exists in different form
```

### Step 3: Design the Change

#### For New Entity Types

```markdown
## New Entity: [EntityName]

**Justification**: [Why this entity is needed, referencing user request or discovered need]

**Definition**:
- **Purpose**: [What this entity represents]
- **Key Properties**:
  - `property1` (type): [Description]
  - `property2` (type): [Description]
- **Relationships**: 
  - Can be [RELATIONSHIP] to [OtherEntity]
  - Can have [RELATIONSHIP] from [AnotherEntity]

**Extraction Rules**:
- Look for [specific patterns]
- Extract when [conditions]
- Handle [edge cases] by [approach]
```

#### For New Relationships

```markdown
## New Relationship: [RELATIONSHIP_NAME]

**Justification**: [Why this relationship is needed]

**Definition**:
- **Subject**: [EntityType] 
- **Predicate**: [RELATIONSHIP_NAME]
- **Object**: [EntityType]
- **Example**: (User: "John") --[PREFERS]--> (Framework: "React")

**Extraction Conditions**:
- Extract when [specific language patterns occur]
- Requires [what information must be present]
- Priority when [disambiguation rules]
```

### Step 4: Propose the Change

Create a schema update proposal following this template:

```markdown
# Schema Update Proposal: [Project Name]

## Summary
[Brief description of proposed changes]

## Detailed Changes

### 1. [First Change Type]
[Detailed specification using templates from Step 3]

### 2. [Second Change Type]
[Detailed specification]

## Impact Analysis
- **Backward Compatibility**: [Will existing data still work?]
- **Extraction Complexity**: [How difficult to implement?]
- **Value Addition**: [What new capabilities does this enable?]

## Implementation Notes
- [Any special considerations]
- [Dependencies on other schema elements]
```

### Step 5: Implement the Change

Once approved, update the schema file:

1. **Locate the appropriate section** in the schema file
2. **Add the new definition** following existing patterns
3. **Update the table of contents** if present
4. **Add examples** to illustrate usage
5. **Update version/date** if tracked

## Common Schema Evolution Scenarios

### Scenario 1: User Requests Tracking New Information

**Example**: "I need to track which team members worked on each feature"

**Process**:
1. Check if "TeamMember" and "Feature" entities exist
2. If not, define them
3. Define "WORKED_ON" relationship
4. Update extraction rules to identify team member mentions

### Scenario 2: Discovered Pattern Needs Formalization

**Example**: Noticing users frequently mention deployment environments

**Process**:
1. Define "Environment" entity
2. Add properties: name, type (dev/staging/prod), url
3. Define relationships to existing entities (Application, Configuration)
4. Create extraction rules for environment mentions

### Scenario 3: Existing Entity Needs Enhancement

**Example**: "Procedure" entity needs to track execution time

**Process**:
1. Verify "Procedure" entity definition
2. Add new property: "estimated_duration"
3. Update extraction rules to capture time mentions
4. Document backward compatibility (optional field)

## Validation Checklist

Before submitting a schema change proposal:

- [ ] **Uniqueness**: Verified entity/relationship doesn't already exist
- [ ] **Clarity**: Definitions are clear and unambiguous  
- [ ] **Completeness**: All properties and relationships are defined
- [ ] **Examples**: Concrete examples are provided
- [ ] **Extraction**: Clear rules for when to extract
- [ ] **Compatibility**: Existing data remains valid
- [ ] **Justification**: Clear link to user need or use case
- [ ] **Consistency**: Follows naming conventions of project

## Best Practices

### Naming Conventions

**Entities**:
- Use PascalCase: `UserPreference`, `SystemComponent`
- Be specific: `DatabaseTable` not just `Table`
- Avoid abbreviations

**Relationships**:
- Use UPPER_SNAKE_CASE: `DEPENDS_ON`, `REFERS_TO`
- Use active voice: `CREATES` not `CREATED_BY`
- Be directional: Subject performs action on Object

**Properties**:
- Use snake_case: `created_at`, `is_active`
- Be descriptive: `deployment_frequency` not `freq`

### Documentation Standards

Each schema element should include:
1. **Purpose**: One-sentence description
2. **Properties**: Type and description for each
3. **Examples**: At least one concrete example
4. **Extraction**: When and how to identify
5. **Relationships**: What it connects to

### Version Control Considerations

When updating schemas:
- Note the date of change
- Briefly describe what changed
- Consider impact on existing data
- Document migration needs if any

## Examples of Well-Defined Schema Elements

### Good Entity Definition

```markdown
**`DeploymentEvent`**: Represents a software deployment to an environment
- **Properties**:
  - `timestamp` (datetime): When deployment occurred
  - `version` (string): Version or commit hash deployed  
  - `status` (enum): success|failed|rollback
  - `duration` (integer): Deployment time in seconds
- **Relationships**:
  - DEPLOYED_TO → Environment
  - DEPLOYED_BY → TeamMember
  - DEPLOYS → Application
- **Extraction**: Look for "deployed", "released", "pushed to production"
```

### Good Relationship Definition

```markdown
**IMPLEMENTS**: Connects SystemComponent to Requirement
- **Example**: (AuthService) --[IMPLEMENTS]--> (UserLoginRequirement)
- **Extract when**: 
  - "X implements requirement Y"
  - "X satisfies requirement Y"
  - "Requirement Y is fulfilled by X"
- **Properties on edge**:
  - `completion_date` (optional)
  - `verification_status` (optional)
```

## Troubleshooting Schema Issues

**Problem**: Multiple entities could represent the same concept
**Solution**: Choose the most specific one, or merge similar entities

**Problem**: Unclear when to use entity vs relationship property
**Solution**: Entities = things that exist independently, Properties = attributes of one thing

**Problem**: Circular relationship definitions
**Solution**: Ensure relationships have clear direction and purpose

**Problem**: Extraction rules too broad/narrow
**Solution**: Start narrow, expand based on real examples

Remember: Schema evolution is iterative. Start simple, expand based on actual needs, and maintain clarity over complexity.