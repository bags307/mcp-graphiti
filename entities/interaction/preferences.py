"""Preference entity for Graphiti MCP Server."""

from pydantic import BaseModel, Field, ConfigDict


class Preference(BaseModel):
    """Represents a person's expressed preference or preference pattern.

    Instructions for identifying and extracting preferences:
    1. Look for preference expressions ("I prefer", "I like", "always use", "never do")
    2. Identify who has the preference (name or role, NEVER generic "user")
    3. Capture what the preference is about (category)
    4. Extract the specific preference
    5. Note the strength if mentioned (strong, moderate, slight)
    6. Only extract explicitly stated preferences
    """

    model_config = ConfigDict(extra='forbid')

    person: str = Field(..., description="Person who has this preference (name or role)")
    category: str = Field(..., description="Category: coding_style|tools|workflow|design|communication")
    preference: str = Field(..., description="The specific preference")
    strength: str = Field(default="moderate", description="Strength: strong|moderate|slight")