import interface
import storage


class Authorization:

    __user_auth = False

    __menu = {
        1: "Зарегистрироваться",
        2: "Войти",
        3: "Сменить пароль",
        0: "Выйти"
    }

    @staticmethod
    def set_user_auth(user_auth: bool):
        Authorization.__user_auth = user_auth
        print(Authorization.__user_auth)

    @classmethod
    def login_menu(cls) -> bool:
        while True:
            if cls.__user_auth:
                return cls.__user_auth
            else:
                print(interface.UserInterface.borders())
                for key, value in cls.__menu.items():
                    print(f"{key} --> {value}")
                print(interface.UserInterface.borders())
                cls.__user_input = int(input(""))
                match cls.__user_input:
                    case 1:
                        cls.__user_name = input("Придумайте имя для вашей учетной записи:\n")
                        cls.__user_master_password = input("Придумайте мастер-пароль для вашей учетной записи:\n")
                        storage.create_user(cls.__user_name, cls.__user_master_password)
                    case 2:
                        cls.__user_name = input("Введите имя вашей учетной записи:\n")
                        cls.__user_master_password = input("Введите мастер-пароль вашей учетной записи:\n")
                        if storage.authenticate_user(cls.__user_name, cls.__user_master_password):
                            cls.__user_auth = True
                    case 3:
                        cls.__user_name = input("Введите имя вашей учетной записи:\n")
                        cls.__user_master_password = input("Введите старый мастер-пароль вашей учетной записи:\n")
                        if storage.check_user(cls.__user_name, cls.__user_master_password):
                            cls.__user_new_master_password = input("Придумайте новый мастер-пароль для вашей учетной записи:\n")
                            cls.__user_new_c_master_password = input("Подтвердите новый мастер-пароль для вашей учетной записи:\n")
                            if cls.__user_new_master_password == cls.__user_new_c_master_password:
                                storage.change_password(cls.__user_name, cls.__user_new_master_password)
                    case 0:
                        print("До свидания!")
                        exit()