"""
Модуль для токенизации математических выражений.
"""

import re
from typing import List
from constants import TOKEN_PATTERN


class Tokenizer:
    """
    Класс для разбиения математических выражений на токены.
    """

    def __init__(self) -> None:
        """Инициализация токенизатора."""
        self._token_pattern = TOKEN_PATTERN

    def tokenize(self, expression: str) -> List[str]:
        """
        Разбивает выражение на токены.

        Args:
            expression: Математическое выражение для токенизации

        Returns:
            Список токенов

        Raises:
            ValueError: Если выражение пустое или не является строкой
        """
        if not isinstance(expression, str):
            raise ValueError("Выражение должно быть строкой")

        expression = expression.strip()

        if not expression:
            raise ValueError("Пустое выражение")

        # Удаляем пробелы и токенизируем
        expression = expression.replace(' ', '')
        tokens = re.findall(self._token_pattern, expression)

        return tokens

    def is_digit_token(token: str) -> bool:
        """
        Проверяет, является ли токен числом.

        Args:
            token: Токен для проверки

        Returns:
            True если токен является числом, иначе False
        """
        if not isinstance(token, str):
            return False
        return token.replace('.', '').isdigit()

    def is_identifier(token: str) -> bool:
        """
        Проверяет, является ли токен идентификатором.

        Args:
            token: Токен для проверки

        Returns:
            True если токен является идентификатором, иначе False
        """
        if not isinstance(token, str):
            return False
        return bool(re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', token))