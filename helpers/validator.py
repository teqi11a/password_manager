from time import sleep


class CodeExceptions:


    @staticmethod
    def validate_number_input(st: str) -> int:
            while True:
                try:
                    return int(st)
                except ValueError:
                    st = input("Попробуйте ещё раз: ")


    @staticmethod
    def validate_agreement(st: str) -> bool:
        __agree = {
            "да": True,
            "д": True,
            "yes": True,
            "y": True,
            "нет": False,
            "н": False,
            "no": False,
            "n": False
        }
        while True:
            if __agree.get(st.lower().strip()):
                return True
            else:
                return False


    @staticmethod
    def validate_password_strength(st: str) -> str:
        if len(st) >= 8 and any(char.isdigit() for char in st) and any(char.isupper() for char in st) and any(char.islower() for char in st):
            print("Ваш пароль средней сложности.")
            sleep(2)
            print("Регистрация прошла успешно!")
            return st
        elif (len(st) >= 12 and len(set(char.isupper() for char in st)) >= 2 and
              len(set(char.islower() for char in st)) >= 2 and any(char.isdigit() for char in st)
              and any(char.isupper() for char in st)
              and any(char for char in st if char in "!@#$%^&*_-+=?")):
            print("Ваш пароль высокой сложности.")
            sleep(2)
            print("Регистрация прошла успешно!")
            return st
        else:
            print("Ваш пароль слишком слабый. Попробуйте ещё раз.")
            st = input("Пароль должен содержать от 8 до 20 символов. Попробуйте ещё раз: ")
            CodeExceptions.validate_password_strength(st)

    @staticmethod
    def validate_password(st: str) -> str:
        while True:
            if 8 <= len(st) <= 20:
                return st
            else:
                st = input("Пароль должен содержать от 8 до 20 символов. Попробуйте ещё раз: ")

    @staticmethod
    def validate_username(st: str) -> str:
        while True:
            if 0 < len(st) < 20 and st.isalpha():
                return st
            else:
                st = input("Имя может содержать только буквы. Попробуйте ещё раз: ")


    @staticmethod
    def validate_service(st: str) -> str:
        while True:
            if 0 < len(st) < 25 and st.isalpha():
                return st
            else:
                st = input("Сервис может содержать только буквы и пробелы. Попробуйте ещё раз: ")