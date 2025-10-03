"""
Unit-тесты для класса Calculator с использованием unittest.
"""

import unittest
import math
import sys
import os
from typing import Any

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import Calculator


class TestCalculatorBasic(unittest.TestCase):
    """
    Базовые тесты для Calculator.
    """
    
    def setUp(self) -> None:
        """
        Подготовка перед каждым тестом.
        """
        self.calculator = Calculator()
    
    def test_calculate_basic_arithmetic(self) -> None:
        """
        Тестирует базовые арифметические операции.
        """
        test_cases = [
            ("2 + 3", 5),
            ("10 - 4", 6),
            ("3 * 4", 12),
            ("15 / 3", 5.0),
            ("2 + 3 * 4", 14),
            ("(2 + 3) * 4", 20),
        ]
        
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result: Any = self.calculator.calculate(expression)
                self.assertEqual(result, expected)
    
    def test_calculate_power_operations(self) -> None:
        """
        Тестирует операции возведения в степень.
        """
        test_cases = [
            ("2 ** 3", 8),
            ("3 ** 2", 9),
            ("(2 ** 3) ** 2", 64),
        ]
        
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result: Any = self.calculator.calculate(expression)
                self.assertEqual(result, expected)
    
    def test_division_by_zero_raises_error(self) -> None:
        """
        Тестирует обработку деления на ноль.
        """
        with self.assertRaises(ValueError, msg="Деление на ноль"):
            self.calculator.calculate("5 / 0")


class TestCalculatorVariables(unittest.TestCase):
    """
    Тесты работы с переменными.
    """
    
    def setUp(self) -> None:
        """
        Подготовка перед каждым тестом.
        """
        self.calculator = Calculator()
    
    def test_unknown_variable_raises_error(self) -> None:
        """
        Тестирует обработку неизвестной переменной.
        """
        with self.assertRaises(ValueError, msg="Неизвестная переменная"):
            self.calculator.calculate("unknown_var + 5")


class TestCalculatorFunctions(unittest.TestCase):
    """
    Тесты функций калькулятора.
    """
    
    def setUp(self) -> None:
        """
        Подготовка перед каждым тестом.
        """
        self.calculator = Calculator()
    
    def test_basic_functions(self) -> None:
        """
        Тестирует базовые математические функции.
        """
        test_cases = [
            ("abs(-5)", 5),
            ("sqrt(16)", 4),
            ("pow(2, 3)", 8),
            ("max(1, 5, 3)", 5),
            ("min(1, 5, 3)", 1),
        ]
        
        for expression, expected in test_cases:
            with self.subTest(expression=expression):
                result: Any = self.calculator.calculate(expression)
                self.assertEqual(result, expected)
    
    def test_unknown_function_raises_error(self) -> None:
        """
        Тестирует обработку неизвестной функции.
        """
        with self.assertRaises(ValueError, msg="Неизвестная функция"):
            self.calculator.calculate("unknown_func(5)")


if __name__ == '__main__':
    unittest.main()