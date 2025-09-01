"""
Unit tests for calculator operations.
"""

import pytest
from src.calculator.operations import Calculator


class TestCalculator:
    """Test cases for Calculator class."""
    
    def test_add_positive_numbers(self):
        """Test addition with positive numbers."""
        result = Calculator.add(5, 3)
        assert result["result"] == 8
    
    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        result = Calculator.add(-5, -3)
        assert result["result"] == -8
    
    def test_add_mixed_numbers(self):
        """Test addition with mixed positive and negative numbers."""
        result = Calculator.add(5, -3)
        assert result["result"] == 2
    
    def test_subtract_positive_numbers(self):
        """Test subtraction with positive numbers."""
        result = Calculator.subtract(10, 4)
        assert result["result"] == 6
    
    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        result = Calculator.subtract(-5, -3)
        assert result["result"] == -2
    
    def test_multiply_positive_numbers(self):
        """Test multiplication with positive numbers."""
        result = Calculator.multiply(6, 7)
        assert result["result"] == 42
    
    def test_multiply_with_zero(self):
        """Test multiplication with zero."""
        result = Calculator.multiply(5, 0)
        assert result["result"] == 0
    
    def test_divide_positive_numbers(self):
        """Test division with positive numbers."""
        result = Calculator.divide(15, 3)
        assert result["result"] == 5.0
    
    def test_divide_with_float_result(self):
        """Test division that results in a float."""
        result = Calculator.divide(10, 3)
        assert result["result"] == pytest.approx(3.3333333333333335)
    
    def test_divide_by_zero(self):
        """Test division by zero error handling."""
        result = Calculator.divide(5, 0)
        assert "error" in result
        assert "Division by zero" in result["error"]
    
    def test_invalid_input_string(self):
        """Test error handling with invalid string input."""
        result = Calculator.add("5", 3)
        assert "error" in result
        assert "Both inputs must be numbers" in result["error"]
    
    def test_invalid_input_none(self):
        """Test error handling with None input."""
        result = Calculator.add(None, 3)
        assert "error" in result
        assert "Both inputs must be numbers" in result["error"]

