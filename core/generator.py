import secrets
from string import ascii_uppercase, ascii_lowercase, digits
from i18n import t
from translation import Language

class PasswordGenerator:

    COMPLEXITY_LEVELS = {
        1: {
            'name': 'Basic',
            'chars': (ascii_uppercase, ascii_lowercase, digits)
        },
        2: {
            'name': 'Advanced',
            'chars': (ascii_uppercase, ascii_lowercase, digits, '!@#$%^&*')
        },
        3: {
            'name': 'Strong',
            'chars': (ascii_uppercase, ascii_lowercase, digits, '!@#$%^&*()_+-=[]{}')
        }
    }

    MIN_LENGTH = 8
    MAX_LENGTH = 64

    def __init__(self, length: int, complexity: int):
        self.length = self._validate_length(length)
        self.complexity = self._validate_complexity(complexity)

    @classmethod
    def generate(cls, length: int, complexity: int) -> str:
        instance = cls(length, complexity)
        return instance._generate_password()

    def _generate_password(self) -> str:
        """Генерация пароля с гарантированным наличием символов из каждой группы"""
        char_groups = self.COMPLEXITY_LEVELS[self.complexity]['chars']
        password = []

        # Гарантируем минимум по одному символу из каждой группы
        for group in char_groups:
            password.append(secrets.choice(group))

        # Заполняем оставшуюся длину
        all_chars = ''.join(char_groups)
        password += [
            secrets.choice(all_chars)
            for _ in range(self.length - len(password))
        ]

        # Перемешиваем результат
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)

    def _validate_length(self, length: int) -> int:
        if not (self.MIN_LENGTH <= length <= self.MAX_LENGTH):
            raise ValueError(t("Generator.ValidateLength"), self.MIN_LENGTH, "<= password <=", self.MAX_LENGTH)
        return length

    def _validate_complexity(self, complexity: int) -> int:
        if complexity not in self.COMPLEXITY_LEVELS:
            raise ValueError(t("Generator.ValidateComplexity"), list(self.COMPLEXITY_LEVELS.keys()))
        return complexity