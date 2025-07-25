"""TechnicalDecision entity for Graphiti MCP Server."""

from pydantic import BaseModel, Field


class TechnicalDecision(BaseModel):
    """
    **AI Persona:** You are an expert entity extraction assistant.
    
    **Task:** Identify and extract information about Technical Decisions mentioned in the provided text context.
    A TechnicalDecision represents an architectural or implementation choice made during development.

    **Context:** The user will provide text containing potential mentions of technology choices or decisions.

    **Extraction Instructions:**
    Your goal is to accurately populate the fields (`decision_area`, `chosen_option`, `rationale`) 
    based *only* on information explicitly or implicitly stated in the text.

    1.  **Identify Core Mentions:** Look for statements about technology choices ("We decided to use X", "We chose Y over Z").
    2.  **Extract Decision Area:** Identify the domain of the decision (architecture, framework, tool, etc.).
    3.  **Extract Chosen Option:** Capture the specific option or approach that was selected.
    4.  **Extract Rationale:** Document the reasoning, trade-offs, or constraints mentioned for the decision.
    5.  **Handle Ambiguity:** If information for a field is missing or unclear, indicate that.

    **Output Format:** Respond with the extracted data structured according to this Pydantic model.
    """

    decision_area: str = Field(
        ...,
        description='The area or domain of the technical decision (architecture, framework, tool, etc.).',
    )
    chosen_option: str = Field(
        ...,
        description='The option or approach that was chosen.',
    )
    rationale: str = Field(
        ...,
        description='The reasoning behind the decision. Only use information mentioned in the context.',
    ) 