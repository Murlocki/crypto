import binascii
import os

from lab13.DES import DES


class CBC:
    def __init__(self,alg = None):
        self.alg = alg if alg is not None else DES()
        self.previous_block = format(int(os.urandom(self.alg.key_length).hex(),16),f"0{self.alg.key_length*8}b")
        self.__previous_block = self.previous_block
    def encrypt(self,plain_text:str):
        byte_text = plain_text.encode('utf-8')
        byte_text = self.pad_data(byte_text)
        binary_text = ''.join(f'{byte:08b}' for byte in byte_text)
        result = ""
        for i in range(len(binary_text)//(self.alg.data_len_bytes*8)):
            result +=self.processOneRound(binary_text[i*self.alg.data_len_bytes*8:(i+1)*self.alg.data_len_bytes*8])
        self.previous_block = self.__previous_block
        return result

    def decrypt(self,cipher_text:str):
        result = ""
        for i in range(len(cipher_text)//(self.alg.data_len_bytes*8)):
            result += self.processOneRoundDecrypt(cipher_text[i*self.alg.data_len_bytes*8:(i+1)*self.alg.data_len_bytes*8])
        byte_data = bytes(int(result[i:i + 8], 2) for i in range(0, len(result), 8))
        result = self.unpad_data(byte_data)
        self.previous_block = self.__previous_block
        return result.decode('utf-8')
    @staticmethod
    def xorCurrentPrevios(current, previous):
        return [str(int(current[i]) ^ int(previous[i])) for i in range(len(current))]

    def processOneRoundDecrypt(self, bits: str):
        new_bits = self.alg.decrypt(bits)
        result = ''.join(self.xorCurrentPrevios(new_bits, self.previous_block))
        self.previous_block = result
        return result

    def processOneRound(self,bits:str):
        new_bits = ''.join(self.xorCurrentPrevios(bits,self.previous_block))
        result = self.alg.encrypt(new_bits)
        self.previous_block = bits
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

cbc = CBC(None)
print(hex(int(cbc.encrypt("Hello World"),2)))
print(cbc.decrypt(cbc.encrypt("I hate cryptography!!!!!!!!!!Waaaaaaaaa")))