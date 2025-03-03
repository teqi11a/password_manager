from helpers.validator import InputValidation as Validator
from interfaces import interface
from db.storage import AuthService, Session
from core.generator import PasswordGenerator
from translation import Language
from i18n import t

class Authorization:
    __user_auth = False

    @staticmethod
    def register():
        username = Validator.validate_username(input(t("LoginInterface.Register.RegisterUsername")))
        gen_master_pass = input(t("LoginIn.Register.RegisterPassword"))
        if Validator.validate_agreement(gen_master_pass):
            master_password = PasswordGenerator.generate(16, 2)
            print(t("LoginInterface.Register.YourMasterPassword"), master_password)
        else:
            master_password = Validator.validate_password(
                Validator.validate_password(input(t("LoginInterface.Register.CreateMasterPassword"))))
            if AuthService.register(username, master_password):
                print(t("LoginInterface.Register.SuccessfulRegister"))

    @staticmethod
    def login():
        username = Validator.validate_username(input(t("LoginInterface.Login.EnterName")))
        master_password = Validator.validate_password(input(t("LoginInterface.Login.EnterMasterPassword")))
        if AuthService.login(username, master_password):
            Authorization.__user_auth = True
            print(t("LoginInterface.Login.SuccessfulAuthorization"))
        else:
            print(t("LoginInterface.Login.FailedAuthorization"))

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
    def get_menu(cls):
        """Возвращает меню с актуальными переводами"""
        return {
            1: t("LoginInterface.LoginMenuOptions.Register"),
            2: t("LoginInterface.LoginMenuOptions.Login"),
            3: t("LoginInterface.LoginMenuOptions.ChangePassword"),
            4: t("LoginInterface.LoginMenuOptions.DeleteAccount"),
            5: t("LoginInterface.LoginMenuOptions.ChangeLanguage"),
            0: t("LoginInterface.LoginMenuOptions.Exit")
        }

    @staticmethod
    def change_language():
        print(t("LoginInterface.ChangeLanguage.ChangeOption"))
        user_lang = Validator.validate_number_input(input(""))
        match user_lang:
            case 1:
                Language.setup_i18n(lang="ru")
            case 2:
                Language.setup_i18n(lang="en")
            case _:
                print(t("LoginInterface.ChangeLanguage.IncorrectLanguage"))
        Language.reload_translations()

    @classmethod
    def login_menu(cls):
        while True:
            if Session.is_authenticated():
                return True
            menu = cls.get_menu()
            print(t("LoginInterface.LoginMenu.AuthorizationMenu"))
            print(interface.UserInterface.borders())
            for key, value in menu.items():
                print(f"{key} --> {value}")
            print(interface.UserInterface.borders())

            choice = Validator.validate_number_input(input(t("ChooseOption")))
            match choice:
                case 1:
                    cls.register()
                case 2:
                    cls.login()
                case 3:
                    cls.change_password()
                case 4:
                    cls.delete_account()
                case 5:
                    cls.change_language()
                case 0:
                    exit(t("LoginInterface.LoginMenu.Exit"))
                case _:
                    print(t("LoginInterface.LoginMenu.WrongOption"))