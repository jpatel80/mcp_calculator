"""
Calculator operations for basic arithmetic.
"""

from typing import Union, Dict, Any
from .validator import validate_numbers, validate_division
from src.utils.logger import logger


class Calculator:
    """Calculator class for performing basic arithmetic operations."""
    
    @staticmethod
    def add(a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """
        Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Dictionary with result or error information
        """
        is_valid, error_msg = validate_numbers(a, b)
        if not is_valid:
            return {"error": error_msg}
        
        result = a + b
        logger.info(f"Addition: {a} + {b} = {result}")
        return {"result": result}
    
    @staticmethod
    def subtract(a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """
        Subtract the second number from the first.
        
        Args:
            a: First number (minuend)
            b: Second number (subtrahend)
            
        Returns:
            Dictionary with result or error information
        """
        is_valid, error_msg = validate_numbers(a, b)
        if not is_valid:
            return {"error": error_msg}
        
        result = a - b
        logger.info(f"Subtraction: {a} - {b} = {result}")
        return {"result": result}
    
    @staticmethod
    def multiply(a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """
        Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Dictionary with result or error information
        """
        is_valid, error_msg = validate_numbers(a, b)
        if not is_valid:
            return {"error": error_msg}
        
        result = a * b
        logger.info(f"Multiplication: {a} * {b} = {result}")
        return {"result": result}
    
    @staticmethod
    def divide(a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """
        Divide the first number by the second.
        
        Args:
            a: Numerator
            b: Denominator
            
        Returns:
            Dictionary with result or error information
        """
        is_valid, error_msg = validate_division(a, b)
        if not is_valid:
            return {"error": error_msg}
        
        result = a / b
        logger.info(f"Division: {a} / {b} = {result}")
        return {"result": result}


# Create a global calculator instance
calculator = Calculator()

