from helpers.validator import CodeExceptions as Validator
from interfaces import interface
from db.storage import AuthService, PasswordManager, Session
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
    def register():
        username = Validator.validate_username(input("Придумайте имя для вашей учетной записи:\n"))

        gen_master_pass = input("Хотите сгенерировать мастер-пароль? (да/нет)(yes/no)\n")
        if Validator.validate_agreement(gen_master_pass):
            master_password = Generator.generate(16, 2)
            print("Ваш мастер-пароль --> ", master_password)
        else:
            master_password = Validator.validate_password_strength(
                Validator.validate_password(input("Придумайте мастер-пароль:\n")))
            if AuthService.register(username, master_password):
                print("Регистрация прошла успешно!")

    @staticmethod
    def login():
        username = Validator.validate_username(input("Введите имя вашей учетной записи:\n"))
        master_password = Validator.validate_password(input("Введите мастер-пароль:\n"))
        if AuthService.login(username, master_password):
            Authorization.__user_auth = True
            print("Авторизация успешна!\n")
        else:
            print("Ошибка авторизации")

    @staticmethod
    def change_password():
        # Реализация смены пароля требует дополнительных методов в AuthService
        print("Функция в разработке")

    @staticmethod
    def delete_account():
        username = Validator.validate_username(input("Введите имя вашей учетной записи:\n"))
        master_password = Validator.validate_password(input("Введите мастер-пароль:\n"))
        confirmation = Validator.validate_agreement(
            input("Вы уверены, что хотите удалить учетную запись? (да/нет)\n"))

        # Требуется реализация метода delete_user в AuthService
        print("Функция в разработке")

    @classmethod
    def login_menu(cls):
        while True:
            if Session.is_authenticated():
                return True
            print("\nМеню авторизации:\n" + interface.UserInterface.borders())
            for key, value in cls.__menu.items():
                print(f"{key} --> {value}")
            print(interface.UserInterface.borders())

            choice = Validator.validate_number_input(input("Выберите опцию: "))
            match choice:
                case 1:
                    cls.register()
                case 2:
                    cls.login()
                case 3:
                    cls.change_password()
                case 4:
                    cls.delete_account()
                case 0:
                    exit("До свидания!")
                case _:
                    print("Неверный выбор")