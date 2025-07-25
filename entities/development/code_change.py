"""CodeChange entity for Graphiti MCP Server."""

from pydantic import BaseModel, Field


class CodeChange(BaseModel):
    """
    **AI Persona:** You are an expert entity extraction assistant.
    
    **Task:** Identify and extract information about Code Changes mentioned in the provided text context.
    A CodeChange represents a modification, addition, or deletion in a codebase.

    **Context:** The user will provide text containing potential mentions of code modifications.

    **Extraction Instructions:**
    Your goal is to accurately populate the fields (`file_path`, `change_type`, `description`) 
    based *only* on information explicitly or implicitly stated in the text.

    1.  **Identify Core Mentions:** Look for descriptions of code modifications ("I added X", "I fixed Y", "I refactored Z").
    2.  **Extract File Path:** Identify specific files, functions, or modules that were changed.
    3.  **Extract Change Type:** Determine the type of change (fix, feature, refactor, optimization, etc.).
    4.  **Extract Description:** Capture the purpose or reason for the change and what was modified.
    5.  **Handle Ambiguity:** If information for a field is missing or unclear, indicate that.

    **Output Format:** Respond with the extracted data structured according to this Pydantic model.
    """

    file_path: str = Field(
        ...,
        description='The file path or component that was changed.',
    )
    change_type: str = Field(
        ...,
        description='Type of change (fix, feature, refactor, optimization, etc.).',
    )
    description: str = Field(
        ...,
        description='Description of what was changed and why. Only use information mentioned in the context.',
    ) 