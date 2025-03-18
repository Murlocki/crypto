import copy
import os
from copy import deepcopy

from lab13.AES.KEY128 import KEY128
from lab13.AES.KEY192 import KEY192
from lab13.AES.KEY256 import KEY256
from lab3 import PolynomialSolver


class AES:
    r_con = [
        0x00000000, 0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000,
        0x80000000, 0x1B000000, 0x36000000,
        # 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        # 0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        # 0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    ]

    s_box = [
        [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
        [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
        [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
        [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
        [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
        [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
        [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
        [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
        [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
        [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
        [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
        [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
        [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
        [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
        [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
        [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16],
    ]

    inv_s_box = [
        [0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB],
        [0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB],
        [0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E],
        [0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25],
        [0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92],
        [0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84],
        [0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06],
        [0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B],
        [0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73],
        [0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E],
        [0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B],
        [0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4],
        [0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F],
        [0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF],
        [0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61],
        [0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D],
    ]

    # MixColumns
    c_box = [
        ["x", "x+1", "1", "1"],
        ["1", "x", "x+1", "1"],
        ["1", "1", "x", "x+1"],
        ["x+1", "1", "1", "x"],
    ]
    c_box_inv = [
        ["x^3+x^2+x", "x^3+x+1", "x^3+x^2+1", "x^3+1"],
        ["x^3+1", "x^3+x^2+x", "x^3+x+1", "x^3+x^2+1"],
        ["x^3+x^2+1", "x^3+1", "x^3+x^2+x", "x^3+x+1"],
        ["x^3+x+1", "x^3+x^2+1", "x^3+1", "x^3+x^2+x"],
    ]
    pol_solver = PolynomialSolver(module="x^8+x^4+x^3+x+1")

    def __init__(self,
                 key: str = "10100111000000111010010100001111010110000100110100001011101111101001000001100000011110010001100110110100111110111101101100100111"):
        if len(key) == 128:
            self.key_object = KEY128(key)
        elif len(key) == 192:
            self.key_object = KEY192(key)
        elif len(key) == 256:
            self.key_object = KEY256(key)
        else:
            raise ValueError("DES init key length is not 128 or 192 or 256 bytes")
        self.round_keys: list[str] = []
        self.__create_round_keys()

    # Создание ключа для каждого раунда
    def __create_round_keys(self):
        words: list[str] = [""] * (self.key_object.round_count + 1) * self.key_object.word_in_key_count
        for i in range(len(self.key_object.key) // 32):
            words[i] = self.key_object.key[i * 32:(i + 1) * 32]
        for i in range(len(self.key_object.key) // 32, len(words)):
            words[i] = self.sub_bytes(words[i-1])
            words[i] = self.key_object.calculateWordI(i, words, self.__calcTemp)
        self.round_keys = [''.join(words[i * 4:(i + 1) * 4]) for i in range(0, 11)]

    # Высчитываем локальное значение
    def __calcTemp(self, wPrev: str, i):
        w_prew_shift = self.__shift(wPrev, -8)
        w_sub = self.sub_bytes(w_prew_shift)
        return self.__xor_calc(w_sub, format(AES.r_con[i // 4], "032b"))

    def sub_bytes(self, s: str) -> str:
        result = ""
        for i in range(4):
            current_byte = s[i * 8:8 * (i + 1)]
            row: int = int(current_byte[0:4], 2)
            col: int = int(current_byte[4:], 2)
            result += format(AES.s_box[row][col], "08b")
        return result

    def sub_bytes_inv(self, s: str) -> str:
        result = ""
        for i in range(4):
            current_byte = s[i * 8:8 * (i + 1)]
            row: int = int(current_byte[0:4], 2)
            col: int = int(current_byte[4:], 2)
            result += format(AES.inv_s_box[row][col], "08b")
        return result

    # Сдвиг ключа
    @staticmethod
    def __shift(key: str, steps: int) -> str:
        vals = key
        result = list(vals)
        for i, val in enumerate(vals):
            result[(i + steps) % len(vals)] = val
        return ''.join(result)

    # Сдвиг строки матрицы
    @staticmethod
    def __shift_row(value: list[str], steps: int) -> list[str]:
        result = [""] * len(value)
        for i in range(len(result)):
            result[i] = value[(i + steps) % len(value)]
        return result

    # MixColumns для 1 столбца
    def __mix_columns_column(self, column: list[str], box: list[list[str]]) -> list[str]:
        result = []
        for row in box:
            new_row = "00000000"
            for i, col in enumerate(row):
                column_polynom = AES.pol_solver.vectorToStr(list(map(int, column[i])))
                prod_polynom = AES.pol_solver.multPolynomial(column_polynom, col)
                new_column_value = format(int(''.join(list(map(str, AES.pol_solver.parsePolynomial(prod_polynom)))), 2),
                                          "08b")
                new_row = self.__xor_calc(new_column_value, new_row)
            result.append(new_row)
        return result

    # Применение MixColumns
    def mix_columns(self, matrix: list[list[str]], box: list[list[str]]) -> list[list[str]]:
        result_matrix = copy.deepcopy(matrix)
        for i in range(len(matrix)):
            column = [matrix[j][i] for j in range(len(matrix))]
            new_column = self.__mix_columns_column(column, box)
            for j in range(len(new_column)):
                result_matrix[j][i] = new_column[j]
        return result_matrix

    # Применение добавления ключа
    def add_round_key(self, matrix: list[list[str]], round_number: int):
        result_matrix = copy.deepcopy(matrix)
        for i in range(len(matrix)):
            column = ''.join([matrix[j][i] for j in range(len(matrix))])
            key_part = self.round_keys[round_number][i * 32:(i + 1) * 32]
            new_column = self.__xor_calc(column, key_part)
            for j in range(len(matrix)):
                result_matrix[j][i] = new_column[j * 8:(j + 1) * 8]
        return result_matrix

    # Функция применения подстановки
    @staticmethod
    def __use_perm(init_string: str, permutation1: list[int]) -> str:
        return ''.join(init_string[bit - 1] for bit in permutation1)

    # Функция xor по строкам
    @staticmethod
    def __xor_calc(first: str, second: str) -> str:
        return "".join([str(int(first[i]) ^ int(second[i])) for i in range(len(first))])

    # Функция прогонки одного раунда
    def __process_one_round(self, input_matrix: list[list[str]], round_number: int) -> list[list[str]]:
        sub_bytes_matrix: list[list[str]] = copy.deepcopy(input_matrix)
        # сделали sub_bytes по матрице
        for i, row in enumerate(input_matrix):
            new_row = self.sub_bytes(''.join(row))
            sub_bytes_matrix[i] = [new_row[i * 8:(i + 1) * 8] for i in range(4)]
        # сделали shift_rows по строкам матрицы
        shift_rows_matrix: list[list[str]] = copy.deepcopy(sub_bytes_matrix)
        for i, row in enumerate(input_matrix):
            shift_rows_matrix[i] = self.__shift_row(sub_bytes_matrix[i], i)

        if round_number != self.key_object.round_count:
            mix_columns_matrix: list[list[str]] = self.mix_columns(shift_rows_matrix, AES.c_box)
        else:
            mix_columns_matrix: list[list[str]] = deepcopy(shift_rows_matrix)
        added_keys_matrix: list[list[str]] = self.add_round_key(mix_columns_matrix, round_number)
        return added_keys_matrix

    # Функция прогонки одного раунда назад
    def __process_one_round_back(self, input_matrix: list[list[str]], round_number: int) -> list[list[str]]:
        sub_bytes_matrix: list[list[str]] = copy.deepcopy(input_matrix)
        # сделали sub_bytes по матрице
        for i, row in enumerate(input_matrix):
            new_row = self.sub_bytes_inv(''.join(row))
            sub_bytes_matrix[i] = [new_row[i * 8:(i + 1) * 8] for i in range(4)]

        shift_rows_matrix: list[list[str]] = copy.deepcopy(sub_bytes_matrix)
        for i, row in enumerate(input_matrix):
            shift_rows_matrix[i] = self.__shift_row(sub_bytes_matrix[i], -i)
        # сделали shift_rows по строкам матрицы
        if round_number != 0:
            mix_columns_matrix: list[list[str]] = self.mix_columns(shift_rows_matrix, AES.c_box_inv)
        else:
            mix_columns_matrix: list[list[str]] = copy.deepcopy(shift_rows_matrix)

        if round_number == 0:
            added_keys_matrix: list[list[str]] = self.add_round_key(mix_columns_matrix, round_number)
        else:
            added_keys_matrix: list[list[str]] = self.inv_add_key(mix_columns_matrix, round_number)
        return added_keys_matrix

    def inv_add_key(self, matrix: list[list[str]], round_number: int):
        result_matrix = copy.deepcopy(matrix)
        for i in range(len(matrix)):
            column = ''.join([matrix[j][i] for j in range(len(matrix))])
            key_part = self.round_keys[round_number][i * 32:(i + 1) * 32]
            key_inv = self.__mix_columns_column([key_part[i * 8:(i + 1) * 8] for i in range(4)], AES.c_box_inv)
            new_column = self.__xor_calc(column, ''.join(key_inv))
            for j in range(len(matrix)):
                result_matrix[j][i] = new_column[j * 8:(j + 1) * 8]
        return result_matrix

    # Функция перевода строки в матрицу
    @staticmethod
    def __str_to_matrix(plain_text: str) -> list[list[str]]:
        result = [[""] * 4 for i in range(4)]
        for i in range(16):
            result[i % 4][i // 4] = plain_text[i * 8:(i + 1) * 8]
        return result

    # Матрица в строку
    @staticmethod
    def __matrix_to_str(matrix: list[list[str]]) -> str:
        result = ""
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                result += matrix[j][i]
        return result

    @staticmethod
    def __print_matrix_16(matrix: list[list[str]]):
        result = deepcopy(matrix)
        for i in range(4):
            for j in range(4):
                result[i][j] = hex(int(matrix[i][j], 2))

    def encrypt(self, plain_text: str) -> str:
        matrix = self.__str_to_matrix(plain_text)
        self.__print_matrix_16(matrix)

        matrix = self.add_round_key(matrix, 0)
        self.__print_matrix_16(matrix)
        for i in range(1, self.key_object.round_count + 1):
            matrix = self.__process_one_round(matrix, i)
            self.__print_matrix_16(matrix)
        return self.__matrix_to_str(matrix)

    def decrypt(self, ciphertext: str) -> str:
        matrix = self.__str_to_matrix(ciphertext)
        self.__print_matrix_16(matrix)
        matrix = self.add_round_key(matrix, self.key_object.round_count)
        self.__print_matrix_16(matrix)
        for i in range(self.key_object.round_count - 1, -1, -1):
            matrix = self.__process_one_round_back(matrix, i)
            self.__print_matrix_16(matrix)
        return self.__matrix_to_str(matrix)


# d = AES(format(int(os.urandom(16).hex(), 16), "0128b"))
# print(len(d.key))
d = AES(format(int("0x2475A2B33475568831E2120013AA5487", 16), "0128b"))

# byte_text = "HelloWorldPlease".encode('utf-8')
# print(byte_text)
# binary_text = ''.join(f'{byte:08b}' for byte in byte_text)
byte_text = "0x00041214120412000C00131108231919"
binary_text = ''.join([format(int(s, 16), "04b") for s in byte_text[2:]])
print(binary_text)
result = d.encrypt(binary_text)
print("result:", hex(int(result, 2)))

binary_decrypt = d.decrypt(result)
byte_data = bytes(int(binary_decrypt[i:i + 8], 2) for i in range(0, len(binary_decrypt), 8))
# print("result decrypt:", byte_data.decode('utf-8'))
print("result decrypt:", hex(int(binary_decrypt, 2))[2:].zfill(32))
# print(binary_text)
# print(binary_decrypt)
