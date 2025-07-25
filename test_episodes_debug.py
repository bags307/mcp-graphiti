#!/usr/bin/env python3
"""
Test script for MCP Graphiti server episode functionality with debug logging.
This simulates what happens when MCP tools are called.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('episode_test_debug.log')
    ]
)

# Set specific loggers
logging.getLogger('graphiti_core').setLevel(logging.DEBUG)
logging.getLogger('neo4j').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

async def test_episodes_directly():
    """Test episode addition directly using Graphiti core (like MCP server does)."""
    
    from graphiti_core import Graphiti
    from graphiti_core.nodes import EpisodeType
    
    # Get connection info
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_user = os.getenv('NEO4J_USER') 
    neo4j_password = os.getenv('NEO4J_PASSWORD')
    
    logger.info(f"Testing episodes with Neo4j at: {neo4j_uri}")
    
    # Initialize Graphiti (same as MCP server does)
    graphiti = Graphiti(neo4j_uri, neo4j_user, neo4j_password)
    
    try:
        await graphiti.build_indices_and_constraints()
        
        # Test both text and JSON episodes
        test_cases = [
            {
                'name': 'Text Episode Test',
                'content': 'This is a text episode to test the debugging setup. Brian is working on the MCP server issue.',
                'episode_type': 'text',
                'description': 'Debug test episode'
            },
            {
                'name': 'JSON Episode Test', 
                'content': {
                    'developer': 'Brian',
                    'task': 'Debug JSON episodes in MCP server',
                    'status': 'testing',
                    'tools_used': ['graphiti-core', 'mcp', 'neo4j'],
                    'issue_description': 'JSON episodes may not be processing correctly'
                },
                'episode_type': 'json',
                'description': 'Structured debug test data'
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            logger.info(f"\\n{'='*50}")
            logger.info(f"TESTING EPISODE {i+1}: {test_case['name']}")
            logger.info(f"Type: {test_case['episode_type']}")
            logger.info(f"Content: {test_case['content']}")
            logger.info(f"{'='*50}")
            
            try:
                # Convert content to string if it's JSON (same as MCP server)
                episode_body = test_case['content']
                if isinstance(episode_body, dict):
                    episode_body = json.dumps(episode_body, indent=2)
                    logger.info(f"Converted JSON to string: {episode_body}")
                
                # Add episode (same as MCP add_episode tool)
                await graphiti.add_episode(
                    name=test_case['name'],
                    episode_body=episode_body,
                    source=EpisodeType.text if test_case['episode_type'] == 'text' else EpisodeType.json,
                    source_description=test_case['description'],
                    reference_time=datetime.now(timezone.utc),
                )
                
                logger.info(f"✅ Episode {i+1} added successfully!")
                
            except Exception as e:
                logger.error(f"❌ Episode {i+1} failed: {e}")
                logger.exception("Full exception:")
        
        # Test search functionality
        logger.info(f"\\n{'='*50}")
        logger.info("TESTING SEARCH FUNCTIONALITY")
        logger.info(f"{'='*50}")
        
        search_queries = [
            'Brian debugging MCP server',
            'JSON episodes issue',
            'developer task status'
        ]
        
        for query in search_queries:
            logger.info(f"\\nSearching for: '{query}'")
            try:
                results = await graphiti.search(query, limit=5)
                logger.info(f"Found {len(results)} results")
                
                for j, result in enumerate(results[:3]):  # Show top 3
                    logger.info(f"  {j+1}. {result.fact}")
                    
            except Exception as e:
                logger.error(f"❌ Search failed for '{query}': {e}")
                logger.exception("Search exception:")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        logger.exception("Full test exception:")
        
    finally:
        await graphiti.close()
        logger.info("✅ Test completed. Check episode_test_debug.log for full details.")

if __name__ == '__main__':
    logger.info("🚀 Starting episode debugging test...")
    asyncio.run(test_episodes_directly())