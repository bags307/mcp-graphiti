# Memory-Graph Usage Guide: Graphiti MCP Server

## Overview

The **memory-graph** MCP server (Graphiti) provides persistent memory and knowledge management for AI agents through a sophisticated knowledge graph. It transforms information into richly connected networks of entities and relationships, creating a dynamic, queryable memory store that evolves with new information.

## Core Concepts

### 🧠 **Memory Structure**
- **Episodes**: Content snippets (text, JSON, conversations) that get processed
- **Nodes**: Extracted entities (concepts, people, things, decisions, etc.)
- **Facts**: Relationships between entities with temporal metadata
- **Group IDs**: Namespaces that organize related data

### 🎯 **Key Capabilities**
1. **Intelligent Entity Extraction**: Automatically identifies and structures entities from text
2. **Relationship Discovery**: Finds and stores connections between entities
3. **Semantic Search**: Natural language queries across your knowledge graph
4. **Temporal Tracking**: Maintains creation times and validity of facts
5. **Multi-Project Support**: Separate knowledge graphs via group IDs

---

## 📋 Available MCP Tools

### **Core Memory Operations**

#### 🔧 `mcp_memory-bank_add_episode`
**Purpose**: Add information to your knowledge graph

**Parameters**:
- `name` (string): Descriptive name for the episode
- `episode_body` (string): The content to process
- `format` (string): How to interpret content - `'text'`, `'json'`, or `'message'`
- `source_description` (string, optional): Context about the source
- `uuid` (string, optional): Custom UUID for the episode
- `entity_subset` (list[string], optional): Limit extraction to specific entity types
- ⚠️ **Note**: Do NOT provide `group_id` parameter - it uses configured defaults

**Usage Examples**:
```javascript
// Add development work as text
mcp_memory-bank_add_episode({
  name: "Bug Fix Session",
  episode_body: "I fixed the authentication timeout bug in auth.py by increasing the session duration from 30 to 60 minutes. This was causing users to get logged out too frequently.",
  format: "text",
  source_description: "development work"
})

// Add structured data as JSON
mcp_memory-bank_add_episode({
  name: "Project Requirements",
  episode_body: "{\"project\": \"payment-system\", \"requirements\": [\"PCI compliance\", \"real-time processing\"], \"deadline\": \"Q2 2025\"}",
  format: "json"
})

// Add conversation transcript
mcp_memory-bank_add_episode({
  name: "Client Meeting",
  episode_body: "user: What's the timeline for the new feature?\nassistant: We can deliver the MVP in 6 weeks with core functionality.",
  format: "message"
})
```

#### 🔍 `mcp_memory-bank_search_nodes`
**Purpose**: Find entities (nodes) in your knowledge graph

**Parameters**:
- `query` (string): Natural language search query
- `group_ids` (list[string], optional): Filter by specific namespaces
- `max_nodes` (int): Maximum results to return (default: 10)
- `center_node_uuid` (string, optional): Focus search around specific entity
- `entity` (string, optional): Filter by entity type (`"Preference"`, `"Procedure"`, `"Requirement"`, etc.)

**Usage Examples**:
```javascript
// Find all preferences
mcp_memory-bank_search_nodes({
  query: "user preferences and settings",
  entity: "Preference",
  max_nodes: 5
})

// Find development-related decisions
mcp_memory-bank_search_nodes({
  query: "technical decisions about architecture",
  entity: "TechnicalDecision"
})

// Find entities related to a specific project
mcp_memory-bank_search_nodes({
  query: "payment system requirements",
  max_nodes: 15
})
```

#### 🔗 `mcp_memory-bank_search_facts`
**Purpose**: Find relationships (facts) between entities

**Parameters**:
- `query` (string): Natural language search query
- `group_ids` (list[string], optional): Filter by specific namespaces  
- `max_facts` (int): Maximum results to return (default: 10)
- `center_node_uuid` (string, optional): Focus search around specific entity

**Usage Examples**:
```javascript
// Find relationships about bug fixes
mcp_memory-bank_search_facts({
  query: "what bugs were fixed and how",
  max_facts: 8
})

// Find connections between developers and projects
mcp_memory-bank_search_facts({
  query: "which developers worked on which features"
})
```

### **Information Retrieval**

#### 📄 `mcp_memory-bank_get_episodes`
**Purpose**: Retrieve recent episodes from your memory

**Parameters**:
- `last_n` (int): Number of recent episodes to retrieve

**Usage Example**:
```javascript
// Get the 5 most recent episodes
mcp_memory-bank_get_episodes({
  last_n: 5
})
```

#### 🔍 `mcp_memory-bank_get_entity_edge`
**Purpose**: Get detailed information about a specific relationship

**Parameters**:
- `uuid` (string): UUID of the entity edge to retrieve

### **Management Operations**

#### 🗑️ `mcp_memory-bank_delete_episode`
**Purpose**: Remove an episode from the knowledge graph

**Parameters**:
- `uuid` (string): UUID of the episode to delete

#### 🗑️ `mcp_memory-bank_delete_entity_edge`
**Purpose**: Remove a relationship between entities

**Parameters**:
- `uuid` (string): UUID of the entity edge to delete

#### ⚠️ `mcp_memory-bank_clear_graph`
**Purpose**: Clear all data from the knowledge graph (DESTRUCTIVE!)

**Security**: Requires two-step authentication process
1. Call without `auth` parameter to get authorization code
2. Get explicit user permission
3. Call again with `auth: "{code}_DELETE_THIS_GRAPH"`

---

## 🏗️ Available Entities

Your memory-graph server includes these entity types for automatic extraction:

### **Development Entities**
- **🔧 CodeChange**: Tracks code modifications, fixes, and refactoring
  - Fields: `file_path`, `change_type`, `description`
- **🐛 BugReport**: Captures issues, errors, and unexpected behavior  
  - Fields: `component`, `severity`, `description`
- **⚙️ TechnicalDecision**: Records architectural and implementation choices
  - Fields: `decision_area`, `chosen_option`, `rationale`

### **Workflow Entities**
- **📋 Requirement**: Captures system and functional requirements
- **⚙️ Procedure**: Step-by-step processes and workflows
- **❤️ Preference**: User preferences and configuration choices

### **Interaction Entities**
- **💬 Feedback**: User feedback and evaluation responses
- **🤝 InteractionModel**: Conversation patterns and interaction styles

### **Resource Entities**
- **🛠️ Tool**: Software tools, APIs, and utilities
- **📚 Documentation**: Documentation, guides, and reference materials
- **📦 Artifact**: Generated files, builds, and deliverables
- **🔧 Resource**: General resources and assets

### **Connection Entities**
- **🤖 Agent**: AI agents, personas, and roles
- **👨‍💻 Developer**: Human developers and team members  
- **🎯 Goal**: Objectives, targets, and desired outcomes
- **📁 Project**: Projects, initiatives, and work packages

---

## 🚀 Best Practices

### **Before Starting Any Task**

#### 1. **Always Search First**
```javascript
// Search for relevant preferences
mcp_memory-bank_search_nodes({
  query: "user preferences for code style and formatting",
  entity: "Preference"
})

// Search for established procedures
mcp_memory-bank_search_nodes({
  query: "how to deploy applications",
  entity: "Procedure"
})

// Search for requirements
mcp_memory-bank_search_nodes({
  query: "security requirements for authentication",
  entity: "Requirement"
})
```

#### 2. **Search for Related Facts**
```javascript
// Find relationships relevant to your task
mcp_memory-bank_search_facts({
  query: "authentication security implementation decisions"
})
```

### **Always Save New Information**

#### 1. **Capture Requirements Immediately**
```javascript
// When user expresses a requirement
mcp_memory-bank_add_episode({
  name: "API Security Requirement",
  episode_body: "All API endpoints must use JWT authentication with 2-hour token expiration and refresh tokens stored securely.",
  format: "text",
  source_description: "client requirements meeting"
})
```

#### 2. **Document Procedures Clearly**
```javascript
// When you discover how something should be done
mcp_memory-bank_add_episode({
  name: "Deployment Procedure",
  episode_body: "To deploy to production: 1) Run tests, 2) Build Docker image, 3) Push to registry, 4) Update Kubernetes manifests, 5) Apply with kubectl, 6) Verify health checks",
  format: "text",
  source_description: "deployment workflow documentation"
})
```

#### 3. **Record Development Work**
```javascript
// Document code changes and decisions
mcp_memory-bank_add_episode({
  name: "Payment Integration Implementation",
  episode_body: "Implemented Stripe payment processing in payment-service.py. Chose Stripe over PayPal because of better webhook reliability and detailed transaction reporting. Added error handling for declined cards and network timeouts.",
  format: "text",
  source_description: "development session"
})
```

### **During Your Work**

#### 1. **Respect Discovered Preferences**
- Align your work with found preferences
- Follow established coding standards
- Use preferred tools and approaches

#### 2. **Follow Procedures Exactly**
- If you find a procedure for your current task, follow it step by step
- Don't deviate unless circumstances require it

#### 3. **Apply Relevant Facts**
- Use factual information to inform decisions
- Reference previous decisions and their rationales

#### 4. **Stay Consistent**
- Maintain consistency with previously identified patterns
- Build upon existing knowledge rather than creating conflicts

### **Search Strategies**

#### 1. **Combine Search Types**
```javascript
// First search for entities
const preferences = await mcp_memory-bank_search_nodes({
  query: "testing and quality assurance preferences",
  entity: "Preference"
});

// Then search for related facts
const relationships = await mcp_memory-bank_search_facts({
  query: "testing tools and quality assurance procedures"
});
```

#### 2. **Use Specific Queries**
```javascript
// ✅ Good: Specific and actionable
mcp_memory-bank_search_nodes({
  query: "React component testing with Jest and React Testing Library"
})

// ❌ Bad: Too vague
mcp_memory-bank_search_nodes({
  query: "testing"
})
```

#### 3. **Center Searches Around Key Entities**
```javascript
// Focus search around a specific project or component
mcp_memory-bank_search_facts({
  query: "authentication bugs and fixes",
  center_node_uuid: "uuid-of-auth-project-node"
})
```

### **Data Quality Tips**

#### 1. **Be Descriptive with Episode Names**
```javascript
// ✅ Good: Descriptive and searchable
name: "Database Schema Migration - Add User Preferences Table"

// ❌ Bad: Too generic
name: "Database Update"
```

#### 2. **Provide Rich Context**
```javascript
// Include context that helps with future searches
episode_body: "Fixed memory leak in image processing service (image-processor.py) by properly disposing of PIL Image objects after use. The leak was causing container memory usage to grow by 50MB per hour under normal load. Added explicit .close() calls and context managers.",
source_description: "performance optimization work"
```

#### 3. **Split Large Information**
```javascript
// Instead of one massive episode, split into logical chunks
// Episode 1: High-level decision
mcp_memory-bank_add_episode({
  name: "Architecture Decision - Microservices Approach",
  episode_body: "Decided to split monolithic application into microservices to improve scalability and team autonomy. Will start with user service, payment service, and notification service."
})

// Episode 2: Implementation details
mcp_memory-bank_add_episode({
  name: "User Service Implementation Details",
  episode_body: "User service will use PostgreSQL for data persistence, Redis for session storage, and expose REST API on port 3001. Authentication via JWT tokens with 2-hour expiration."
})
```

---

## 🔧 Advanced Usage

### **Temporal Context**
The knowledge graph maintains temporal information, so you can:
- Track when decisions were made
- Understand the evolution of requirements
- See how procedures have changed over time

### **Multi-Project Management**
Each project can have its own group_id for:
- Isolated knowledge graphs
- Project-specific entities
- Separate concern management

### **Hybrid Search Capabilities**
The system uses sophisticated search combining:
- **Vector similarity**: Semantic understanding
- **Full-text search**: Keyword matching
- **Graph traversal**: Relationship-based discovery
- **Advanced re-ranking**: MMR, Cross-encoder, RRF

---

## 🎯 Quick Start Workflow

1. **Initialize** - Always search first:
   ```javascript
   mcp_memory-bank_search_nodes({query: "preferences for current task", entity: "Preference"})
   ```

2. **Research** - Find related facts:
   ```javascript
   mcp_memory-bank_search_facts({query: "relevant context and relationships"})
   ```

3. **Work** - Respect found preferences and procedures

4. **Document** - Save new information immediately:
   ```javascript
   mcp_memory-bank_add_episode({
     name: "Descriptive Name",
     episode_body: "Detailed information...",
     format: "text"
   })
   ```

5. **Iterate** - Build upon the knowledge graph over time

---

**Remember**: The knowledge graph is your persistent memory. Use it consistently to provide personalized, context-aware assistance that builds upon previous interactions and maintains continuity across sessions. 