import binascii
import os

from lab13.AES.AES import AES
from lab13.DES import DES


class CTR:
    def __init__(self,alg = None):
        self.alg = alg if alg is not None else DES()
        self.counter_key = format(int(os.urandom(self.alg.key_length).hex(),16),f"0{self.alg.key_length*8}b")
        self.__counter_key = self.counter_key
        self.module = 1
    def encrypt(self,plain_text:str):
        byte_text = plain_text.encode('utf-8')
        byte_text = self.pad_data(byte_text)
        binary_text = ''.join(f'{byte:08b}' for byte in byte_text)
        result = ""
        self.module = 2**(len(binary_text)//(self.alg.data_len_bytes*8))
        for i in range(len(binary_text)//(self.alg.data_len_bytes*8)):
            result +=self.process_one_round(binary_text[i * self.alg.data_len_bytes * 8:(i + 1) * self.alg.data_len_bytes * 8])
        self.counter_key = self.__counter_key
        return result

    def decrypt(self,cipher_text:str):
        result = ""
        for i in range(len(cipher_text)//(self.alg.data_len_bytes*8)):
            result += self.process_one_round(cipher_text[i * self.alg.data_len_bytes * 8:(i + 1) * self.alg.data_len_bytes * 8])
        byte_data = bytes(int(result[i:i + 8], 2) for i in range(0, len(result), 8))
        result = self.unpad_data(byte_data)
        self.counter_key = self.__counter_key
        return result.decode('utf-8')
    @staticmethod
    def xor_calc(current, previous):
        return [str(int(current[i]) ^ int(previous[i])) for i in range(len(current))]

    # Метод увеличения значения ключа
    def __inc_counter_key(self):
        self.counter_key = format((int(self.counter_key, 2) + 1) % self.module,"0128b")

    def process_one_round(self, bits:str):
        encrypt_counter = self.alg.encrypt(self.counter_key)
        result = ''.join(self.xor_calc(bits, encrypt_counter))
        self.__inc_counter_key()
        return result
    # Функция добавление лишних битов на случай не соответсвия размеру блока алгоритма
    def pad_data(self,data: bytes) -> bytes:
        # Вычисляем количество байт для дополнения
        padding_length = self.alg.data_len_bytes - (len(data) % self.alg.data_len_bytes)
        # Дополняем данные байтами, значение которых равно padding_length
        padding = bytes([padding_length] * padding_length)
        return data + padding

    # Удаляем лишние биты при декодировке
    def unpad_data(self,data: bytes) -> bytes:
        padding_length = data[-1]
        if padding_length > len(data):
            raise ValueError("Некорректное дополнение: длина дополнения превышает размер данных.")
        if data[-padding_length:] != bytes([padding_length] * padding_length):
            raise ValueError("Некорректное дополнение: байты дополнения не совпадают.")
        return data[:-padding_length]

cbc = CTR(AES())
#print(hex(int(cbc.encrypt("Hello World"),2)))
print(cbc.encrypt("I hate cryptography!!!!!!!!!!Waaaaaaaaa"))
print(cbc.decrypt(cbc.encrypt("I hate cryptography!!!!!!!!!!Waaaaaaaaa")))

