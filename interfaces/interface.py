from helpers import generator as gen
from db.storage import PasswordManager, Session
from helpers.validator import CodeExceptions as Validator


class Choices:
    _min_length = 8
    _max_length = 32
    __interface_borders = {1: "-", 2: "@", 3: "."}
    __passw_interface = {
        1: "Показать пароль",
        2: "Показать все пароли"
    }

    @classmethod
    def generate_passw_interface(cls):
        length = Validator.validate_number_input(
            input("Введите длину пароля (8-32): "))

        if not cls._min_length <= length <= cls._max_length:
            print("Недопустимая длина")
            return ""

        difficulty = Validator.validate_number_input(
            input("Выберите сложность (1-3): "))

        password = gen.Generator.generate(length, difficulty)
        print(f"Сгенерированный пароль: {password}")

        if Validator.validate_agreement(input("Сохранить? (да/нет): ")):
            service = Validator.validate_service(input("Название сервиса: "))
            PasswordManager.save_password(service, password)

        return ""

    @classmethod
    def show_passw_interface(cls):
        print('')
        for key, value in cls.__passw_interface.items():
            print(f"{key}: {value}")
        print('')
        _user_choice: int = Validator.validate_number_input(input('Выберите опцию: '))
        match _user_choice:
            case 1:
                print("")
                _user_service = Validator.validate_service(input('Название сервиса: '))
                service, password = PasswordManager.get_password(_user_service)
                print(f"Сервис: {service} -> Пароль: {password}")
            case 2:
                data = PasswordManager.get_all_passwords()
                if not data:
                    print("Нет сохраненных паролей")
                    return ""
                print("\nСохраненные пароли:\n")
                for record in data:
                    pwd_id, service, password = record
                    print(f"[ID: {pwd_id}] Сервис: {service} -> Пароль: {password}")
                print()
                return ""
            case _:
                print("Неверный выбор")

class UserInterface:
    __interface_list = {
        1: "Сгенерировать пароль",
        2: "Показать пароли",
        3: "Изменить оформление",
        0: "Выйти"
    }

    _interface_border = '*'

    @classmethod
    def menu(cls):
        print(cls.borders())
        for k, v in cls.__interface_list.items():
            print(f"{k} --> {v}")
        print(cls.borders())

        choice = Validator.validate_number_input(input("Выберите опцию: "))

        match choice:
            case 1:
                Choices.generate_passw_interface()
            case 2:
                Choices.show_passw_interface()
            case 3:
                print("Функция в разработке")
            case 0:
                Session.clear()
                return "exit"
            case _:
                print("Неверный выбор")

        return ""

    @classmethod
    def borders(cls):
        return cls._interface_border * 50