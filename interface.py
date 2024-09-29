import generator as gen
import login
from storage import save_passw, logout
from validator import CodeExceptions as Validator

class Choices:

    _min_length = 8
    _max_length = 32
    __passw = ''
    __interface_borders = {
        1: "-",
        2: "@",
        3: "."
    }
    @classmethod
    def generate_passw_interface(cls):
        cls.__user_length = Validator.validate_number_input(input(f"{UserInterface.borders()}\nВведите длину пароля: "
                                                                  f"({cls._min_length} - {cls._max_length})\n{UserInterface.borders()}\n"))

        if cls.__user_length < cls._min_length or cls.__user_length > cls._max_length:
            print("Вы ввели неверную длину пароля\n")
            return UserInterface.menu()

        cls.__user_difficulty = int(input(f"{UserInterface.borders()}\nВведите сложность пароля: (1 - 3)\n{UserInterface.borders()}\n"))
        if cls.__user_difficulty < 1 or cls.__user_difficulty > 3:
            print("Вы ввели неверную опцию сложности пароля\n")
            return UserInterface.menu()

        __passw = gen.Generator.generate(cls.__user_length, cls.__user_difficulty)
        __save_generated_pass = Validator.validate_agreement(input("Сохранить пароль? (да/нет)(yes/no)\n"))
        if __save_generated_pass:
            __service = Validator.validate_service(input("Введите название сервиса: "))
            save_passw( __service,__passw)
        return f"Ваш сгенерированный пароль --> {__passw}\n"

    @classmethod
    def change_borders_interface(cls):
        for key, value in cls.__interface_borders.items():
            print(f"{key} --> {value}")
        cls.__user_choice = Validator.validate_number_input(input())
        match cls.__user_choice:
            case 1:
                UserInterface.border = cls.__interface_borders[cls.__user_choice]
            case 2:
                UserInterface.border = cls.__interface_borders[cls.__user_choice]
            case 3:
                UserInterface.border = cls.__interface_borders[cls.__user_choice]
        return f"Вы выбрали --> {cls.__interface_borders[cls.__user_choice]}"


class UserInterface:

    __user_choice = ""

    __interface_list = {
        1: "Сгенерировать пароль",
        2: "Показать сохраненные пароли",
        3: "Поменять границы интерфейса",
        4: "Сохранить пароль",
        0: "Выйти из учетной записи"
    }

    _interface_border = '*'

    @property
    def border(self):
        return self._interface_border

    @border.setter
    def border(self, border):
        self._interface_border = border

    @classmethod
    def menu(cls):
        print(cls.borders())
        print("Выберите опцию из списка: ")
        for key, value in cls.__interface_list.items():
            print(f"{key} --> {value}")
        print(f"{cls.borders()}")
        cls.__user_choice = Validator.validate_number_input(input())

        match cls.__user_choice:
            case 1:
                print(Choices.generate_passw_interface())
            case 2:
                pass
            case 3:
                print(Choices.change_borders_interface())
            case 4:
                save_passw(Validator.validate_service(input("Введите название сервиса: \n")),
                           (Validator.validate_password(input("Введите пароль: \n"))))
            case 0:
                print("До свидания!")
                login.Authorization.set_user_auth(logout())
                return "exit_to_login"
        return ""
    @classmethod
    def borders(cls):
        return cls().border * 50
