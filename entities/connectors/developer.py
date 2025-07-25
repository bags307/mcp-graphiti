"""Developer entity for Graphiti MCP Server.

This module defines the Developer entity, which represents developer-specific working style and context.
"""

from pydantic import BaseModel, Field, ConfigDict


class Developer(BaseModel):
    """Developer-specific working style and context.

    Instructions for identifying and extracting developer context:
    1. Explicit statements about developer working style, patterns, expertise, and other relevant information.
    """

    model_config = ConfigDict(extra='forbid')

    developer_id: str = Field(..., description="Unique identifier for the developer.")
    developer_name: str = Field(..., description="Name of the developer.")
    expertise: list[str] = Field(default_factory=list, description="Areas of expertise.")
    working_style: str = Field(..., description="Developer's work patterns and habits.")
    projects: list[str] = Field(default_factory=list, description="List of projects the developer is involved in.")
    goals: list[str] = Field(default_factory=list, description="List of goals or objectives the developer is working on.")
    tools: list[str] = Field(default_factory=list, description="List of tools or capabilities the developer uses.")
    limitations: list[str] = Field(default_factory=list, description="List of limitations or constraints the developer faces.")

    @property
    def name(self) -> str:
        """Return the developer name for embedding purposes."""
        return self.developer_name
    