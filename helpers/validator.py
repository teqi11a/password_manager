import re
from time import sleep
from translation import Language
from i18n import t

class InputValidation:

    @staticmethod
    def validate_number_input(st: str) -> int:
            while True:
                try:
                    return int(st)
                except ValueError:
                    st = input(t("Validator.TryAgain"))


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
            print(t("Validator.ValidatePasswordStrength.MediumComplexity"))
            sleep(2)
            print(t("Validator.ValidatePasswordStrength.SuccessfulRegistration"))
            return st
        elif (len(st) >= 12 and len(set(char.isupper() for char in st)) >= 2 and
              len(set(char.islower() for char in st)) >= 2 and any(char.isdigit() for char in st)
              and any(char.isupper() for char in st)
              and any(char for char in st if char in "!@#$%^&*_-+=?")):
            print(t("Validator.ValidatePasswordStrength.HighComplexity"))
            sleep(2)
            print(t("Validator.ValidatePasswordStrength.SuccessfulRegistration"))
            return st
        else:
            print(t("Validator.ValidatePasswordStrength.WeakPassword"))
            st = input(t("Validator.ValidatePasswordStrength.PasswordCondition"))
            InputValidation.validate_password_strength(st)

    @staticmethod
    def validate_password(st: str) -> str:
        while True:
            if 8 <= len(st) <= 20:
                return st
            else:
                st = input(t("Validator.ValidatePasswordStrength.PasswordCondition"))

    @staticmethod
    def validate_username(st: str) -> str:
        while True:
            if 0 < len(st) < 20 and st.isalpha():
                return st
            else:
                st = input(t("Validator.ValidateUsername"))


    @staticmethod
    def validate_service(st: str) -> str | None:
        pattern = r'[a-zA-Z-._]'
        while True:
            if re.compile(pattern):
                return st
            else:
                st = input(t("Validator.ValidateService"))