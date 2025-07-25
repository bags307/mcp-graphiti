"""Insight entity for Graphiti MCP Server - A comprehensive, flexible entity for capturing insights."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class Insight(BaseModel):
    """Represents a key insight, observation, or conclusion that can relate to any other entity.
    
    This is the most flexible entity in the system - designed to capture important
    observations, learnings, conclusions, or strategic thoughts that emerge from
    conversations, analysis, or experience.

    Instructions for identifying and extracting insights:
    
    1. **Look for synthesis moments** - When information is being connected, analyzed, or conclusions drawn
    2. **Capture "aha moments"** - Realizations, discoveries, or breakthroughs
    3. **Extract strategic observations** - High-level thinking about direction, approach, or implications
    4. **Note important learnings** - Things learned from experience, failures, or successes
    5. **Identify patterns** - Recurring themes, trends, or relationships observed
    6. **Capture decision rationale** - The "why" behind decisions or recommendations
    7. **Extract implications** - What something means for the future or other areas
    8. **Note meta-observations** - Insights about processes, methods, or approaches themselves
    
    Examples of when to extract Insights:
    - "I realized that our API design approach isn't scaling well with team growth"
    - "The pattern I'm seeing is that performance issues always stem from database queries"
    - "This suggests we should prioritize developer experience over pure performance"
    - "What I learned from this outage is that our monitoring blind spots are in the message queues"
    - "The key insight here is that users care more about reliability than speed"
    - "This analysis reveals that our technical debt is concentrated in the authentication layer"
    - "I think the fundamental issue is that we're solving the wrong problem"
    - "The breakthrough came when we realized the bottleneck wasn't where we thought"
    
    Categories include:
    - technical: Architecture, implementation, performance insights
    - business: Market, user, strategy insights  
    - operational: Process, workflow, team insights
    - architectural: System design, patterns, trade-offs
    - user_experience: User behavior, needs, pain points
    - performance: Speed, efficiency, bottleneck insights
    - security: Vulnerability, threat, protection insights
    - organizational: Team dynamics, culture, structure
    - product: Feature, roadmap, positioning insights
    - process: Methodology, workflow, improvement insights
    """

    model_config = ConfigDict(extra='forbid')

    insight_title: str = Field(..., description="Concise title summarizing the insight")
    narrative: str = Field(..., description="Detailed explanation of the insight, observation, or conclusion")
    category: str = Field(..., description="Category: technical|business|operational|architectural|user_experience|performance|security|organizational|product|process")
    importance_level: str = Field(..., description="Importance: critical|high|medium|low")
    
    # Context and attribution
    source_context: Optional[str] = Field(None, description="Context where this insight emerged (meeting, analysis, incident, etc.)")
    attributed_to: Optional[str] = Field(None, description="Person who provided or discovered this insight")
    evidence: Optional[List[str]] = Field(None, description="Supporting evidence, data points, or observations")
    
    # Relationships and implications  
    related_entities: Optional[List[str]] = Field(None, description="Names of related entities (services, features, people, etc.)")
    implications: Optional[List[str]] = Field(None, description="What this insight means for future decisions or actions")
    action_items: Optional[List[str]] = Field(None, description="Specific actions that should be taken based on this insight")
    
    # Metadata
    confidence_level: str = Field(default="medium", description="Confidence: high|medium|low")
    time_sensitivity: Optional[str] = Field(None, description="How time-sensitive: immediate|short_term|long_term|ongoing")
    tags: Optional[List[str]] = Field(None, description="Additional tags for categorization and searchability")
    
    # Validation and evolution
    validation_status: str = Field(default="hypothesis", description="Status: hypothesis|validated|invalidated|needs_testing")
    contradicts: Optional[List[str]] = Field(None, description="Previous insights or assumptions this contradicts")
    supports: Optional[List[str]] = Field(None, description="Previous insights or decisions this supports")