# Makefile for Calculator MCP Server
# Commands to prepare environment before starting Claude Desktop

.PHONY: help build start stop restart test clean logs status setup verify

# Default target
help:
	@echo "Calculator MCP Server - Available Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup     - Complete setup: build, start, and verify MCP server"
	@echo "  build     - Build the Docker container"
	@echo "  start     - Start the MCP server container"
	@echo "  stop      - Stop the MCP server container"
	@echo "  restart   - Restart the MCP server container"
	@echo ""
	@echo "Verification Commands:"
	@echo "  test      - Run all tests"
	@echo "  verify    - Verify MCP server is working correctly"
	@echo "  status    - Check container status"
	@echo "  logs      - Show container logs"
	@echo ""
	@echo "Maintenance Commands:"
	@echo "  clean     - Stop containers and remove images"
	@echo "  rebuild   - Clean and rebuild everything from scratch"
	@echo ""
	@echo "Usage:"
	@echo "  make setup    # Complete setup before starting Claude Desktop"
	@echo "  make verify   # Quick verification that everything works"

# Complete setup - run this before starting Claude Desktop
setup: build start verify
	@echo "✅ MCP Server setup complete!"
	@echo "🚀 You can now start Claude Desktop and connect to the MCP server"

# Build the Docker container
build:
	@echo "🔨 Building Docker container..."
	docker compose build
	@echo "✅ Build complete"

# Start the MCP server container
start:
	@echo "🚀 Starting MCP server container..."
	docker compose up -d
	@echo "✅ Container started"

# Stop the MCP server container
stop:
	@echo "🛑 Stopping MCP server container..."
	docker compose down
	@echo "✅ Container stopped"

# Restart the MCP server container
restart: stop start
	@echo "✅ Container restarted"

# Run all tests
test:
	@echo "🧪 Running tests..."
	docker compose exec calculator-mcp-server bash -c "cd tests && python -m pytest -v"
	@echo "✅ Tests complete"

# Run tests with coverage
test-coverage:
	@echo "🧪 Running tests with coverage..."
	docker compose exec calculator-mcp-server bash -c "cd tests && python -m pytest --cov=../src --cov-report=term-missing"
	@echo "✅ Coverage report complete"

# Verify MCP server is working correctly
verify: status
	@echo "🔍 Verifying MCP server..."
	@echo "Testing MCP server startup..."
	@docker compose exec -T calculator-mcp-server python src/mcp_stdio_server.py &
	@sleep 2
	@pkill -f "python src/mcp_stdio_server.py" || true
	@echo "✅ MCP server verification complete"

# Check container status
status:
	@echo "📊 Container status:"
	docker compose ps
	@echo ""

# Show container logs
logs:
	@echo "📋 Container logs:"
	docker compose logs calculator-mcp-server

# Clean up containers and images
clean:
	@echo "🧹 Cleaning up containers and images..."
	docker compose down --rmi all --volumes --remove-orphans
	@echo "✅ Cleanup complete"

# Rebuild everything from scratch
rebuild: clean build start verify
	@echo "✅ Complete rebuild finished"

# Quick health check
health:
	@echo "🏥 Health check:"
	@docker compose ps | grep -q "Up" && echo "✅ Container is running" || echo "❌ Container is not running"
	@docker compose exec calculator-mcp-server python -c "import sys; print('✅ Python environment OK')" 2>/dev/null || echo "❌ Python environment issue"

# Show project path for Claude Desktop configuration
path:
	@echo "📁 Project path for Claude Desktop configuration:"
	@pwd
	@echo ""
	@echo "Use this path in your Claude Desktop MCP configuration:"
	@echo "  \"args\": [\"compose\", \"-f\", \"$(shell pwd)/docker-compose.yml\", \"exec\", \"-T\", \"calculator-mcp-server\", \"python\", \"src/mcp_stdio_server.py\"]"

# Development workflow
dev: build start test
	@echo "✅ Development environment ready"

# Production-like setup
prod: build start verify
	@echo "✅ Production setup complete"
