from helpers.validator import CodeExceptions as Validator
from interfaces import interface
from db import storage
from helpers.generator import Generator


class Authorization:

    __user_auth = False

    __menu = {
        1: "Зарегистрироваться",
        2: "Войти",
        3: "Сменить пароль",
        4: "Удалить учетную запись",
        0: "Выйти"
    }

    @staticmethod
    def set_user_auth(user_auth: bool):
        Authorization.__user_auth = user_auth
        print(Authorization.__user_auth)

    @staticmethod
    def register():
        __user_name = Validator.validate_username(input("Придумайте имя для вашей учетной записи:\n"))
        gen_master_pass = input("Хотите сгенерировать мастер-пароль? (да/нет)(yes/no)\n")
        if Validator.validate_agreement(gen_master_pass):
            __user_master_password = Generator.generate(16, 2)
            print("Ваш мастер-пароль --> ", __user_master_password)
        else:
            __user_master_password = Validator.validate_password_strength(
                Validator.validate_password(input("Придумайте мастер-пароль для вашей учетной записи:\n")))
        storage.create_user(__user_name, __user_master_password)


    @staticmethod
    def login():
        __user_name = Validator.validate_username(input("Введите имя вашей учетной записи:\n"))
        __user_master_password = Validator.validate_password(input("Введите мастер-пароль вашей учетной записи:\n"))
        if storage.authenticate_user(__user_name, __user_master_password):
            Authorization.__user_auth = True

    @staticmethod
    def change_password():
        __user_name = Validator.validate_username(input("Введите имя вашей учетной записи:\n"))
        __user_master_password = Validator.validate_password(
            input("Введите старый мастер-пароль вашей учетной записи:\n"))
        if storage.check_user(__user_name, __user_master_password):
            __user_new_master_password = Validator.validate_password_strength(
                Validator.validate_password(input("Придумайте новый мастер-пароль для вашей учетной записи:\n")))
            __user_new_c_master_password = Validator.validate_password(
                input("Подтвердите новый мастер-пароль для вашей учетной записи:\n"))
            if __user_new_master_password == __user_new_c_master_password:
                storage.change_password(__user_name, __user_new_master_password)

    @staticmethod
    def logout():
        __user_name = Validator.validate_username(input("Введите имя вашей учетной записи:\n"))
        __user_master_password = Validator.validate_password(
            input("Введите мастер-пароль вашей учетной записи: \n"))
        __user_sure = Validator.validate_agreement(
            input(
                "Вы уверены, что хотите удалить учетную запись? (да/нет)(yes/no)\n(Удалятся также все сохраненные пароли)\n"))
        if storage.check_user(__user_name, __user_master_password) and __user_sure:
            storage.delete_user(__user_name, __user_master_password)
            __user_auth = False
        else:
            print("Вы ввели неправильный мастер-пароль. Попробуйте ещё раз.")

    @classmethod
    def login_menu(cls):
        while True:
            if cls.__user_auth:
                return cls.__user_auth
            else:
                print("\nВыберите опцию из списка: \n")
                print(interface.UserInterface.borders())
                for key, value in cls.__menu.items():
                    print(f"{key} --> {value}")
                print(interface.UserInterface.borders())
                cls.__user_input = Validator.validate_number_input(input())
                match cls.__user_input:
                    case 1:
                        cls.register()
                    case 2:
                        cls.login()
                    case 3:
                        cls.change_password()
                    case 4:
                        cls.logout()
                    case 0:
                        print("До свидания!")
                        exit()