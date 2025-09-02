"""
MCP Server implementation using stdio communication for Claude Desktop integration.
"""

import json
import sys
from typing import Dict, Any, Optional
from src.calculator.operations import calculator
from src.utils.logger import logger


class MCPServer:
    """MCP Server that communicates via stdio."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.request_id = 0
        self.initialized = False
    
    def send_response(self, result: Any = None, error: Optional[Dict[str, Any]] = None):
        """Send a response to the client."""
        response = {
            "jsonrpc": "2.0",
            "id": self.request_id
        }
        
        if error:
            response["error"] = error
        else:
            response["result"] = result
        
        print(json.dumps(response), flush=True)
    
    def handle_initialize(self, params: Dict[str, Any]):
        """Handle initialize request."""
        logger.info("Initializing MCP server")
        self.initialized = True
        
        # Use the client's protocol version if available, otherwise default to 2024-11-05
        client_protocol_version = params.get("protocolVersion", "2024-11-05")
        logger.info(f"Client protocol version: {client_protocol_version}")
        
        # Return server capabilities
        capabilities = {
            "tools": {
                "listChanged": True,
                "listRequired": False
            }
        }
        
        self.send_response({
            "protocolVersion": client_protocol_version,
            "capabilities": capabilities,
            "serverInfo": {
                "name": "calculator-mcp-server",
                "version": "1.0.0"
            }
        })
    
    def handle_tools_list(self, params: Dict[str, Any]):
        """Handle tools/list request."""
        tools = [
            {
                "name": "add",
                "description": "Add two numbers",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "subtract",
                "description": "Subtract second number from first",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "multiply",
                "description": "Multiply two numbers",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                }
            },
            {
                "name": "divide",
                "description": "Divide first number by second",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "Numerator"},
                        "b": {"type": "number", "description": "Denominator"}
                    },
                    "required": ["a", "b"]
                }
            }
        ]
        
        self.send_response({"tools": tools})
    
    def handle_tools_call(self, params: Dict[str, Any]):
        """Handle tools/call request."""
        # Try different possible field names for tool calls
        tool_calls = params.get("calls", [])
        if not tool_calls:
            tool_calls = params.get("toolCalls", [])
        if not tool_calls:
            tool_calls = params.get("tool_calls", [])
        
        # Handle case where Claude Desktop sends tool call directly in params
        if not tool_calls and "name" in params and "arguments" in params:
            tool_calls = [{"name": params["name"], "arguments": params["arguments"]}]
            logger.info(f"Detected direct tool call in params: {tool_calls}")
        
        logger.info(f"Received tool calls: {tool_calls}")
        logger.info(f"Full params: {params}")
        results = []
        
        for call in tool_calls:
            tool_name = call.get("name")
            arguments = call.get("arguments", {})
            
            try:
                if tool_name == "add":
                    result = calculator.add(arguments.get("a"), arguments.get("b"))
                elif tool_name == "subtract":
                    result = calculator.subtract(arguments.get("a"), arguments.get("b"))
                elif tool_name == "multiply":
                    result = calculator.multiply(arguments.get("a"), arguments.get("b"))
                elif tool_name == "divide":
                    result = calculator.divide(arguments.get("a"), arguments.get("b"))
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                
                # Return the actual result value in the format Claude Desktop expects
                if "result" in result:
                    results.append({
                        "type": "text",
                        "text": str(result["result"])
                    })
                else:
                    results.append({
                        "type": "text",
                        "text": f"Error: {result.get('error', 'Unknown error')}"
                    })
                
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}")
                results.append({
                    "type": "text",
                    "text": f"Error: {str(e)}"
                })
        
        # Return results in the format expected by Claude Desktop
        # MCP tools/call expects a specific response structure
        self.send_response({
            "content": results
        })
    
    def handle_request(self, request: Dict[str, Any]):
        """Handle incoming requests."""
        method = request.get("method")
        params = request.get("params", {})
        self.request_id = request.get("id", 0)
        
        logger.info(f"Handling request: {method}")
        logger.info(f"Full request: {request}")
        
        try:
            if method == "initialize":
                self.handle_initialize(params)
            elif method == "notifications/initialized":
                # Handle initialization notification (no response needed)
                logger.info("Received initialization notification")
                return
            elif method == "tools/list":
                self.handle_tools_list(params)
            elif method == "tools/call":
                self.handle_tools_call(params)
            else:
                self.send_response(error={
                    "code": -32601,
                    "message": "Method not found",
                    "data": f"Unknown method: {method}"
                })
        except Exception as e:
            logger.error(f"Error handling request {method}: {str(e)}")
            self.send_response(error={
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            })
    
    def run(self):
        """Run the MCP server."""
        logger.info("Starting MCP Server (stdio mode)")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    self.handle_request(request)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {str(e)}")
                    self.send_response(error={
                        "code": -32700,
                        "message": "Parse error",
                        "data": str(e)
                    })
                except Exception as e:
                    logger.error(f"Unexpected error: {str(e)}")
                    self.send_response(error={
                        "code": -32603,
                        "message": "Internal error",
                        "data": str(e)
                    })
        except KeyboardInterrupt:
            logger.info("MCP Server stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {str(e)}")
            sys.exit(1)


def main():
    """Main entry point for the MCP server."""
    server = MCPServer()
    server.run()


if __name__ == "__main__":
    main()
