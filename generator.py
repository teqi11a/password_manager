from random import choice


class Structures:

    _set_alphabet_upper = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                     'N', 'O', 'P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

    _set_alphabet_lower = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')

    _set_numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)

    _dict_difficulty = {
        'min': 1,
        'middle': 2,
        'max': 3
    }

    _dict_difficulty_ref = {
        1: ('.', ',', '?', '!'),
        2: ('/', '_', '-', '+', '='),
        3: ('@', '#', '$', '%', '^', '&', '*', '(', ')', '~', '`')
    }

    _min_length = 6
    _max_length = 18


class Generator(Structures):

    default_difficulty = Structures._dict_difficulty['min']
    default_length = 8

    def __init__(self, length, difficulty):
        self.__length = length
        self.__difficulty = difficulty

    @classmethod
    def generate(cls, length: int, diff: int) -> str:
        temp_set = set()
        temp_gen_str = ""
        match diff:
            case 1:
                temp_set = Structures._dict_difficulty_ref[1]
            case 2:
                temp_set = Structures._dict_difficulty_ref[1] + Structures._dict_difficulty_ref[2]
            case 3:
                temp_set = Structures._dict_difficulty_ref[1] + Structures._dict_difficulty_ref[2] + Structures._dict_difficulty_ref[3]
        for i in range(length // 2):
            temp_gen_str += str(choice(temp_set))
            temp_gen_str += str(choice(Structures._set_alphabet_lower + Structures._set_alphabet_upper + Structures._set_numbers))
        return temp_gen_str if length % 2 == 0 else temp_gen_str + choice(Structures._set_alphabet_lower + Structures._set_alphabet_upper + Structures._set_numbers)

    def validate_gen_str(self, gen_str: str) -> bool:
        if len(gen_str) < self._min_length or len(gen_str) > self._max_length:
            return False
        return True