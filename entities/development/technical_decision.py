"""TechnicalDecision entity for Graphiti MCP Server."""

from pydantic import BaseModel, Field, ConfigDict


class TechnicalDecision(BaseModel):
    """Represents an architectural or technology choice made during development.

    Instructions for identifying and extracting technical decisions:
    1. Look for decision language ("we decided", "chose", "selected", "going with")
    2. Identify technology or architecture choices being made
    3. Extract who made the decision (names or roles, NEVER generic "team")
    4. Capture what was chosen and why
    5. Note the area of decision (database, architecture, framework, etc.)
    6. Only extract explicitly stated information
    """

    model_config = ConfigDict(extra='forbid')

    title: str = Field(..., description="Brief descriptive title of the decision")
    decision_maker: str = Field(..., description="Person(s) who made the decision (names or roles)")
    decision_area: str = Field(..., description="Area: architecture|database|framework|language|infrastructure|security")
    chosen_option: str = Field(..., description="What was chosen")
    rationale: str = Field(..., description="Why this choice was made")