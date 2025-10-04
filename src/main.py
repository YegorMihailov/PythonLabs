"""
Главный модуль для запуска калькулятора.
"""

from src.calculator import Calculator

def main() -> None:
    """Главная функция для интерактивного режима калькулятора."""
    calculator = Calculator()

    while True:
        try:
            user_input = input(">>> ").strip()

            if user_input.lower() in ('exit'):
                print("Выход из программы")
                break

            if not user_input:
                continue

            elif user_input == 'vars':
                variables = calculator.get_variables()
                if variables:
                    print("Переменные:")
                    for name, value in variables.items():
                        print(f"  {name} = {value}")
                else:
                    print("Переменные не объявлены")
                continue

            elif user_input == 'funcs':
                functions = calculator.get_available_functions()
                print("Доступные функции:", ', '.join(sorted(functions)))
                continue

            elif user_input == 'clear':
                calculator.clear_variables()
                print("Все переменные очищены")
                continue

            # Вычисление выражения
            result = calculator.calculate(user_input)
            print(f"Результат: {result}")

        except ValueError as error:
            print(f"Ошибка: {error}")
        except KeyboardInterrupt:
            print("\nВыход из программы")
            break
        except Exception as error:
            print(f"Неизвестная ошибка: {error}")


if __name__ == "__main__":
    main()