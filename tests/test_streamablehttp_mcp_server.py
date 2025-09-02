"""
Tests for the StreamableHttp MCP server using FastMCP.
"""

import pytest
import requests
import json
import time


class TestStreamableHttpMCPServer:
    """Test suite for the StreamableHttp MCP server using FastMCP."""
    
    @pytest.fixture
    def base_url(self):
        """Base URL for the StreamableHttp MCP server."""
        return "http://localhost:8000"
    
    @pytest.fixture
    def headers(self):
        """Headers for MCP requests."""
        return {
            "Content-Type": "application/json"
        }
    
    def test_root_endpoint(self, base_url):
        """Test the root endpoint."""
        response = requests.get(f"{base_url}/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "calculator-mcp-server"
        assert data["version"] == "1.0.0"
        assert data["transport"] == "streamablehttp"
        assert data["framework"] == "fastapi"
        assert "endpoints" in data
    
    def test_health_check(self, base_url):
        """Test the health check endpoint."""
        response = requests.get(f"{base_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["transport"] == "streamablehttp"
        assert data["framework"] == "fastapi"
    
    def test_mcp_initialize(self, base_url, headers):
        """Test MCP initialize request."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        assert data.get("error") is None
        assert "result" in data
        
        result = data["result"]
        assert "protocolVersion" in result
        assert "capabilities" in result
        assert "serverInfo" in result
    
    def test_mcp_tools_list(self, base_url, headers):
        """Test MCP tools/list request."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 2
        assert data.get("error") is None
        assert "result" in data
        
        result = data["result"]
        assert "tools" in result
        tools = result["tools"]
        
        # Check that all expected tools are present
        tool_names = [tool["name"] for tool in tools]
        assert "add" in tool_names
        assert "subtract" in tool_names
        assert "multiply" in tool_names
        assert "divide" in tool_names
    
    def test_mcp_tools_call_add(self, base_url, headers):
        """Test MCP tools/call with add operation."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "toolCalls": [
                    {
                        "name": "add",
                        "arguments": {"a": 5, "b": 3}
                    }
                ]
            }
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 3
        assert data.get("error") is None
        assert "result" in data
        
        # Check the result format
        result = data["result"]
        assert "name" in result
        assert "content" in result
        assert result["name"] == "add"
        content = result["content"]
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "8"
    
    def test_mcp_tools_call_subtract(self, base_url, headers):
        """Test MCP tools/call with subtract operation."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "toolCalls": [
                    {
                        "name": "subtract",
                        "arguments": {"a": 10, "b": 4}
                    }
                ]
            }
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 4
        assert data.get("error") is None
        assert "result" in data
        
        result = data["result"]
        assert "name" in result
        assert "content" in result
        assert result["name"] == "subtract"
        content = result["content"]
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "6"
    
    def test_mcp_tools_call_multiply(self, base_url, headers):
        """Test MCP tools/call with multiply operation."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "toolCalls": [
                    {
                        "name": "multiply",
                        "arguments": {"a": 6, "b": 7}
                    }
                ]
            }
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 5
        assert data.get("error") is None
        assert "result" in data
        
        result = data["result"]
        assert "name" in result
        assert "content" in result
        assert result["name"] == "multiply"
        content = result["content"]
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "42"
    
    def test_mcp_tools_call_divide(self, base_url, headers):
        """Test MCP tools/call with divide operation."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "toolCalls": [
                    {
                        "name": "divide",
                        "arguments": {"a": 20, "b": 5}
                    }
                ]
            }
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 6
        assert data.get("error") is None
        assert "result" in data
        
        result = data["result"]
        assert "name" in result
        assert "content" in result
        assert result["name"] == "divide"
        content = result["content"]
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert content[0]["text"] == "4.0"
    
    def test_mcp_tools_call_divide_by_zero(self, base_url, headers):
        """Test MCP tools/call with divide by zero error."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "toolCalls": [
                    {
                        "name": "divide",
                        "arguments": {"a": 10, "b": 0}
                    }
                ]
            }
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 7
        assert data.get("error") is None
        assert "result" in data
        
        result = data["result"]
        assert "name" in result
        assert "content" in result
        assert result["name"] == "divide"
        content = result["content"]
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert "Error" in content[0]["text"]
    
    def test_mcp_tools_call_unknown_tool(self, base_url, headers):
        """Test MCP tools/call with unknown tool."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 8,
            "method": "tools/call",
            "params": {
                "toolCalls": [
                    {
                        "name": "unknown_tool",
                        "arguments": {"a": 1, "b": 2}
                    }
                ]
            }
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 8
        assert data.get("error") is None
        assert "result" in data
        
        result = data["result"]
        assert "name" in result
        assert "content" in result
        assert result["name"] == "unknown_tool"
        content = result["content"]
        assert len(content) == 1
        assert content[0]["type"] == "text"
        assert "Error" in content[0]["text"]
    
    def test_mcp_tools_call_multiple_tools(self, base_url, headers):
        """Test MCP tools/call with multiple tools."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 9,
            "method": "tools/call",
            "params": {
                "toolCalls": [
                    {
                        "name": "add",
                        "arguments": {"a": 2, "b": 3}
                    },
                    {
                        "name": "multiply",
                        "arguments": {"a": 4, "b": 5}
                    }
                ]
            }
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 9
        assert data.get("error") is None
        assert "result" in data
        
        result = data["result"]
        assert "calls" in result
        calls = result["calls"]
        assert len(calls) == 2
        assert calls[0]["name"] == "add"
        assert calls[1]["name"] == "multiply"
        assert "content" in calls[0]
        assert "content" in calls[1]
        content0 = calls[0]["content"]
        content1 = calls[1]["content"]
        assert len(content0) == 1
        assert len(content1) == 1
        assert content0[0]["type"] == "text"
        assert content0[0]["text"] == "5"
        assert content1[0]["type"] == "text"
        assert content1[0]["text"] == "20"
    
    def test_mcp_method_not_found(self, base_url, headers):
        """Test MCP request with unknown method."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "unknown_method",
            "params": {}
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 10
        assert data.get("error") is not None
        
        error = data["error"]
        assert error["code"] == -32601
        assert "Method not found" in error["message"]
    
    def test_mcp_invalid_json(self, base_url, headers):
        """Test MCP request with invalid JSON."""
        response = requests.post(f"{base_url}/mcp", data="invalid json", headers=headers)
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_mcp_notifications_initialized(self, base_url, headers):
        """Test MCP notifications/initialized request."""
        request_data = {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "notifications/initialized",
            "params": {}
        }
        
        response = requests.post(f"{base_url}/mcp", json=request_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 11
        assert data.get("error") is None
        assert data.get("result") is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

