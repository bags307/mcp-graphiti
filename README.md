# Graphiti MCP Server

Fork of the [getzep/graphiti](https://github.com/getzep/graphiti) example with a focus on developer experience and multi‑project support. Graphiti extracts entities and relationships from text and stores them in Neo4j. This repo adds a CLI that spins up a root server plus project‑specific MCP servers in Docker so several knowledge graphs share the same database.

## Quick Start

1. **Install and clone**
   ```bash
   pipx install 'git+https://github.com/rawr-ai/mcp-graphiti.git'
   git clone https://github.com/rawr-ai/mcp-graphiti.git
   cd mcp-graphiti
   cp .env.example .env  # fill in Neo4j credentials and your OpenAI key
   ```
2. **Launch services**
   ```bash
   graphiti compose   # generates docker-compose.yml and updates .cursor/mcp.json
   graphiti up -d
   ```
   The root server runs on port **8000**; project containers start at **8001**.
3. **Create a project**
   ```bash
   cd /path/to/my-kg
   graphiti init my-kg        # writes ai/graph/mcp-config.yaml
   # add entity definitions under ai/graph/entities/
   ```
   Rerun `graphiti compose && graphiti up -d` from anywhere to start its container.

Once running you can:
- Check `http://localhost:8000/graphiti/status`.
- Connect MCP‑compatible tools to `http://localhost:800{N}/sse`.
- Browse Neo4j at `http://localhost:7474` using the credentials in `.env`.

### Security note
If `NEO4J_PASSWORD` remains `password` the server refuses to start unless `GRAPHITI_ENV=dev`. Always use a strong password in production.

## Why this fork?
The upstream repository assumes one server per compose file. Here a single compose file manages many project servers that share Neo4j. Each service gets its own `group_id`, entities and model so projects stay isolated while running on the same database.

### Highlights
- **Project isolation** – different extraction rules or models never collide.
- **Editor auto‑discovery** – ports are written to `.cursor/mcp.json`.
- **Crash containment** – a bad prompt only restarts its container.
- **Hot reload** – tweak a project's config and run `graphiti reload <container>`.
- **OpenRouter support** – Advanced provider routing with special Cerebras compatibility.

Leave `mcp-projects.yaml` empty if you only need the root server.

## OpenRouter Configuration
The server supports OpenRouter as an LLM provider with advanced routing capabilities:

```bash
# Basic setup
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_API_KEY=sk-or-your-openrouter-key
export MODEL_NAME=meta-llama/llama-4-maverick

# Provider routing (e.g., use Cerebras exclusively)
export OPENROUTER_PROVIDER=cerebras
export OPENROUTER_ALLOW_FALLBACKS=false
```

The implementation includes special handling for Cerebras which requires "JSON" in prompts when using structured output.

## Making Your Project AI-Memory Enabled

This section shows exactly what to add to your project so Claude (or any AI agent) can use the Graphiti memory graph throughout every conversation.

### Step 1: Add Graphiti Instructions to Your Project

Create a `CLAUDE.md` file in your project root with these MANDATORY instructions:

```markdown
# CLAUDE.md - Graphiti Memory Instructions

## CRITICAL: Memory Graph Usage

You have access to a Graphiti memory graph for this project. You MUST use it constantly throughout our conversation.

### BEFORE EVERY TASK - MANDATORY SEARCHES

Before answering ANY question or taking ANY action, you MUST:

1. Search for relevant context:
```python
# Always search nodes first
nodes = await mcp__graphiti__search_nodes(
    query="[relevant keywords from the user's question]",
    max_nodes=10
)

# Then search for relationships
facts = await mcp__graphiti__search_facts(
    query="[relevant relationship keywords]",
    max_facts=10
)

# If asking about preferences/procedures
preferences = await mcp__graphiti__search_nodes(
    query="[topic] preference style convention [person_name if known]",
    entity="Preference",
    max_nodes=5
)

# Search for specific person's preferences
alice_prefs = await mcp__graphiti__search_nodes(
    query="Alice preference",
    entity="Preference",
    max_nodes=10
)
```

2. If no relevant information found, search broader terms
3. Use the retrieved context to inform your response

### DURING EVERY CONVERSATION - CAPTURE EVERYTHING

You MUST create episodes for:

1. **User Preferences** (immediately when expressed):
```python
# When someone expresses a preference
await mcp__graphiti__add_episode(
    name="Preference: [topic] - [person_name]",
    episode_body={
        "preference": {
            "person": "[name or identifier of who expressed this]",
            "topic": "[what the preference is about]",
            "preference": "[the specific preference]",
            "context": "[when/where this applies]",
            "strength": "[strong|moderate|slight]"
        }
    },
    format="json"
)

# Example: "I prefer tabs over spaces" from Alice
await mcp__graphiti__add_episode(
    name="Preference: Code Formatting - Alice",
    episode_body={
        "preference": {
            "person": "Alice",
            "topic": "code_formatting",
            "preference": "tabs over spaces",
            "context": "Python and JavaScript files",
            "strength": "strong"
        }
    },
    format="json"
)
```

2. **Technical Decisions** (as soon as made):
```python
# When any choice is made
await mcp__graphiti__add_episode(
    name="Decision: [what was decided]",
    episode_body={
        "decision": {
            "type": "[architecture/tool/approach]",
            "chosen": "[what was chosen]",
            "alternatives": ["option1", "option2"],
            "reason": "[why this choice]",
            "context": "[relevant details]"
        }
    },
    format="json"
)
```

3. **Problems and Solutions** (when encountered):
```python
# When debugging or solving issues
await mcp__graphiti__add_episode(
    name="Issue: [problem summary]",
    episode_body={
        "problem": "[what went wrong]",
        "cause": "[root cause]",
        "solution": "[how it was fixed]",
        "prevention": "[how to avoid in future]"
    },
    format="json"
)
```

4. **Code Patterns** (when established):
```python
# When creating reusable patterns
await mcp__graphiti__add_episode(
    name="Pattern: [pattern name]",
    episode_body={
        "pattern": {
            "name": "[descriptive name]",
            "purpose": "[what it solves]",
            "implementation": "[how to implement]",
            "files": ["file1.py", "file2.py"]
        }
    },
    format="json"
)
```

5. **Project Information** (any project details):
```python
# Project goals, requirements, constraints
await mcp__graphiti__add_episode(
    name="Project: [aspect]",
    episode_body={
        "aspect": "[goals/requirements/constraints]",
        "details": "[specific information]"
    },
    format="json"
)
```

### MANDATORY BEHAVIOR PATTERNS

1. **Start of EVERY conversation**:
   - Search for project context
   - Search for user preferences
   - Search for recent work
   - Load established procedures

2. **Before suggesting ANYTHING**:
   - Search if there's an established preference
   - Search if there's a defined procedure
   - Search for similar past decisions

3. **After completing ANY task**:
   - Create episode documenting what was done
   - Create episode for any decisions made
   - Create episode for any patterns discovered

4. **When user corrects you**:
   - Immediately create preference episode
   - Search for related preferences to update mental model

### YOUR MEMORY RESPONSIBILITIES

- You are building a persistent memory across all conversations
- Every piece of information might be crucial later
- Always err on the side of capturing too much rather than too little
- The knowledge graph IS your long-term memory - use it constantly
- **CRITICAL**: Always identify WHO said something, made a decision, or has a preference
  - Use names when known (Alice, Bob, TeamLead)
  - Use roles when names unknown (frontend-dev, product-owner)
  - Never use generic "user" - be specific about identity

## Project-Specific Memory Schema

[Your project-specific entities and relationships go here - see Step 2]
```

### Step 2: Define Your Project's Memory Schema

Add this section to your `CLAUDE.md` to define project-specific entities:

```markdown
## Project-Specific Entities

This project tracks the following custom entities:

### Entity: Component
Represents a software component in our architecture.

Extract when: User mentions services, modules, libraries, or system parts
```python
{
    "type": "Component",
    "name": "AuthService",
    "component_type": "service",
    "description": "Handles user authentication",
    "dependencies": ["Database", "CacheService"],
    "owner": "backend-team"
}
```

### Entity: Feature
Represents a product feature or user story.

Extract when: User discusses features, requirements, or user stories
```python
{
    "type": "Feature", 
    "name": "User Login",
    "status": "in_progress",
    "priority": "high",
    "assigned_to": "Alice",
    "related_components": ["AuthService", "UserAPI"]
}
```

### Entity: Configuration
Represents system configuration or settings.

Extract when: User mentions config, settings, environment variables
```python
{
    "type": "Configuration",
    "name": "DatabaseConfig",
    "environment": "production",
    "settings": {
        "host": "db.example.com",
        "pool_size": 20
    }
}
```

### Relationships to Track

1. **DEPENDS_ON**: (Component) --[DEPENDS_ON]--> (Component)
   - Extract when: "X needs Y", "X requires Y", "X uses Y"

2. **IMPLEMENTS**: (Component) --[IMPLEMENTS]--> (Feature)
   - Extract when: "X implements Y", "Y is handled by X"

3. **CONFIGURES**: (Configuration) --[CONFIGURES]--> (Component)
   - Extract when: Settings or config is associated with a component

### Schema Evolution

When you identify information that doesn't fit existing entities:
1. Propose new entity type in an episode
2. Document the structure and extraction rules
3. Start using it immediately
```

### Step 3: Create Project Entity Definitions

Create `ai/graph/entities/project_entities.py` in your project:

```python
"""
Project-specific entities for the knowledge graph.
Copy this file to your project at: ai/graph/entities/project_entities.py
"""

from pydantic import BaseModel, Field
from typing import List, Optional

class Component(BaseModel):
    """
    Software component in the system architecture.
    
    Extract when user mentions:
    - Services, microservices
    - Modules, packages
    - Libraries, frameworks
    - Databases, caches
    - Any architectural component
    """
    name: str = Field(description="Component name")
    component_type: str = Field(description="Type: service|library|database|cache|module")
    description: str = Field(description="What this component does")
    dependencies: List[str] = Field(description="Other components this depends on")
    owner: Optional[str] = Field(description="Team or person responsible")
    
class Feature(BaseModel):
    """
    Product feature or user story.
    
    Extract when user mentions:
    - Features, functionality
    - User stories, requirements
    - Capabilities, use cases
    """
    name: str = Field(description="Feature name")
    status: str = Field(description="Status: planned|in_progress|completed|blocked")
    priority: str = Field(description="Priority: critical|high|medium|low")
    description: str = Field(description="What this feature does")
    assigned_to: Optional[str] = Field(description="Developer assigned")
    related_components: List[str] = Field(description="Components involved")

class Configuration(BaseModel):
    """
    System configuration or settings.
    
    Extract when user mentions:
    - Config, configuration
    - Settings, parameters
    - Environment variables
    - System properties
    """
    name: str = Field(description="Configuration name")
    environment: str = Field(description="Environment: dev|staging|prod|local")
    category: str = Field(description="Category: database|api|security|performance")
    settings: dict = Field(description="Key-value configuration pairs")

class TechnicalDecision(BaseModel):
    """
    Architectural or implementation decision.
    
    Extract when user:
    - Makes technology choices
    - Decides between alternatives
    - Establishes patterns
    - Sets technical direction
    """
    decision_type: str = Field(description="Type: architecture|tool|pattern|approach")
    chosen: str = Field(description="What was chosen")
    alternatives: List[str] = Field(description="Options that were considered")
    rationale: str = Field(description="Why this choice was made")
    impact: Optional[str] = Field(description="Expected impact or trade-offs")
    date: str = Field(description="When decision was made")

class Issue(BaseModel):
    """
    Bug, problem, or issue encountered.
    
    Extract when user mentions:
    - Bugs, errors, issues
    - Problems, failures
    - Things not working
    - Unexpected behavior
    """
    title: str = Field(description="Brief issue description")
    severity: str = Field(description="Severity: critical|high|medium|low")
    status: str = Field(description="Status: open|investigating|resolved")
    component: str = Field(description="Affected component")
    description: str = Field(description="Detailed problem description")
    solution: Optional[str] = Field(description="How it was resolved")
    root_cause: Optional[str] = Field(description="Why it happened")
```

### Step 4: Quick Setup Commands

Add this to your project README:

```markdown
## AI Memory Setup

To enable AI memory for this project:

1. Initialize Graphiti:
```bash
graphiti init [project-name]
```

2. Copy entity definitions:
```bash
cp ai/graph/entities/project_entities.py ai/graph/entities/
```

3. Start the memory server:
```bash
graphiti compose && graphiti up -d
```

4. Configure your AI tool to use the MCP server at `http://localhost:800X/sse`
```

### What This Gives You

With these files in place, Claude will:

1. **Always search before acting** - No more repeating mistakes or ignoring preferences
2. **Build memory throughout conversations** - Every interaction adds to the knowledge
3. **Remember across sessions** - Previous decisions and patterns persist
4. **Understand your project deeply** - Accumulates context over time
5. **Follow established patterns** - Respects preferences and procedures

The key is that the instructions make memory usage MANDATORY, not optional. Claude must search before every action and capture information continuously.

## Danger zone
Setting `NEO4J_DESTROY_ENTIRE_GRAPH=true` wipes *all* projects the next time you run `graphiti up`. Use with care.

## Contributing
PRs and issues are welcome.

© 2025 rawr‑ai • MIT License
