"""
Продвинутый калькулятор с поддержкой переменных и функций.
"""

import math
from typing import Any, Dict, List, Optional, Union
from constants import (
    ERROR_MESSAGES
)

from tokenizer import Tokenizer


class Calculator:
    """
    Калькулятор с поддержкой переменных, функций и сложных выражений.
    """

    def __init__(self) -> None:
        """Инициализация калькулятора."""
        self._tokenizer = Tokenizer()
        self._variables: Dict[str, Union[int, float]] = {}
        self._tokens: List[str] = []
        self._current_position: int = 0

        # Инициализация встроенных функций
        self._functions: Dict[str, Any] = self.initialize_functions()

    def initialize_functions(self) -> Dict[str, Any]:
        """
        Инициализирует словарь встроенных функций.

        Returns:
            Словарь функций {имя: функция}
        """
        return {
            'abs': abs,
            'sqrt': math.sqrt,
            'pow': pow,
            'max': max,
            'min': min,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'log': math.log,
            'log10': math.log10,
            'exp': math.exp,
        }

    def get_current_token(self) -> Optional[str]:
        """
        Возвращает текущий токен.

        Returns:
            Текущий токен или None если достигнут конец
        """
        if self._current_position < len(self._tokens):
            return self._tokens[self._current_position]
        return None

    def consume_token(self, expected_token: Optional[str] = None) -> str:
        """
        Потребляет текущий токен и перемещается к следующему.

        Args:
            expected_token: Ожидаемый токен (если None, проверка не выполняется)

        Returns:
            Потребленный токен

        Raises:
            ValueError: Если достигнут конец или токен не соответствует ожидаемому
        """
        if self._current_position >= len(self._tokens):
            raise ValueError(ERROR_MESSAGES['unexpected_end'])

        current_token = self._tokens[self._current_position]

        if expected_token and current_token != expected_token:
            raise ValueError(
                ERROR_MESSAGES['unexpected_token'].format(
                    expected_token, current_token
                )
            )

        self._current_position += 1
        return current_token

    def parse_number(self, token: str) -> Union[int, float]:
        """
        Преобразует токен в число.

        Args:
            token: Токен для преобразования

        Returns:
            Числовое значение токена

        Raises:
            ValueError: Если токен не может быть преобразован в число
        """
        if not isinstance(token, str):
            raise ValueError(ERROR_MESSAGES['invalid_number'].format(token))

        try:
            if '.' in token:
                return float(token)
            else:
                return int(token)
        except ValueError:
            raise ValueError(ERROR_MESSAGES['invalid_number'].format(token))

    def handle_primary_expression(self) -> Union[int, float]:
        """
        Обрабатывает первичные выражения: числа, переменные, скобки, вызовы функций.
        
        Returns:
            Union[int, float]: Результат вычисления первичного выражения
            
        Raises:
            ValueError: При синтаксических ошибках в выражении
        """
        token = self.get_current_token()
        
        if token is None:
            raise ValueError("Ожидалось число, переменная, функция или скобка")
        
        if token == '(':
            self.consume_token('(')
            result = self.handle_expression()
            self.consume_token(')')
            return result
        
        # ИСПРАВЛЕНИЕ: Вызов статических методов через класс, а не через экземпляр
        elif Tokenizer.is_digit_token(token):  # Было: self._tokenizer.is_digit_token(token)
            number_token = self.consume_token()
            return self.parse_number(number_token)
        
        # ИСПРАВЛЕНИЕ: Тоже для is_identifier
        elif Tokenizer.is_identifier(token):  # Было: self._tokenizer.is_identifier(token)
            identifier = self.consume_token()
            next_token = self.get_current_token()
            
            if next_token == '(':
                return self.handle_function_call(identifier)
            else:
                return self.handle_variable_reference(identifier)
        
        else:
            raise ValueError(f"Ожидалось число, переменная или '(', но получен '{token}'")

    def handle_function_call(self, function_name: str) -> Union[int, float]:
        """
        Обрабатывает вызов функции.

        Args:
            function_name: Имя вызываемой функции

        Returns:
            Результат вызова функции

        Raises:
            ValueError: Если функция неизвестна или ошибка в аргументах
        """
        if function_name not in self._functions:
            raise ValueError(
                ERROR_MESSAGES['unknown_function'].format(function_name)
            )

        self.consume_token('(')

        arguments = []
        if self.get_current_token() != ')':
            arguments.append(self.handle_expression())

            while self.get_current_token() == ',':
                self.consume_token(',')
                arguments.append(self.handle_expression())

        self.consume_token(')')

        try:
            return self._functions[function_name](*arguments)
        except Exception as error:
            raise ValueError(f"Ошибка вызова функции {function_name}: {str(error)}")

    def handle_variable_reference(self, variable_name: str) -> Union[int, float]:
        """
        Обрабатывает ссылку на переменную.

        Args:
            variable_name: Имя переменной

        Returns:
            Значение переменной

        Raises:
            ValueError: Если переменная не объявлена
        """
        if variable_name not in self._variables:
            raise ValueError(
                ERROR_MESSAGES['unknown_variable'].format(variable_name)
            )
        return self._variables[variable_name]

    def handle_unary_expression(self) -> Union[int, float]:
        """
        Обрабатывает унарные выражения (+ и -).

        Returns:
            Результат унарного выражения
        """
        token = self.get_current_token()

        if token in ('+', '-'):
            self.consume_token()
            operand = self.handle_unary_expression()

            if token == '+':
                return operand
            else:
                return -operand
        else:
            return self.handle_primary_expression()

    def handle_power_expression(self) -> Union[int, float]:
        """
        Обрабатывает возведение в степень (**).

        Returns:
            Результат выражения со степенями
        """
        left_operand = self.handle_unary_expression()

        token = self.get_current_token()
        if token == '**':
            self.consume_token('**')
            right_operand = self.handle_power_expression()
            return left_operand ** right_operand

        return left_operand

    def handle_multiplicative_expression(self) -> Union[int, float]:
        """
        Обрабатывает мультипликативные выражения (*, /, //, %).

        Returns:
            Результат мультипликативного выражения

        Raises:
            ValueError: При делении на ноль
        """
        result = self.handle_power_expression()

        while True:
            token = self.get_current_token()
            if token in ('*', '/', '//', '%'):
                self.consume_token()
                right_operand = self.handle_power_expression()

                if token == '*':
                    result *= right_operand
                elif token == '/':
                    if right_operand == 0:
                        raise ValueError(ERROR_MESSAGES['division_by_zero'])
                    result /= right_operand
                elif token == '//':
                    if right_operand == 0:
                        raise ValueError(ERROR_MESSAGES['integer_division_by_zero'])
                    if isinstance(result, int) and isinstance(right_operand, int):
                        result //= right_operand
                    else:
                        raise ValueError("Операция // допустима только для целых чисел")
                elif token == '%':
                    if right_operand == 0:
                        raise ValueError(ERROR_MESSAGES['modulo_by_zero'])
                    if isinstance(result, int) and isinstance(right_operand, int):
                        result %= right_operand
                    else:
                        raise ValueError("Операция % допустима только для целых чисел")
            else:
                break

        return result

    def handle_additive_expression(self) -> Union[int, float]:
        """
        Обрабатывает аддитивные выражения (+, -).

        Returns:
            Результат аддитивного выражения
        """
        result = self.handle_multiplicative_expression()

        while True:
            token = self.get_current_token()
            if token in ('+', '-'):
                self.consume_token()
                right_operand = self.handle_multiplicative_expression()

                if token == '+':
                    result += right_operand
                else:
                    result -= right_operand
            else:
                break

        return result

    def handle_assignment(self) -> Union[int, float]:
        """
        Обрабатывает присваивание переменных (let x = выражение).

        Returns:
            Значение присваивания

        Raises:
            ValueError: При ошибках в синтаксисе присваивания
        """
        token = self.get_current_token()

        if token == 'let':
            self.consume_token('let')

            variable_name = self.get_current_token()
            if not self._tokenizer.is_identifier(variable_name):
                raise ValueError(
                    ERROR_MESSAGES['invalid_identifier'].format(variable_name)
                )

            self.consume_token()
            self.consume_token('=')

            value = self.handle_expression()
            self._variables[variable_name] = value
            return value

        else:
            return self.handle_additive_expression()

    def handle_expression(self) -> Union[int, float]:
        """
        Обрабатывает полное выражение.

        Returns:
            Результат вычисления выражения
        """
        return self.handle_assignment()

    def calculate(self, expression: str) -> Union[int, float]:
        """
        Вычисляет математическое выражение.

        Args:
            expression: Математическое выражение для вычисления

        Returns:
            Результат вычисления

        Raises:
            ValueError: Если выражение содержит ошибки
        """
        if not isinstance(expression, str):
            raise ValueError(ERROR_MESSAGES['invalid_expression'])

        if not expression.strip():
            raise ValueError(ERROR_MESSAGES['empty_expression'])

        # Токенизация выражения
        self._tokens = self._tokenizer.tokenize(expression)
        self._current_position = 0

        # Рекурсивный разбор
        result = self.handle_expression()

        # Проверка, что все токены обработаны
        if self._current_position != len(self._tokens):
            raise ValueError(ERROR_MESSAGES['unprocessed_tokens'])

        return result

    def get_variables(self) -> Dict[str, Union[int, float]]:
        """
        Возвращает словарь всех объявленных переменных.

        Returns:
            Копия словаря переменных
        """
        return self._variables.copy()

    def get_available_functions(self) -> List[str]:
        """
        Возвращает список доступных функций.

        Returns:
            Список имен функций
        """
        return list(self._functions.keys())

    def clear_variables(self) -> None:
        """Очищает все объявленные переменные."""
        self._variables.clear()

    def get_variable_value(self, variable_name: str) -> Optional[Union[int, float]]:
        """
        Возвращает значение переменной.

        Args:
            variable_name: Имя переменной

        Returns:
            Значение переменной или None если переменная не существует
        """
        return self._variables.get(variable_name)