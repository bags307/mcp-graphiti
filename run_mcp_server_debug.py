#!/usr/bin/env python3
"""
Debug version of MCP Graphiti server with comprehensive logging.
Run from the mcp-graphiti/ directory to start server with detailed logs.
"""

import asyncio
import logging
import os
import sys
from logging import StreamHandler
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
        StreamHandler(sys.stdout),  # Console output
        logging.FileHandler('mcp_server_debug.log')  # File output
    ]
)

# Set specific loggers to appropriate levels
logging.getLogger('graphiti_core').setLevel(logging.DEBUG)
logging.getLogger('mcp').setLevel(logging.DEBUG)
logging.getLogger('neo4j').setLevel(logging.DEBUG)
logging.getLogger('httpx').setLevel(logging.INFO)  # Reduce HTTP noise
logging.getLogger('uvicorn').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

async def run_mcp_server():
    """Run the MCP server with debug logging."""
    
    # Import after setting up logging
    from mcp.server.stdio import stdio_server
    from graphiti_mcp_server import main as mcp_main
    
    logger.info("🚀 Starting MCP Graphiti Server with debug logging...")
    
    # Log environment configuration
    logger.info("=== ENVIRONMENT CONFIGURATION ===")
    logger.info(f"NEO4J_URI: {os.getenv('NEO4J_URI', 'Not set')}")
    logger.info(f"NEO4J_USER: {os.getenv('NEO4J_USER', 'Not set')}")
    logger.info(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    logger.info(f"MODEL_NAME: {os.getenv('MODEL_NAME', 'Not set')}")
    logger.info(f"GRAPHITI_LOG_LEVEL: {os.getenv('GRAPHITI_LOG_LEVEL', 'Not set')}")
    logger.info(f"MCP_ROOT_GROUP_ID: {os.getenv('MCP_ROOT_GROUP_ID', 'Not set')}")
    logger.info(f"MCP_ROOT_USE_CUSTOM_ENTITIES: {os.getenv('MCP_ROOT_USE_CUSTOM_ENTITIES', 'Not set')}")
    logger.info("====================================")
    
    try:
        # Run the main MCP server function
        await mcp_main()
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server failed: {e}")
        logger.exception("Full server exception details:")
        raise

if __name__ == '__main__':
    try:
        asyncio.run(run_mcp_server())
    except KeyboardInterrupt:
        logger.info("\\n👋 Server shutdown complete")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        sys.exit(1)