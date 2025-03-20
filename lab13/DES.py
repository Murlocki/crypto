class DES:
    # Перестановка для ключа
    permutation: list[int] = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
                              41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36,
                              29, 32]
    # Удаление битов для ключа
    del_perm: list[int] = [
        57, 49, 41, 33, 25, 17, 9, 1,
        58, 50, 42, 34, 26, 18, 10, 2,
        59, 51, 43, 35, 27, 19, 11, 3,
        60, 52, 44, 36, 63, 55, 47, 39,
        31, 23, 15, 7, 62, 54, 46, 38,
        30, 22, 14, 6, 61, 53, 45, 37,
        29, 21, 13, 5, 28, 20, 12, 4
    ]
    # Перестановки на входе и выходе алгоса
    in_permutation: list[int] = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22,
                                 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27,
                                 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]

    out_permutation: list[int] = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22,
                                  62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11,
                                  51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]

    # Перестановка для расширения при вычислении раунда
    expand_permutation: list[int] = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    s_box = [
        # S-box 1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],
        # S-box 2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
        ],
        # S-box 3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
        ],
        # S-box 4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
        ],
        # S-box 5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
        ],
        # S-box 6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
        ],
        # S-box 7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
        ],
        # S-box 8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
        ]
    ]

    # Прямая перестановка для вычисления функции
    forward_permutation: list[int] = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]

    def __init__(self, key: str = "1010101010111011000010010001100000100111001101101100110011011101"):
        if len(key) != 64:
            # Обычно ключ дается размером в 64 бита, где 8,16,24,32,40,48,56,64 - проверочные биты,которые удаляются
            raise ValueError("DES init key length is not 64 bytes")
        self.key: str = key
        self.round_keys: list[str] = []
        self.__create_round_keys()
        self.data_len_bytes = 8
    @property
    def key_length(self):
        return len(self.key)
    # Создание ключа для каждого раунда
    def __create_round_keys(self):
        real_key = self.__use_perm(self.key, DES.del_perm)
        left_key = real_key[:28]
        right_key = real_key[28:]
        for i in range(16):
            step = 1 if i + 1 in [1, 2, 9, 16] else 2
            left_key = self.__shift(left_key, -step)
            right_key = self.__shift(right_key, -step)
            compress_key = self.__use_perm(left_key + right_key, DES.permutation)
            self.round_keys.append(compress_key)

    # Сдвиг ключа
    @staticmethod
    def __shift(key: str, steps: int) -> str:
        vals = key
        result = list(vals)
        for i, val in enumerate(vals):
            result[(i + steps) % len(vals)] = val
        return ''.join(result)

    # Функция применения подстановки
    @staticmethod
    def __use_perm(init_string: str, permutation1: list[int]) -> str:
        return ''.join(init_string[bit - 1] for bit in permutation1)

    # Вычисление функции от правой части
    def __calcF(self, input_string: str, key: str) -> str:
        extend_input_string = self.__use_perm(input_string, DES.expand_permutation)
        xor_string = self.__xor_calc(key, extend_input_string)
        result = ""
        for i in range(8):
            current_str = xor_string[i * 6:(i + 1) * 6]
            row = int(current_str[0] + current_str[5], 2)
            col = int(current_str[1:5], 2)
            result_bit = format(DES.s_box[i][row][col], '04b')
            result += result_bit
        return self.__use_perm(result, DES.forward_permutation)

    # Функция xor по строкам
    @staticmethod
    def __xor_calc(first: str, second: str) -> str:
        return "".join([str(int(first[i]) ^ int(second[i])) for i in range(len(first))])

    # Функция прогонки одного раунда
    def __processOneRound(self, input_string: str, round_number: int,inverse:bool = False) -> str:
        left_str = input_string[:32]
        right_str = input_string[32:]
        function_str = self.__calcF(right_str, self.round_keys[round_number if not inverse else -round_number - 1])
        xor = self.__xor_calc(left_str, function_str)
        if round_number < 15:
            return right_str + xor
        return xor + right_str


    def encrypt(self, plaintext: str):
        if len(plaintext) != 64:
            raise ValueError("plaintext length must be 64 bytes")
        result = plaintext
        result = self.__use_perm(result, DES.in_permutation)
        for i in range(16):
            result = self.__processOneRound(result, i)
        return self.__use_perm(result, DES.out_permutation)
    def decrypt(self, ciphertext: str):
        if len(ciphertext) != 64:
            raise ValueError("ciphertext length must be 64 bytes")
        result = self.__use_perm(ciphertext, DES.in_permutation)
        for i in range(16):
            result = self.__processOneRound(result, i,True)
        return self.__use_perm(result, DES.out_permutation)

d = DES(str(bin(0xAABB09182736CCDD))[2:].zfill(64))
result1 = d.encrypt(str(bin(0x123456ABCD132536))[2:].zfill(64))
#print(hex(int(result1, 2)))
result = d.decrypt(str(bin(0xc0b7a8d05f3a829c))[2:].zfill(64))
#print(hex(int(result, 2)))