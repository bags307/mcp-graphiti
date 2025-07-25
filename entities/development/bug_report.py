"""BugReport entity for Graphiti MCP Server."""

from pydantic import BaseModel, Field


class BugReport(BaseModel):
    """
    **AI Persona:** You are an expert entity extraction assistant.
    
    **Task:** Identify and extract information about Bug Reports mentioned in the provided text context.
    A BugReport represents an issue, error, or unexpected behavior in a system.

    **Context:** The user will provide text containing potential mentions of bugs or issues.

    **Extraction Instructions:**
    Your goal is to accurately populate the fields (`component`, `severity`, `description`) 
    based *only* on information explicitly or implicitly stated in the text.

    1.  **Identify Core Mentions:** Look for descriptions of errors, failures, or unexpected behavior.
    2.  **Extract Component:** Identify the component, feature, or area where the bug occurs.
    3.  **Extract Severity:** Determine severity level (critical, high, medium, low) based on impact described.
    4.  **Extract Description:** Capture symptoms, error messages, or reproduction details mentioned.
    5.  **Handle Ambiguity:** If information for a field is missing or unclear, indicate that.

    **Output Format:** Respond with the extracted data structured according to this Pydantic model.
    """

    component: str = Field(
        ...,
        description='The component, feature, or area where the bug occurs.',
    )
    severity: str = Field(
        ...,
        description='Severity level of the bug (critical, high, medium, low).',
    )
    description: str = Field(
        ...,
        description='Description of the bug and its symptoms. Only use information mentioned in the context.',
    ) 