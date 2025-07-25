# Graphiti Rules Documentation

This directory contains rule documents for working with the Graphiti MCP server. The rules are organized into two formats to support different AI agents and development environments.

## Directory Structure

```
rules/
├── ai-agents/          # Universal AI agent documentation
│   ├── graphiti-mcp-core-rules.md
│   ├── graphiti-knowledge-graph-maintenance.md
│   ├── graphiti-quick-reference.md
│   ├── graphiti-common-patterns.md
│   ├── graphiti-troubleshooting.md
│   └── examples/
│       └── schema-template.md
├── cursor/             # Cursor IDE-specific rules
│   ├── graphiti-mcp-core-rules.md
│   ├── graphiti-knowledge-graph-maintenance.md
│   └── examples/
│       └── graphiti-example-schema.md
├── templates/          # Shared templates
│   └── schema_template.py
└── README.md          # This file
```

## For AI Agents (Claude, GPT, etc.)

The `ai-agents/` directory contains documentation optimized for any AI agent:

1. **Start Here**: Read `graphiti-quick-reference.md` for a quick overview of available tools
2. **Core Guide**: Use `graphiti-mcp-core-rules.md` for comprehensive usage instructions
3. **Patterns**: Check `graphiti-common-patterns.md` for proven extraction and search patterns
4. **Troubleshooting**: Consult `graphiti-troubleshooting.md` when encountering issues
5. **Schema Updates**: Follow `graphiti-knowledge-graph-maintenance.md` to propose schema changes

### Key Features of AI Agent Docs
- Explicit file paths (no IDE-specific syntax)
- Concrete code examples for each concept
- Step-by-step procedures
- Error handling guidance
- MCP tool usage examples

## For Cursor IDE Users

The `cursor/` directory contains the original Cursor-optimized rules:

- Uses `@` syntax for file references
- Includes YAML frontmatter with `globs` and `alwaysApply`
- Integrated with Cursor's rule system

## Creating Project-Specific Schemas

Use the templates to create schemas for new projects:

1. **For AI Agents**: Copy `ai-agents/examples/schema-template.md`
2. **For Cursor**: Copy `templates/schema_template.py`

Customize the template with your project's:
- Entity definitions
- Relationship types
- Extraction rules
- Validation guidelines

## Best Practices

1. **AI Agents**: Start with AGENT_INSTRUCTIONS.md at the repository root
2. **Keep Both Versions in Sync**: When updating rules, update both versions
3. **Test Examples**: Ensure all code examples work with current implementation
4. **Version Control**: Document significant changes to rule structures

## Contributing

When adding new documentation:
1. Create both AI-agent and Cursor versions if applicable
2. Include practical examples
3. Test all code snippets
4. Update this README if adding new files

## Migration Notes

The original Cursor-specific files have been preserved in the `cursor/` directory. The new `ai-agents/` directory provides equivalent functionality with universal compatibility.