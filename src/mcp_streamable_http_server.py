"""
MCP Server implementation using FastAPI for StreamableHttp transport.
This server supports HTTP POST requests for MCP communication.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from src.calculator.operations import calculator
from src.utils.logger import logger


class MCPRequest(BaseModel):
    """MCP request model."""
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    method: str
    params: Optional[Dict[str, Any]] = None


class MCPResponse(BaseModel):
    """MCP response model."""
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class StreamableHttpMCPServer:
    """MCP Server that communicates via StreamableHttp transport."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        """Initialize the StreamableHttp MCP server."""
        self.host = host
        self.port = port
        self.initialized = False
        self.app = FastAPI(title="Calculator MCP Server", version="1.0.0")
        self.setup_routes()
    
    def setup_routes(self):
        """Setup FastAPI routes."""
        
        @self.app.get("/")
        async def root():
            """Root endpoint."""
            return {
                "name": "calculator-mcp-server",
                "version": "1.0.0",
                "transport": "streamablehttp",
                "framework": "fastapi",
                "endpoints": {
                    "health": "GET /health",
                    "mcp": "POST /mcp"
                }
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {
                "status": "healthy", 
                "transport": "streamablehttp",
                "framework": "fastapi"
            }
        
        @self.app.post("/mcp")
        async def handle_mcp_request(request: MCPRequest):
            """Handle MCP requests via HTTP POST."""
            try:
                response = await self.process_mcp_request(request)
                # Return the response directly without wrapping in MCPResponse
                # This ensures proper JSON-RPC format for MCP Inspector
                return response
            except Exception as e:
                logger.error(f"Error processing MCP request: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def process_mcp_request(self, request: MCPRequest) -> Dict[str, Any]:
        """Process MCP requests."""
        method = request.method
        params = request.params or {}
        request_id = request.id
        
        logger.info(f"Processing MCP request: {method}")
        
        try:
            if method == "initialize":
                return await self.handle_initialize(params, request_id)
            elif method == "notifications/initialized":
                logger.info("Received initialization notification")
                return {"jsonrpc": "2.0", "id": request_id}
            elif method == "tools/list":
                return await self.handle_tools_list(params, request_id)
            elif method == "tools/call":
                return await self.handle_tools_call(params, request_id)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": "Method not found",
                        "data": f"Unknown method: {method}"
                    }
                }
        except Exception as e:
            logger.error(f"Error processing request {method}: {str(e)}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": "Internal error",
                    "data": str(e)
                }
            }
    
    async def handle_initialize(self, params: Dict[str, Any], request_id: int) -> Dict[str, Any]:
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
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": client_protocol_version,
                "capabilities": capabilities,
                "serverInfo": {
                    "name": "calculator-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    
    async def handle_tools_list(self, params: Dict[str, Any], request_id: int) -> Dict[str, Any]:
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
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["a", "b"]
                }
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }
    
    async def handle_tools_call(self, params: Dict[str, Any], request_id: int) -> Dict[str, Any]:
        """Handle tools/call request."""
        logger.info(f"Tools call params: {params}")
        # Try different possible parameter names that MCP clients might use
        tool_calls = params.get("toolCalls", params.get("calls", params.get("tool_calls", [])))
        
        # If no toolCalls array found, check if the tool call is directly in params
        if not tool_calls and "name" in params:
            tool_calls = [params]
            
        logger.info(f"Tool calls extracted: {tool_calls}")
        results = []
        
        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("arguments", {})
            
            logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
            
            try:
                # Execute the calculator operation
                if tool_name == "add":
                    result = calculator.add(tool_args.get("a"), tool_args.get("b"))
                elif tool_name == "subtract":
                    result = calculator.subtract(tool_args.get("a"), tool_args.get("b"))
                elif tool_name == "multiply":
                    result = calculator.multiply(tool_args.get("a"), tool_args.get("b"))
                elif tool_name == "divide":
                    result = calculator.divide(tool_args.get("a"), tool_args.get("b"))
                else:
                    result = {"error": f"Unknown tool: {tool_name}"}
                
                # Format the result
                if "error" not in result:
                    results.append({
                        "name": tool_name,
                        "content": [{
                            "type": "text",
                            "text": str(result["result"])
                        }]
                    })
                else:
                    results.append({
                        "name": tool_name,
                        "content": [{
                            "type": "text",
                            "text": f"Error: {result.get('error', 'Unknown error')}"
                        }]
                    })
                
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {str(e)}")
                results.append({
                    "type": "text",
                    "text": f"Error: {str(e)}"
                })
        
        # Return results in the format expected by MCP clients
        # Return results in the format that MCP clients expect
        # Some clients expect results directly, others expect them in a calls array
        logger.info(f"Returning results: {results}")
        
        # Return results in the format that MCP clients expect
        # Based on MCP specification, tools/call should return results in a specific format
        logger.info(f"Returning results: {results}")
        
        # For single tool calls, return the result directly
        # For multiple tool calls, return them in a calls array
        if len(results) == 1:
            single_result = results[0]
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "name": single_result["name"],
                    "content": single_result["content"]
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "calls": results
                }
            }
    
    def run(self):
        """Run the StreamableHttp MCP server."""
        logger.info(f"Starting MCP Server (StreamableHttp mode) on {self.host}:{self.port}")
        logger.info("Using FastAPI framework")
        
        # Run the server using uvicorn
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="info")


def main():
    """Main entry point for the StreamableHttp MCP server."""
    import os
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    server = StreamableHttpMCPServer(host=host, port=port)
    server.run()


if __name__ == "__main__":
    main()
