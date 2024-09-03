class CodeExceptions:

    @staticmethod
    def validate_number(st: str) -> int:
            while True:
                if int(st):
                    return int(st)
                else:
                    st = input("Введите корректное число")

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
            if __agree.get(st):
                return True
            else:
                return False