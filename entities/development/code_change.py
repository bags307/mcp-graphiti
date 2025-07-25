"""CodeChange entity for Graphiti MCP Server."""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class CodeChange(BaseModel):
    """Represents a modification to the codebase (commit, PR, or change).

    Instructions for identifying and extracting code changes:
    1. Look for mentions of code modifications ("added", "changed", "fixed", "updated")
    2. Identify commit messages, PR descriptions, or change narratives
    3. Extract who made the change (name or role, NEVER generic "developer")
    4. List all files that were modified
    5. Capture what the change does (summary) and why (description)
    6. Note the type of change (feature, fix, refactor, etc.)
    7. Extract the branch name if mentioned (e.g., "on main", "in feature branch")
    8. Extract commit hash or PR number if mentioned
    9. Note what bug or feature this relates to if mentioned
    10. Only extract explicitly stated information
    """

    model_config = ConfigDict(extra='forbid')

    author: str = Field(..., description="Person who made the change (name or role)")
    summary: str = Field(..., description="Brief summary of the change")
    change_type: str = Field(..., description="Type: feature|fix|refactor|performance|security|docs|test|config")
    files_changed: List[str] = Field(..., description="List of files that were modified")
    description: str = Field(..., description="Detailed description of what changed and why")
    branch: Optional[str] = Field(None, description="Git branch where change was made (e.g., 'main', 'feature/add-auth')")
    commit_hash: Optional[str] = Field(None, description="Git commit hash or identifier")
    pull_request_id: Optional[str] = Field(None, description="PR/MR number or identifier")
    fixes_issue: Optional[str] = Field(None, description="Bug or issue this change fixes")
    implements_feature: Optional[str] = Field(None, description="Feature this change implements")