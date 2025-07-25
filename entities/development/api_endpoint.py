"""APIEndpoint entity for Graphiti MCP Server - Comprehensive API endpoint tracking."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class APIEndpoint(BaseModel):
    """Represents an API endpoint (REST, GraphQL, RPC, WebSocket) in a service or application.
    
    This entity comprehensively tracks API routes, endpoints, and web services with
    detailed information about their behavior, requirements, and characteristics.

    Instructions for identifying and extracting API endpoints:
    
    1. **HTTP/REST endpoints** - Look for method + path combinations:
       - GET /api/v1/users, POST /users/:id/settings
       - Route definitions in code, API documentation
       
    2. **GraphQL endpoints** - Look for GraphQL schemas, queries, mutations:
       - query getUserProfile, mutation createUser
       - Schema definitions, resolver functions
       
    3. **RPC/gRPC endpoints** - Look for service methods:
       - UserService.GetUser, CreateUser method
       - Service definitions, proto files
       
    4. **WebSocket endpoints** - Look for real-time connections:
       - ws://api.example.com/chat, Socket.IO namespaces
       - Event handlers, connection endpoints
       
    5. **Webhook endpoints** - Look for callback URLs:
       - POST /webhooks/github, payment callback endpoints
       - External service integration points
    
    Examples of when to extract API endpoints:
    - "The GET /api/v1/users endpoint returns paginated user data"
    - "We need to add authentication to the POST /orders endpoint"
    - "The GraphQL mutation createProject requires admin permissions"
    - "The WebSocket /chat endpoint handles real-time messaging"
    - "The webhook at /webhooks/stripe processes payment events"
    - "The health check endpoint /health returns service status"
    
    Extract comprehensive details when available:
    - Request/response schemas and examples
    - Authentication and authorization requirements  
    - Rate limiting and performance characteristics
    - Error responses and status codes
    - Versioning and deprecation information
    """

    model_config = ConfigDict(extra='forbid')

    # Core identification
    endpoint_name: str = Field(..., description="Descriptive name for this endpoint (e.g., 'Get User Profile', 'Create Order')")
    method: str = Field(..., description="HTTP method: GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD|CONNECT|TRACE or GraphQL|RPC|WebSocket|Webhook")
    path: str = Field(..., description="URL path pattern (e.g., '/api/v1/users/:id', 'query getUserProfile', 'UserService.GetUser')")
    service: str = Field(..., description="Service, application, or component that provides this endpoint")
    
    # Functionality and purpose
    purpose: str = Field(..., description="What this endpoint does and its business purpose")
    endpoint_type: str = Field(..., description="Type: rest|graphql|grpc|websocket|webhook|health_check|internal|public")
    
    # Request/Response specifications
    request_schema: Optional[Dict[str, Any]] = Field(None, description="Request body schema, parameters, or GraphQL variables")
    response_schema: Optional[Dict[str, Any]] = Field(None, description="Response schema, data structure, or possible return types")
    request_example: Optional[str] = Field(None, description="Example request payload or parameters")
    response_example: Optional[str] = Field(None, description="Example successful response")
    
    # Security and access control
    auth_required: Optional[bool] = Field(None, description="Whether authentication is required")
    auth_method: Optional[str] = Field(None, description="Authentication method: bearer_token|api_key|basic_auth|oauth2|session|none")
    permissions_required: Optional[List[str]] = Field(None, description="Required permissions, roles, or scopes")
    access_level: Optional[str] = Field(None, description="Access level: public|internal|private|admin")
    
    # Performance and operational characteristics
    rate_limits: Optional[Dict[str, Any]] = Field(None, description="Rate limiting configuration (requests per minute, burst limits, etc.)")
    timeout_ms: Optional[int] = Field(None, description="Request timeout in milliseconds")
    cache_behavior: Optional[str] = Field(None, description="Caching behavior: no_cache|cache_5min|cache_1hour|conditional|etc.")
    performance_sla: Optional[str] = Field(None, description="Performance SLA or expected response time (e.g., '<100ms p95')")
    
    # Versioning and lifecycle
    api_version: Optional[str] = Field(None, description="API version (e.g., 'v1', '2.0', '2024-01-15')")
    status: str = Field(default="active", description="Status: active|deprecated|experimental|planned|disabled")
    deprecation_date: Optional[str] = Field(None, description="When this endpoint will be deprecated (ISO date)")
    replacement_endpoint: Optional[str] = Field(None, description="Replacement endpoint if deprecated")
    
    # Error handling and monitoring
    possible_errors: Optional[List[str]] = Field(None, description="Common error responses and status codes")
    monitoring_enabled: Optional[bool] = Field(None, description="Whether this endpoint is monitored for performance/errors")
    alerting_rules: Optional[List[str]] = Field(None, description="Alerting rules or SLA violations that trigger alerts")
    
    # Dependencies and relationships
    depends_on_services: Optional[List[str]] = Field(None, description="Other services this endpoint depends on")
    used_by_clients: Optional[List[str]] = Field(None, description="Known clients, applications, or services that use this endpoint")
    database_tables: Optional[List[str]] = Field(None, description="Database tables this endpoint reads from or writes to")
    
    # Documentation and metadata
    documentation_url: Optional[str] = Field(None, description="Link to API documentation or specification")
    openapi_spec: Optional[str] = Field(None, description="OpenAPI/Swagger specification reference")
    tags: Optional[List[str]] = Field(None, description="Tags for categorization (e.g., ['user-management', 'public-api', 'critical'])")
    notes: Optional[str] = Field(None, description="Additional notes, quirks, or important implementation details")

    @property
    def name(self) -> str:
        """Return the endpoint name for embedding purposes."""
        return self.endpoint_name