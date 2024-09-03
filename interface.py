import generator as gen

class CodeExceptions:

    @staticmethod
    def validate_number(st: str) -> int:
        try:
            return int(st)
        except:
            raise TypeError("Введите число")

class Choices:
    __passw = ''
    __interface_borders = {
        1: "-",
        2: "@",
        3: "."
    }
    @classmethod
    def generate_passw_interface(cls):
        cls.__user_length = CodeExceptions.validate_number(input(f"{UserInterface.borders()}\nВведите длину пароля: \n{UserInterface.borders()}\n"))
        cls.__user_difficulty = CodeExceptions.validate_number(input(f"{UserInterface.borders()}\nВведите сложность пароля: \n{UserInterface.borders()}\n"))
        __passw = gen.Generator.generate(cls.__user_length, cls.__user_difficulty)
        return f"Ваш сгенерированный пароль --> {__passw}\n"

    @classmethod
    def change_borders_interface(cls):
        for key, value in cls.__interface_borders.items():
            print(f"{key} --> {value}")
        cls.__user_choice = CodeExceptions.validate_number(input())
        match cls.__user_choice:
            case 1:
                UserInterface.border = cls.__interface_borders[1]
            case 2:
                UserInterface.border = cls.__interface_borders[2]
            case 3:
                UserInterface.border = cls.__interface_borders[3]
        return f"Новый интерфейс границ теперь --> {cls.__interface_borders[cls.__user_choice]}"

class UserInterface:

    __user_choice = ""

    __interface_list = {
        1: "Сгенерировать пароль",
        2: "Показать сохраненные пароли",
        3: "Поменять границы интерфейса",
        4: "Выйти"
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
        cls.__user_choice = CodeExceptions.validate_number(input())
        match cls.__user_choice:
            case 1:
                print(Choices.generate_passw_interface())
            case 2:
                pass
            case 3:
                print(Choices.change_borders_interface())
            case 4:
                print("До свидания!")
                exit()


    @classmethod
    def borders(cls):
        return cls._interface_border * 25


while True:
    UserInterface.menu()