"""
Logging configuration for the Calculator MCP Server.
"""

import logging
import os
from typing import Optional


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    
    Args:
        name: The name of the logger
        level: The logging level (defaults to LOG_LEVEL environment variable or INFO)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set log level
    log_level = level or os.getenv("LOG_LEVEL", "INFO")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create console handler if none exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(getattr(logging, log_level.upper()))
        
        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger


# Create default logger
logger = setup_logger("calculator-mcp-server")

