# Calculator MCP Server

A simple Model Context Protocol (MCP) server that provides basic arithmetic operations (addition, subtraction, multiplication, division) for integration with Claude Desktop and other AI assistants.

## Features

- **Basic Arithmetic Operations**: Add, subtract, multiply, and divide two numbers
- **MCP Protocol Compliance**: Implements the Model Context Protocol for seamless AI integration
- **Docker-First Design**: Containerized for consistent deployment and testing
- **Error Handling**: Robust error handling for invalid inputs and division by zero
- **JSON-RPC 2.0**: Uses JSON-RPC 2.0 for communication
- **Stdio-Based Communication**: Direct process communication for Claude Desktop integration

## Prerequisites

- **Docker and Docker Compose** (required)
- **Claude Desktop** (for MCP integration)

## Quick Start

### 1. Clone and Deploy

```bash
git clone <repository-url>
cd calculator-mcp-server
make setup
```

**Or manually:**
```bash
docker compose up --build -d
```

### 2. Verify Server is Running

```bash
# Check container status
make status

# Test the MCP server
make verify
```

### 3. Connect to Claude Desktop

Follow the detailed setup instructions below to connect this MCP server to Claude Desktop.

## Claude Desktop MCP Setup

### Step 1: Prepare the MCP Server

1. **Start the server** (if not already running):
   ```bash
   make setup
   ```

2. **Verify the server is accessible**:
   ```bash
   make verify
   ```
   The server should start and wait for input via stdin.

### Step 2: Configure Claude Desktop

**Important**: MCP servers must be executable processes, not HTTP endpoints. The server needs to run as a process that Claude Desktop can communicate with directly.

**Note**: This project provides a stdio-based MCP server (`src/mcp_stdio_server.py`) for Claude Desktop integration.

1. **Open Claude Desktop**

2. **Access Developer Settings**:
   - Go to **Settings** (gear icon)
   - Click **Developer**
   - Click **Edit Config**

3. **Add MCP Server Configuration**:
   Add the following configuration to your Claude Desktop config file:

   ```json
   {
     "mcpServers": {
       "calculator-mcp": {
         "command": "docker",
         "args": ["compose", "-f", "/Path/to/your/docker-compose.yml", "exec", "-T", "calculator-mcp-server", "python", "src/mcp_stdio_server.py"]
       }
     }
   }
   ```

   **Important**: Replace `/Path/to/your/docker-compose.yml` with the actual path to your docker-compose.yml file.
   
   **To find your project path**:
   ```bash
   make path
   ```
   This will show you the exact path and configuration to use.

4. **Alternative Direct Python Configuration**:
   If the Docker command approach doesn't work, you can also try running the Python script directly:

   ```json
   {
     "mcpServers": {
       "calculator-mcp": {
         "command": "python",
         "args": ["src/mcp_stdio_server.py"],
         "cwd": "/path/to/your/calculator-mcp-server"
       }
     }
   }
   ```

   **Note**: This requires Python and all dependencies to be installed locally, which goes against our Docker-first approach but may work as a fallback.

5. **Save and Restart**:
   - Save the config file
   - Restart Claude Desktop for changes to take effect

### Step 3: Using the Calculator in Claude

Once connected, you can use the calculator directly in Claude conversations:

```
Claude, can you add 15 and 27 using the calculator MCP server?
```

Claude will use the MCP server to perform the calculation and return the result.

### Available Operations

The calculator supports these operations via MCP:

- **Addition**: `add(a, b)` - Adds two numbers
- **Subtraction**: `subtract(a, b)` - Subtracts the second number from the first
- **Multiplication**: `multiply(a, b)` - Multiplies two numbers
- **Division**: `divide(a, b)` - Divides the first number by the second

### Example Claude Interactions

```
User: "What's 42 divided by 7?"
Claude: "Let me calculate that using the calculator MCP server... 42 ÷ 7 = 6"

User: "Can you multiply 8 and 9?"
Claude: "Using the calculator MCP server: 8 × 9 = 72"

User: "What's 100 minus 23?"
Claude: "Calculating with the MCP server: 100 - 23 = 77"
```

## MCP Protocol Documentation

### Available Tools

The MCP server provides the following calculator tools:

- **add** - Add two numbers
- **subtract** - Subtract second number from first
- **multiply** - Multiply two numbers
- **divide** - Divide first number by second

### MCP Protocol Flow

1. **Initialize**: Server responds with capabilities and server info
2. **Tools List**: Server provides available calculator tools
3. **Tools Call**: Server executes calculator operations and returns results

### Example MCP Communication

**Initialize Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "claude-ai", "version": "0.1.0"}
  }
}
```

**Tools Call Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "calls": [
      {
        "name": "add",
        "arguments": {"a": 5, "b": 3}
      }
    ]
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "name": "add",
        "content": [{"type": "text", "text": "8"}]
      }
    ]
  }
}
```

## Makefile Commands

The project includes a Makefile with convenient commands for common tasks:

### Quick Commands

```bash
make setup     # Complete setup before starting Claude Desktop
make verify    # Quick verification that everything works
make status    # Check container status
make logs      # Show container logs
make test      # Run all tests
make clean     # Clean up containers and images
```

### Available Commands

- **`make setup`** - Complete setup: build, start, and verify MCP server
- **`make build`** - Build the Docker container
- **`make start`** - Start the MCP server container
- **`make stop`** - Stop the MCP server container
- **`make restart`** - Restart the MCP server container
- **`make test`** - Run all tests
- **`make test-coverage`** - Run tests with coverage report
- **`make verify`** - Verify MCP server is working correctly
- **`make status`** - Check container status
- **`make logs`** - Show container logs
- **`make clean`** - Stop containers and remove images
- **`make rebuild`** - Clean and rebuild everything from scratch
- **`make health`** - Quick health check
- **`make path`** - Show project path for Claude Desktop configuration
- **`make dev`** - Development workflow setup
- **`make prod`** - Production-like setup

### Usage Examples

```bash
# Before starting Claude Desktop
make setup

# Quick verification
make verify

# Get configuration path
make path

# Development workflow
make dev
```

## Docker-Based Development

### Running Tests

All testing is performed in Docker containers for consistency:

```bash
# Run all tests
docker compose exec calculator-mcp-server bash -c "cd tests && python -m pytest -v"

# Run tests with coverage
docker compose exec calculator-mcp-server bash -c "cd tests && python -m pytest --cov=../src --cov-report=term-missing"

# Run specific test file
docker compose exec calculator-mcp-server bash -c "cd tests && python -m pytest test_calculator.py -v"
```

### Code Quality Checks

```bash
# Run linting
docker compose exec calculator-mcp-server python -m flake8 src/

# Check code formatting
docker compose exec calculator-mcp-server python -m black --check src/
```

### Development Workflow

1. **Make code changes** in the `src/` directory
2. **Rebuild and restart** the container:
   ```bash
   docker compose down && docker compose up --build -d
   ```
3. **Run tests** to verify changes:
   ```bash
   docker compose exec calculator-mcp-server bash -c "cd tests && python -m pytest -v"
   ```
4. **Test MCP server**:
   ```bash
   docker compose exec calculator-mcp-server python src/mcp_stdio_server.py
   ```

## Configuration

The server can be configured using environment variables in `docker-compose.yml`:

```yaml
environment:
  - LOG_LEVEL=INFO
```

## Project Structure

```
/
├── agents.md              # Development guidelines
├── .gitignore            # Git ignore patterns
├── .dockerignore         # Docker ignore patterns
├── CHANGELOG.md          # Project change log
├── README.md             # Project documentation
├── Makefile              # Convenient commands for setup and management
├── docker-compose.yml    # Docker Compose configuration
├── src/
│   ├── Dockerfile        # Container configuration
│   ├── requirements.txt  # Python dependencies
│   ├── mcp_stdio_server.py # Main MCP server
│   ├── calculator/       # Calculator operations
│   │   ├── __init__.py
│   │   ├── operations.py # Arithmetic operations
│   │   └── validator.py  # Input validation
│   └── utils/           # Utility functions
│       ├── __init__.py
│       └── logger.py    # Logging configuration
└── tests/
    ├── pytest.ini       # Pytest configuration
    └── test_calculator.py # Calculator tests
```

## Troubleshooting

### Common Issues

1. **Container won't start**:
   ```bash
   # Check logs
   docker compose logs calculator-mcp-server
   
   # Rebuild from scratch
   docker compose down
   docker system prune -f
   docker compose up --build -d
   ```

2. **Container not starting**:
   ```bash
   # Check container logs
   docker compose logs calculator-mcp-server
   
   # Rebuild container
   docker compose down && docker compose up --build -d
   ```

3. **MCP connection fails in Claude Desktop**:
   - Verify the Docker container is running: `docker compose ps`
   - Check that the config file path is correct in the MCP configuration
   - Ensure you're using `src/mcp_stdio_server.py` (not `src/main.py`) in the configuration
   - Check Claude Desktop logs for MCP connection errors
   - **If you see "spawn http ENOENT" error**: The HTTP configuration is incorrect. Use the Docker command configuration instead.
   - **If you see "address already in use" error**: The HTTP server is conflicting. Use the stdio MCP server instead.
   - **If Docker command fails**: Try the direct Python configuration as a fallback
   - Restart Claude Desktop after making config changes

4. **Tests failing**:
   ```bash
   # Check test logs
   docker compose exec calculator-mcp-server bash -c "cd tests && python -m pytest -v -s"
   ```

### Container Status

The container runs continuously and can be monitored:

```bash
# Check container status
docker compose ps

# View container logs
docker compose logs calculator-mcp-server
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make changes and test in Docker:
   ```bash
   docker compose down && docker compose up --build -d
   docker compose exec calculator-mcp-server bash -c "cd tests && python -m pytest -v"
   ```
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

