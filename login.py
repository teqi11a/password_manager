import interface

class Authorization:

    __user_auth = False

    __menu = {
        1: "Зарегистрироваться",
        2: "Войти",
        3: "Сменить пароль",
        4: "Выйти"
    }

    @classmethod
    def login_menu(cls) -> bool:
        while True:
            if cls.__user_auth:
                break
            else:
                interface.UserInterface.borders()
                for key, value in cls.__menu.items():
                    print(f"{key} --> {value}")
                interface.UserInterface.borders()
                cls.__user_input = input("")
                match cls.__user_input:
                    case 1:
                        print()
                    case 2:
                        pass
                    case 3:
                        print()
                    case 4:
                        print("До свидания!")
                        exit()
        return cls.__user_auth