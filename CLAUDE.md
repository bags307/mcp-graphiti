# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Core Architecture

This repository implements a **Graphiti MCP (Model Context Protocol) Server ecosystem** that provides AI agents with knowledge graph capabilities using Neo4j as the backend database. The system supports multi-project isolation where each project can have its own entities, configuration, and graph namespace while sharing the same Neo4j instance.

### Key Components

- **MCP Server** (`graphiti_mcp_server.py`): Main server exposing Graphiti functionality via MCP protocol
- **CLI Tool** (`graphiti_cli/`): Management interface for Docker services and project configuration  
- **Entity System** (`entities/`): Modular entity definitions for knowledge graph extraction
- **Project Registry** (`mcp-projects.yaml`): Central configuration for managing multiple projects
- **Root Server**: Default server instance running on port 8000
- **Project Servers**: Individual MCP server instances for each registered project (ports 8001+)

## Common Development Tasks

### Testing
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=graphiti_cli --cov-report=html

# Run specific test files
pytest tests/unit/test_docker.py
pytest tests/functional/test_cli_commands.py
```

### Development Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# Install with uv (preferred)
uv pip sync uv.lock
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your Neo4j credentials and OpenAI API key
```

### Docker Services Management
```bash
# Generate docker-compose.yml from configurations
graphiti compose

# Start all services (builds images first)
graphiti up -d

# Stop services
graphiti down

# Restart services
graphiti restart -d

# Reload specific service container
graphiti reload mcp-project-name-server
```

### Project Management  
```bash
# Initialize new project (creates ai/graph structure)
graphiti init my-project /path/to/project

# Create entity set within project
cd /path/to/project
graphiti entity my-entities

# Setup Cursor rules for project
graphiti rules my-project /path/to/project
```

## Configuration Files

### Environment Configuration (`.env`)
Primary configuration file controlling:
- **Neo4j connection**: `NEO4J_USER`, `NEO4J_PASSWORD`, `NEO4J_URI`
- **OpenAI/LLM settings**: `OPENAI_API_KEY`, `MODEL_NAME`, `OPENAI_BASE_URL`
- **Root server config**: `MCP_ROOT_GROUP_ID`, `MCP_ROOT_HOST_PORT`
- **Logging**: `GRAPHITI_LOG_LEVEL`

### Project Registry (`mcp-projects.yaml`)
Central registry defining projects managed by the CLI:
```yaml
projects:
  project-name:
    root_dir: /absolute/path/to/project
    enabled: true
```

### Project Configuration (`ai/graph/mcp-config.yaml`)
Per-project MCP server configuration:
```yaml
services:
  - id: service-name
    group_id: namespace-for-graph-data
    entities_dir: "entities"  # or ["entities/core", "entities/custom"]
    include_root_entities: false
    port_default: 8002
    environment:
      GRAPHITI_LOG_LEVEL: debug
```

## Entity System

### Entity Loading Hierarchy
1. **Root entities** (`/app/entities/` in container) - loaded by default unless `include_root_entities: false`
2. **Project entities** (`ai/graph/entities/` in project) - loaded based on `entities_dir` configuration

### Entity Registration
Entities are automatically discovered and registered from Python files:
- Must be Pydantic `BaseModel` subclasses
- Must have docstrings
- Located in configured entity directories
- Registered via `entities/entity_registry.py`

### Entity Directory Structure
```
entities/
├── actions/          # Action-based entities
├── connectors/       # Agent/developer/project connectors  
├── constraints/      # Requirements and constraints
├── development/      # Development-specific entities
├── interaction/      # User interaction entities
└── resources/        # Artifacts and documentation
```

## Docker Architecture

### Service Structure
- **neo4j**: Shared Neo4j database instance
- **graphiti-mcp-root**: Root MCP server (port 8000)
- **mcp-{project}-{service}**: Project-specific MCP servers (ports 8001+)

### Volume Management
- `neo4j_data`: Persistent Neo4j database storage
- Project directories: Mounted read-only into containers

### Network Configuration
- All services communicate via Docker internal network
- Host ports exposed for external access (Neo4j: 7474/7687, MCP servers: 8000+)

## Key Development Patterns

### Entity Definition
```python
from pydantic import BaseModel

class MyEntity(BaseModel):
    """Entity description for LLM processing."""
    name: str
    description: str
    # Additional fields...
```

### MCP Tool Implementation
Tools are defined in `graphiti_mcp_server.py` using FastMCP decorators:
```python
@mcp.tool()
async def my_tool(param: str) -> Union[SuccessResponse, ErrorResponse]:
    """Tool description."""
    # Implementation
```

### CLI Command Structure
Commands in `graphiti_cli/commands/` follow patterns:
- Use Typer for argument parsing
- Delegate to logic modules in `graphiti_cli/logic/`
- Handle Docker operations via subprocess calls
- Provide colored output via constants

## Important Security Considerations

### Neo4j Password Security
- Default password `'password'` only allowed when `GRAPHITI_ENV=dev`
- Production deployments must use strong passwords
- Server refuses to start with weak passwords in non-dev environments

### Graph Clearing Operations
- `clear_graph` tool requires authorization code + explicit confirmation
- Only accessible from root group ID
- Permanently destroys ALL graph data across projects

## Logging and Debugging

### Log Levels
Configure via `GRAPHITI_LOG_LEVEL` environment variable:
- `debug`: Detailed execution information
- `info`: General operational messages (default)
- `warn`: Warning conditions
- `error`: Error conditions

### Container Logs
```bash
# View logs for all services
docker compose logs -f

# View logs for specific service  
docker compose logs -f graphiti-mcp-root
```

## Integration Points

### Cursor IDE Integration
- `.cursor/mcp.json` automatically updated with server configurations
- Symlinks created for project rules and schemas
- Entity templates provided for rapid development

### OpenRouter Support
Supports OpenRouter as alternative LLM provider with advanced provider routing:

**Basic Configuration:**
```bash
export OPENAI_BASE_URL=https://openrouter.ai/api/v1
export OPENAI_API_KEY=sk-or-your-openrouter-key
export MODEL_NAME=qwen/qwen-3-32b
```

**Provider Routing Options:**
```bash
# Force specific provider (e.g., Cerebras only)
export OPENROUTER_PROVIDER=cerebras
export OPENROUTER_ALLOW_FALLBACKS=false

# Preferred provider order with fallbacks
export OPENROUTER_PROVIDER_ORDER=cerebras,together,openai
export OPENROUTER_ALLOW_FALLBACKS=true
```

**Supported Providers:** anthropic, openai, cerebras, together, deepinfra, groq, and many others

**Cerebras Integration:**
The server includes special handling for Cerebras through OpenRouter:
- Automatically detects Cerebras in provider configuration
- Injects "JSON" into prompts when using structured output (required by Cerebras)
- Extends `OpenAIGenericClient` for better schema injection support
- Provider routing via `extra_body` parameter per OpenRouter API specification

## Troubleshooting

### Common Issues
- **Port conflicts**: Check `docker compose ps` and adjust port mappings
- **Entity loading failures**: Verify Python syntax and Pydantic model structure
- **Neo4j connection issues**: Confirm credentials and service startup order
- **Permission errors**: Ensure proper file ownership for mounted volumes

### Health Checks
```bash
# Verify setup
graphiti check-setup

# Check service status
curl http://localhost:8000/graphiti/status

# Neo4j browser
open http://localhost:7474
```