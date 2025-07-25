# Development Entity Relationships Schema

This document defines the relationships (edges/facts) between development entities in the Graphiti knowledge graph.

**IMPORTANT**: In Graphiti, relationships are NOT defined as separate entities. They are created dynamically within episodes using the "relationships" array. This document serves as a reference for the types of relationships that should be extracted.

## Overview

The development domain includes four core entities:
- **BugReport**: Tracks defects and issues
- **CodeChange**: Records modifications to the codebase
- **TechnicalDecision**: Documents architectural and technology choices
- **Preference**: Captures individual and team preferences

## Relationship Definitions

### 1. FIXES (CodeChange → BugReport)
**Pattern**: `(CodeChange) --[FIXES]--> (BugReport)`

**Description**: Indicates that a code change fixes a specific bug report.

**Properties on Edge**:
- `verification_status` (enum: pending|verified|failed): Whether the fix has been verified
- `fix_type` (enum: complete|partial|workaround): Nature of the fix
- `verified_by` (string, optional): Person who verified the fix
- `verified_date` (string, ISO date, optional): When fix was verified

**Example**:
```
(CodeChange: "Fix null pointer in auth") --[FIXES {verification_status: "verified", fix_type: "complete", verified_by: "QA-Alice"}]--> (BugReport: "Login crash on empty password")
```

**Extraction Conditions**:
- "This fixes bug #123"
- "Resolves issue with..."
- "Patch for the reported problem"
- Code change description mentions fixing specific bug

### 2. IMPLEMENTS (CodeChange → TechnicalDecision)
**Pattern**: `(CodeChange) --[IMPLEMENTS]--> (TechnicalDecision)`

**Description**: Shows that a code change implements a technical decision.

**Properties on Edge**:
- `implementation_phase` (enum: initial|ongoing|final): Stage of implementation
- `compliance_level` (enum: full|partial|adapted): How closely it follows the decision
- `notes` (string, optional): Implementation notes or deviations

**Example**:
```
(CodeChange: "Add Redis caching layer") --[IMPLEMENTS {implementation_phase: "initial", compliance_level: "full"}]--> (TechnicalDecision: "Use Redis for session management")
```

**Extraction Conditions**:
- "Implementing the decision to..."
- "As per our architecture decision..."
- "Following the technical direction..."

### 3. REPORTED_BY (BugReport → Person)
**Pattern**: `(BugReport) --[REPORTED_BY]--> (Person)`

**Description**: Links a bug report to the person who reported it.

**Properties on Edge**:
- `report_method` (enum: direct|automated|monitoring): How it was reported
- `initial_severity` (string, optional): Reporter's assessment of severity

**Example**:
```
(BugReport: "Memory leak in data processor") --[REPORTED_BY {report_method: "monitoring", initial_severity: "critical"}]--> (Person: "DevOps-Bob")
```

**Extraction Conditions**:
- Already captured in BugReport.reporter field
- Automatically created when BugReport entity is extracted

### 4. DECIDED_BY (TechnicalDecision → Person)
**Pattern**: `(TechnicalDecision) --[DECIDED_BY]--> (Person)`

**Description**: Links technical decisions to decision makers.

**Properties on Edge**:
- `role_in_decision` (enum: primary|contributor|approver): Their role
- `expertise_area` (string, optional): What expertise they brought

**Example**:
```
(TechnicalDecision: "Microservices architecture") --[DECIDED_BY {role_in_decision: "primary", expertise_area: "distributed systems"}]--> (Person: "Architect-Carol")
```

**Extraction Conditions**:
- From TechnicalDecision.decision_maker list
- "Carol made the call to..."
- "The architecture team decided..."

### 5. BLOCKS (BugReport → Feature/BugReport/CodeChange)
**Pattern**: `(BugReport) --[BLOCKS]--> (Feature|BugReport|CodeChange)`

**Description**: Indicates that a bug blocks other work.

**Properties on Edge**:
- `blocking_severity` (enum: complete|partial|intermittent): How much it blocks
- `workaround_available` (boolean): Whether there's a workaround
- `estimated_impact` (string, optional): Impact description

**Example**:
```
(BugReport: "Database connection pool exhaustion") --[BLOCKS {blocking_severity: "complete", workaround_available: false}]--> (Feature: "User Analytics Dashboard")
```

**Extraction Conditions**:
- "This bug is blocking..."
- "Can't proceed until this is fixed"
- "Dependent on resolution of..."

### 6. CAUSES (CodeChange → BugReport)
**Pattern**: `(CodeChange) --[CAUSES]--> (BugReport)`

**Description**: Indicates that a code change introduced a bug (regression).

**Properties on Edge**:
- `regression_type` (enum: functional|performance|security): Type of regression
- `detected_after` (string, duration): How long after the change
- `root_cause` (string, optional): Brief description of cause

**Example**:
```
(CodeChange: "Optimize query performance") --[CAUSES {regression_type: "functional", detected_after: "2 days"}]--> (BugReport: "Missing results in search")
```

**Extraction Conditions**:
- "This change introduced..."
- "Regression caused by..."
- "Bug appeared after deploying..."

### 7. PREFERS (Person → Preference)
**Pattern**: `(Person) --[PREFERS]--> (Preference)`

**Description**: Links people to their preferences.

**Properties on Edge**:
- `context` (string, optional): When this preference applies
- `since` (string, ISO date, optional): When preference was established

**Example**:
```
(Person: "Frontend-Alice") --[PREFERS {context: "code reviews", since: "2024-01-15"}]--> (Preference: "Detailed inline comments")
```

**Extraction Conditions**:
- From Preference.person field
- "Alice prefers..."
- "Team lead likes to..."

### 8. CONFLICTS_WITH (Preference → Preference)
**Pattern**: `(Preference) --[CONFLICTS_WITH]--> (Preference)`

**Description**: Indicates when preferences are incompatible.

**Properties on Edge**:
- `conflict_type` (enum: direct|partial|situational): Nature of conflict
- `resolution_strategy` (string, optional): How to handle the conflict

**Example**:
```
(Preference: "Tabs for indentation") --[CONFLICTS_WITH {conflict_type: "direct", resolution_strategy: "follow project convention"}]--> (Preference: "Spaces for indentation")
```

**Extraction Conditions**:
- "This conflicts with..."
- "Incompatible with the preference for..."
- When opposite preferences are stated

### 9. SUPERSEDES (TechnicalDecision → TechnicalDecision)
**Pattern**: `(TechnicalDecision) --[SUPERSEDES]--> (TechnicalDecision)`

**Description**: When one decision replaces another.

**Properties on Edge**:
- `reason` (string): Why the change was made
- `migration_required` (boolean): Whether migration is needed
- `superseded_date` (string, ISO date): When superseded

**Example**:
```
(TechnicalDecision: "GraphQL API") --[SUPERSEDES {reason: "better performance", migration_required: true}]--> (TechnicalDecision: "REST API")
```

**Extraction Conditions**:
- "This replaces our previous decision..."
- "Moving away from X to Y"
- "Deprecating the old approach"

### 10. DEPENDS_ON (CodeChange → CodeChange)
**Pattern**: `(CodeChange) --[DEPENDS_ON]--> (CodeChange)`

**Description**: When one change requires another to be applied first.

**Properties on Edge**:
- `dependency_type` (enum: build|runtime|logical): Type of dependency
- `strict` (boolean): Whether order is strictly required

**Example**:
```
(CodeChange: "Add user preferences API") --[DEPENDS_ON {dependency_type: "logical", strict: true}]--> (CodeChange: "Create preferences table")
```

**Extraction Conditions**:
- "This requires the previous change..."
- "Must be applied after..."
- "Depends on PR #123"

### 11. RELATED_TO (Any → Any)
**Pattern**: `(Any Entity) --[RELATED_TO]--> (Any Entity)`

**Description**: Generic relationship for loosely connected entities.

**Properties on Edge**:
- `relationship_type` (string): Nature of the relationship
- `strength` (enum: strong|moderate|weak): Connection strength

**Example**:
```
(BugReport: "Performance degradation") --[RELATED_TO {relationship_type: "similar_symptoms", strength: "moderate"}]--> (BugReport: "High CPU usage")
```

**Extraction Conditions**:
- "This is related to..."
- "See also..."
- "Similar to..."

## Usage Guidelines

### How Relationships Work in Graphiti

Relationships are created as part of episodes, not as standalone entities. When adding an episode:

1. Define all entities involved in the "episode_body"
2. Add a "relationships" array with connections between those entities
3. Each relationship includes: from (entity key), to (entity key), type, and optional properties

### Creating Relationships

When extracting episodes, relationships should be created based on explicit mentions or clear implications in the text:

```json
{
  "name": "Bug Fix Implementation",
  "episode_body": {
    "change": {
      "type": "CodeChange",
      "author": "Backend-Bob",
      "summary": "Fix memory leak in data processor",
      "change_type": "fix",
      "files_changed": ["src/processor/data_handler.py"],
      "description": "Properly dispose of temporary objects after processing"
    },
    "bug": {
      "type": "BugReport", 
      "title": "Memory leak in data processor",
      "reporter": "DevOps-Carol",
      "status": "resolved"
    },
    "relationships": [
      {
        "from": "change",
        "to": "bug",
        "type": "FIXES",
        "properties": {
          "verification_status": "verified",
          "fix_type": "complete",
          "verified_by": "QA-Alice"
        }
      }
    ]
  },
  "format": "json"
}
```

### Relationship Integrity Rules

1. **Both entities must exist**: Never create relationships to non-existent entities
2. **Direction matters**: Follow the defined pattern direction
3. **Required properties**: Always include required edge properties
4. **Avoid duplicates**: Don't create the same relationship twice
5. **Maintain consistency**: Use consistent property values

### Automatic Relationship Creation

Some relationships should be automatically created when entities are extracted:
- `REPORTED_BY`: When BugReport has a reporter
- `DECIDED_BY`: When TechnicalDecision has decision_makers
- `PREFERS`: When Preference has a person

### Querying Relationships

To find related entities:
```python
# Find all bugs fixed by a code change
await mcp__graphiti__search_facts(
    query="fixes relationship code change",
    max_facts=10
)

# Find dependencies between changes
await mcp__graphiti__search_facts(
    query="depends on code changes",
    max_facts=20
)
```

## Relationship Evolution

As the system evolves, new relationships may be needed:
- Consider adding relationships for test coverage
- May need relationships to external systems
- Could add temporal relationships (PRECEDED_BY, FOLLOWED_BY)

Remember: Relationships are as important as entities in creating a useful knowledge graph!

## Integration with Entity Extraction

Each entity's docstring now includes:
1. **Common Relationships** section showing typical relationships
2. **Full Episode Example** demonstrating how to create entities WITH relationships
3. Specific relationship properties and patterns

Always refer to the entity docstrings for the most up-to-date relationship examples.