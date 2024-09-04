from validator import CodeExceptions as Validator
import interface
import storage


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
                        cls.__user_name = Validator.validate_username(input("Придумайте имя для вашей учетной записи:\n"))
                        cls.__user_master_password = Validator.validate_password_strength(
                            Validator.validate_password(input("Придумайте мастер-пароль для вашей учетной записи:\n")))
                        storage.create_user(cls.__user_name, cls.__user_master_password)
                    case 2:
                        cls.__user_name = Validator.validate_username(input("Введите имя вашей учетной записи:\n"))
                        cls.__user_master_password = Validator.validate_password(input("Введите мастер-пароль вашей учетной записи:\n"))
                        if storage.authenticate_user(cls.__user_name, cls.__user_master_password):
                            cls.__user_auth = True
                    case 3:
                        cls.__user_name = Validator.validate_username(input("Введите имя вашей учетной записи:\n"))
                        cls.__user_master_password = Validator.validate_password(input("Введите старый мастер-пароль вашей учетной записи:\n"))
                        if storage.check_user(cls.__user_name, cls.__user_master_password):
                            cls.__user_new_master_password = Validator.validate_password_strength(
                                Validator.validate_password(input("Придумайте новый мастер-пароль для вашей учетной записи:\n")))
                            cls.__user_new_c_master_password = Validator.validate_password(input("Подтвердите новый мастер-пароль для вашей учетной записи:\n"))
                            if cls.__user_new_master_password == cls.__user_new_c_master_password:
                                storage.change_password(cls.__user_name, cls.__user_new_master_password)
                    case 4:
                        cls.__user_name = Validator.validate_username(input("Введите имя вашей учетной записи:\n"))
                        cls.__user_master_password = Validator.validate_password(input("Введите мастер-пароль вашей учетной записи: \n"))
                        cls.__user_sure = Validator.validate_agreement(
                            input("Вы уверены, что хотите удалить учетную запись? (да/нет)(yes/no)\n(Удалятся также все сохраненные пароли)\n"))
                        if storage.check_user(cls.__user_name, cls.__user_master_password) and cls.__user_sure:
                            storage.delete_user(cls.__user_name, cls.__user_master_password)
                            cls.__user_auth = False
                        else:
                            print("Вы ввели неправильный мастер-пароль. Попробуйте ещё раз.")
                    case 0:
                        print("До свидания!")
                        exit()