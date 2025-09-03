"""
Main entry point for the Calculator MCP Server.
This file serves as the primary application entry point as required by AGENTS.md.
"""

import sys
import os

# Add the src directory to Python path for proper imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """
    Main entry point for the Calculator MCP Server.
    
    This server launches the StreamableHttp transport by default,
    providing HTTP-based MCP communication on port 8000.
    
    Usage:
        python main.py                    # Start HTTP server on 0.0.0.0:8000
    """
    # Start HTTP server by default
    from mcp_streamable_http_server import StreamableHttpMCPServer
    server = StreamableHttpMCPServer(host="0.0.0.0", port=8000)
    print("Starting HTTP MCP Server on 0.0.0.0:8000")
    server.run()

if __name__ == "__main__":
    main()
