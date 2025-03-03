from db.storage import PasswordManager, Session
from core.generator import PasswordGenerator
from helpers.validator import InputValidation as Validator
from translation import Language
from i18n import t

class Choices:
    _min_length = 8
    _max_length = 32
    __interface_borders = {1: "-", 2: "@", 3: "."}
    __passw_interface = {
        1: t("MainInterface.ShowPasswordsOptions.OnePass"),
        2: t("MainInterface.ShowPasswordsOptions.AllPass")
    }

    @classmethod
    def generate_passw_interface(cls):

        length = Validator.validate_number_input(
            input(t("MainInterface.GeneratePassword.InputPasswordLength")),
            # min_val=8,
            # max_val=64
        )

        complexity = Validator.validate_number_input(
            input(t("MainInterface.GeneratePassword.InputPasswordComplexity")),
            # min_val=1,
            # max_val=3
        )

        try:
            password = PasswordGenerator.generate(length, complexity)
            print(t("MainInterface.GeneratePassword.GeneratedPassword"), password)

            if Validator.validate_agreement(input(t("MainInterface.GeneratePassword.SavePasswordAgreement"))):
                service = Validator.validate_service(input(t("MainInterface.GeneratePassword.ServiceInput")))
                PasswordManager.save_password(service, password)

        except ValueError as e:
            print(t("MainInterface.GeneratePassword.GenerationFailed"), str(e))

        return ""

    @staticmethod
    def save_pass_interface():
        service = Validator.validate_service(input(t("MainInterface.SavePassword.ServiceInput")))
        password = input(t("MainInterface.SavePassword.EnterPassword"))
        PasswordManager.save_password(service, password)
        print(t("MainInterface.SavePassword.PasswordSaveSuccess"))

    @classmethod
    def show_passw_interface(cls):
        print('')
        for key, value in cls.__passw_interface.items():
            print(f"{key}: {value}")
        print('')
        _user_choice: int = Validator.validate_number_input(input(t("ChooseOption")))
        match _user_choice:
            case 1:
                print("")
                _user_service = Validator.validate_service(input(t("MainInterface.ShowPasswordInterface.ServiceName")))
                data = PasswordManager.get_password(_user_service)
                for service_name, password in data:
                    print(t("MainInterface.ShowPasswordInterface.ServiceOutput"), service_name, t("MainInterface.ShowPasswordInterface.PasswordOutput"), password, sep='')
            case 2:
                pass_confirm = Validator.validate_password(input(t("MainInterface.ShowPasswordInterface.ConfirmAction")))
                if PasswordManager.check_password(pass_confirm):
                    data = PasswordManager.get_all_passwords()
                    if not data:
                        print(t("MainInterface.ShowPasswordInterface.NoPasswordsFound"))
                        return ""
                    print(t("MainInterface.ShowPasswordInterface.SavedPasswords"))
                    for record in data:
                        pwd_id, service, password = record
                        print(t("MainInterface.ShowPasswordInterface.ShowID"), pwd_id, '] ', t("MainInterface.ShowPasswordInterface.ServiceOutput"), service,
                              t("MainInterface.ShowPasswordInterface.PasswordOutput"), password, sep='')
                    print()
                    return ""
                else:
                    print("MainInterface.ShowPasswordInterface.WrongMasterPassword")
            case _:
                print("MainInterface.ShowPasswordInterface.WrongOption")

class UserInterface:
    __interface_list = {
        1: t("MainInterface.MenuInterface.InterfaceOptions.GeneratePassword"),
        2: t("MainInterface.MenuInterface.InterfaceOptions.ShowPasswords"),
        3: t("MainInterface.MenuInterface.InterfaceOptions.SavePassword"),
        4: t("MainInterface.MenuInterface.InterfaceOptions.ChangeDesign"),
        0: t("MainInterface.MenuInterface.InterfaceOptions.Logout")
    }

    _interface_border = '*'

    @classmethod
    def menu(cls):
        print(cls.borders())
        for k, v in cls.__interface_list.items():
            print(f"{k} --> {v}")
        print(cls.borders())

        choice = Validator.validate_number_input(input(t("ChooseOption")))

        match choice:
            case 1:
                Choices.generate_passw_interface()
            case 2:
                Choices.show_passw_interface()
            case 3:
                Choices.save_pass_interface()
            case 4:
                print(t("MainInterface.MenuInterface.FunctionInDevelopment"))
            case 0:
                Session.clear()
                return "MainInterface.MenuInterface.UserLogout"
            case _:
                print(t("MainInterface.MenuInterface.WrongOption"))

        return ""

    @classmethod
    def borders(cls):
        return cls._interface_border * 50