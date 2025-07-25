"""Service entity for Graphiti MCP Server."""

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class Service(BaseModel):
    """Represents a service or microservice in the system architecture.

    Instructions for identifying and extracting services:
    1. Look for service names or microservice references
    2. Identify mentions of "service", "API", "backend", "frontend"
    3. Extract the service name and type
    4. Note what the service does (its responsibility)
    5. Capture the tech stack if mentioned
    6. Extract dependencies on other services
    7. Only extract explicitly stated information
    """

    model_config = ConfigDict(extra='forbid')

    name: str = Field(..., description="Service name (e.g., 'auth-service', 'user-api')")
    service_type: str = Field(..., description="Type: backend|frontend|api|worker|database|cache")
    responsibility: str = Field(..., description="What this service does")
    tech_stack: Optional[List[str]] = Field(None, description="Technologies used (e.g., ['Node.js', 'Express', 'PostgreSQL'])")
    depends_on: Optional[List[str]] = Field(None, description="Other services this depends on")
    repository: Optional[str] = Field(None, description="Git repository containing this service")