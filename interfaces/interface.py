from db.storage import PasswordManager, Session
from core.generator import PasswordGenerator
from helpers.validator import InputValidation as Validator


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
            input("Введите длину пароля (8-64): "),
            # min_val=8,
            # max_val=64
        )

        complexity = Validator.validate_number_input(
            input("Выберите сложность (1-3):\n1. Базовый\n2. Продвинутый\n3. Максимальный\n"),
            # min_val=1,
            # max_val=3
        )

        try:
            password = PasswordGenerator.generate(length, complexity)
            print(f"Сгенерированный пароль: {password}")

            if Validator.validate_agreement(input("Сохранить пароль? (да/нет): ")):
                service = Validator.validate_service(input("Введите название сервиса: "))
                PasswordManager.save_password(service, password)

        except ValueError as e:
            print(f"Ошибка генерации: {str(e)}")

        return ""

    @staticmethod
    def save_pass_interface():
        service = Validator.validate_service(input("Введите название сервиса: \n"))
        password = input('Введите пароль: \n')
        PasswordManager.save_password(service, password)
        print("Пароль успешно сохранен!")

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
                pass_confirm = Validator.validate_password(input("Подтвердите действие используя мастер-пароль:\n"))
                if PasswordManager.check_password(pass_confirm):
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
                else:
                    print("Неверный мастер-пароль!\n")
            case _:
                print("Неверный выбор")

class UserInterface:
    __interface_list = {
        1: "Сгенерировать пароль",
        2: "Показать пароли",
        3: "Сохранить пароль",
        4: "Изменить оформление",
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
                Choices.save_pass_interface()
            case 4:
                print("Функция в разработке\n")
            case 0:
                Session.clear()
                return "Вы вышли из системы\n"
            case _:
                print("Неверный выбор")

        return ""

    @classmethod
    def borders(cls):
        return cls._interface_border * 50