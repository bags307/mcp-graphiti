"""GitRepository entity for Graphiti MCP Server."""

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GitRepository(BaseModel):
    """Represents a Git repository in the development ecosystem.

    Instructions for identifying and extracting git repositories:
    1. Look for repository names, URLs, or references
    2. Identify mentions of "repo", "repository", "git project"
    3. Extract the repository name or identifier
    4. Capture the URL if mentioned (GitHub, GitLab, etc.)
    5. Note the primary language if stated
    6. Extract the owner/organization if mentioned
    7. Only extract explicitly stated information
    """

    model_config = ConfigDict(extra='forbid')

    repo_name: str = Field(..., description="Repository name (e.g., 'mcp-graphiti')")
    url: Optional[str] = Field(None, description="Repository URL (e.g., 'https://github.com/org/repo')")
    owner: Optional[str] = Field(None, description="Owner or organization name")
    primary_language: Optional[str] = Field(None, description="Main programming language")
    description: Optional[str] = Field(None, description="Repository purpose or description")