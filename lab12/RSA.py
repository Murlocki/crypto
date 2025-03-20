import math

from Crypto.Hash import SHA256
from sklearn.metrics import r2_score
from sympy import randprime


class RSA:
    @staticmethod
    def __extended_gcd(a1: int, m1: int) -> list[int]:
        """
        :param a1: int - большее число
        :param m1: int - меньшее число
        :return: list[int] - нод и коэффициенты для решения Диаофантового уравнения
        """

        def calc_extended_gcd(r1, r2, s1, s2, t1, t2):
            while r2 != 0:
                q = r1 // r2
                # print(f'Коэффициенты алгоритма Евклида: q:{q} r1:{r1} r2:{r2} r:{r1%r2} s1:{s1} s2:{s2} s:{s1-q*s2} t1:{t1} t2:{t2} t:{t1-q*t2}')
                r1, r2, s1, s2, t1, t2 = [r2, r1 % r2, s2, s1 - q * s2, t2, t1 - q * t2]
            return [r1, s1, t1]

        return calc_extended_gcd(a1, m1, 1, 0, 0, 1)

    def create_keys(self, p_size: int, q_size: int) -> list[list[int]]:
        """
        Создает открытый и закрытый ключи
        :param p_size:int - размер числа p в битах
        :param q_size:int - размер числа q в битах
        :return: list[list[int]] - пара из открытого и закрытого ключа
        """
        # Сгенерировали p и q
        p = randprime(2 ** p_size / 2 + 1, 2 ** p_size)
        q = randprime(2 ** q_size / 2 + 1, 2 ** q_size)

        # Сгенерировали n и значение функции эйлера от него
        n_module = p * q
        euler_n = (p - 1) * (q - 1)

        # Сгенерировали e - открытую экспоненту
        while True:
            e = randprime(2, euler_n)
            if math.gcd(euler_n, e) == 1:
                break

        # Сгенерировали d - секретную экспоненту
        d = self.__extended_gcd(euler_n, e)[2] % euler_n
        # print(p,q,n_module,euler_n,e,d,(e*d)%euler_n)

        return [[e, n_module], [d, n_module]]

    # Подпись сообщения
    def subcribe(self, message: str, secret_key: list[int]) -> [str, int]:
        """
        Вычисляет подпись сообщения
        :param message: str - сообщение для подписи
        :param secret_key: list[int] - секретный ключ
        :return: [str, int] - сообщение и его подпись
        """
        message_int = SHA256.new(message.encode('utf-8'))
        s = pow(int(message_int.hexdigest(), 16), secret_key[0], secret_key[1])
        return [message, s]

    def check_sub(self, message: str, sub: int, open_key: list[int]) -> bool:
        """
        Проверяет подпись сообщения.
        :param message: int - сообщение
        :param sub: int - подпись
        :param open_key: list[int] - открытый ключ
        :return: bool - True, если подпись верна, иначе False
        """
        message_int = int(SHA256.new(message.encode('utf-8')).hexdigest(), 16)
        decrypted = pow(sub, open_key[0], open_key[1])
        #print(decrypted,message_int)
        return message_int == decrypted

    def encrypt(self, message: str, sub: int, open_key: list[int]) -> int:
        """
        Шифрует сообщение и подпись.
        :param message: str - сообщение
        :param sub: int - подпись
        :param open_key: list[int] - открытый ключ
        :return: int - зашифрованные данные
        """
        # Объединяем сообщение и подпись в одну строку
        combined_data = f"{message}:{sub}"

        # Преобразуем строку в число
        combined_int = int.from_bytes(combined_data.encode('utf-8'), byteorder='big')
        # Шифруем с использованием открытого ключа
        encrypted_data = pow(combined_int, open_key[0], open_key[1])
        return encrypted_data

    def decrypt(self, encrypted_data: int, secret_key: list[int]) -> [str, int]:
        """
        Расшифровывает данные и разделяет их на сообщение и подпись.
        :param encrypted_data: int - зашифрованные данные
        :param secret_key: list[int] - секретный ключ
        :return: [str, int] - сообщение и подпись
        """
        # Расшифровываем с использованием закрытого ключа
        decrypted_int = pow(encrypted_data, secret_key[0], secret_key[1])

        # Преобразуем число в строку
        decrypted_data = decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, byteorder='big').decode('utf-8')

        # Разделяем строку на сообщение и подпись
        message, sub = decrypted_data.split(':')
        return [message, int(sub)]


# Пример использования
rsa = RSA()
rsa_send = RSA()
message = "HelloRoaw"

# Создание ключей
p_sub_size, q_sub_size = 256,256
p_send_size, q_send_size = p_sub_size*4,q_sub_size*4

keys = rsa.create_keys(p_sub_size, q_sub_size)
keys_send = rsa_send.create_keys(p_send_size, q_send_size)

# Создание подписи
sub = rsa.subcribe(message=message, secret_key=keys[1])
print("Сообщение и подпись:", sub)

# Шифрование сообщения и подписи
encrypted_data = rsa_send.encrypt(message=message, sub=sub[1], open_key=keys_send[0])
print("Зашифрованные данные:", encrypted_data)

# Расшифрование данных
decrypted_data = rsa_send.decrypt(encrypted_data=encrypted_data, secret_key=keys_send[1])
print("Расшифрованные данные:", decrypted_data)

# Проверка подписи
check = rsa.check_sub(message=decrypted_data[0], sub=decrypted_data[1], open_key=keys[0])
print("Проверка подписи:", check)