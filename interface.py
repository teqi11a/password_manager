# from random import choice
# import generator as gen

class CodeExceptions:

    @staticmethod
    def validate_number(st: str) -> int:
        try:
            return int(st)
        except:
            raise TypeError("Введите число")

class GenerateChoice:

    # __user_length = 8
    # __user_difficulty = "min"

    @classmethod
    def generate_interface(cls):
        cls.user_length = CodeExceptions.validate_number(input(f"{UserInterface.borders()}\nВведите длину пароля: \n{UserInterface.borders()}\n"))
        cls.user_difficulty = CodeExceptions.validate_number(input(f"{UserInterface.borders()}\nВведите сложность пароля: \n{UserInterface.borders()}\n"))


class UserInterface:

    __user_choice = ""

    __interface_list = {
        1: "Сгенерировать пароль",
        2: "Показать сохраненные пароли",
        3: "Поменять границы интерфейса",
        4: "Выйти"
    }
    __interface_borders = {
        1: "-",
        2: "@",
        3: "."
    }

    __interface_border = '*'


    @classmethod
    def menu(cls):
        print(cls.borders())
        print("Выберите опцию из списка: ")
        for key, value in cls.__interface_list.items():
            print(f"{key} --> {value}")
        print(f"{cls.borders()}\n")
        cls.__user_choice = CodeExceptions.validate_number(input())
        match cls.__user_choice:
            case 1:
                print(GenerateChoice.generate_interface())


    @classmethod
    def borders(cls):
        return cls.__interface_border * 25
