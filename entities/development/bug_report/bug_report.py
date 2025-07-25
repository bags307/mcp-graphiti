"""BugReport entity for Graphiti MCP Server."""

from pydantic import BaseModel, Field, ConfigDict


class BugReport(BaseModel):
    """Represents a software defect, error, or issue that needs tracking and resolution.

    Instructions for identifying and extracting bug reports:
    1. Look for error messages, exceptions, failures ("not working", "broken", "fails")
    2. Identify mentions of "bug", "issue", "problem", "error", "defect"
    3. Extract the person who reported it (name or role, NEVER generic "user")
    4. Capture what component/service/feature is affected
    5. Note severity based on impact (critical, high, medium, low)
    6. Extract the description of what's wrong
    7. Only extract explicitly stated information
    """

    model_config = ConfigDict(extra='forbid')

    title: str = Field(..., description="Brief descriptive title of the bug")
    reporter: str = Field(..., description="Person who reported (name or role, NEVER generic 'user')")
    component: str = Field(..., description="Affected component, service, or feature")
    severity: str = Field(..., description="Impact level: critical|high|medium|low")
    description: str = Field(..., description="What's wrong and how it behaves")