"""APIEndpoint entity for Graphiti MCP Server."""

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class APIEndpoint(BaseModel):
    """Represents an API endpoint (REST, GraphQL, RPC) in a service.

    Instructions for identifying and extracting API endpoints:
    1. Look for HTTP methods with paths (GET /users, POST /api/v1/items)
    2. Identify route definitions, endpoint documentation
    3. Extract the HTTP method and path pattern
    4. Note what service/component provides this endpoint
    5. Capture the purpose or functionality
    6. Extract request/response types if mentioned
    7. Only extract explicitly stated information
    """

    model_config = ConfigDict(extra='forbid')

    method: str = Field(..., description="HTTP method: GET|POST|PUT|DELETE|PATCH")
    path: str = Field(..., description="URL path pattern (e.g., '/api/v1/users/:id')")
    service: str = Field(..., description="Service that provides this endpoint")
    purpose: str = Field(..., description="What this endpoint does")
    request_type: Optional[str] = Field(None, description="Expected request body type/schema")
    response_type: Optional[str] = Field(None, description="Response type/schema")
    auth_required: Optional[bool] = Field(None, description="Whether authentication is required")