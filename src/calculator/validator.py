"""
Input validation for calculator operations.
"""

from typing import Union, Tuple
from src.utils.logger import logger


def validate_numbers(a: Union[int, float], b: Union[int, float]) -> Tuple[bool, str]:
    """
    Validate that the input numbers are valid for arithmetic operations.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if inputs are numbers
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return False, "Both inputs must be numbers"
    
    # Check for NaN or infinity
    if not (a == a and b == b):  # NaN check
        return False, "Inputs cannot be NaN"
    
    if abs(a) == float('inf') or abs(b) == float('inf'):
        return False, "Inputs cannot be infinite"
    
    logger.debug(f"Validated inputs: a={a}, b={b}")
    return True, ""


def validate_division(a: Union[int, float], b: Union[int, float]) -> Tuple[bool, str]:
    """
    Validate inputs specifically for division operation.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # First validate as numbers
    is_valid, error_msg = validate_numbers(a, b)
    if not is_valid:
        return False, error_msg
    
    # Check for division by zero
    if b == 0:
        return False, "Division by zero is not allowed"
    
    logger.debug(f"Validated division inputs: a={a}, b={b}")
    return True, ""

