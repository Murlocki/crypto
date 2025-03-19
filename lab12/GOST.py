import math
import random
from argparse import ArgumentError

from ecdsa import ellipticcurve
from gostcrypto import gosthash
from sympy import isprime
from lab12.EllipseCurve import EllipseCurve

class GOST:
    def __init__(self, p:int=None, a:int=None, b:int=None, m:int=None, q:int = None):
        # if not isprime(p) or p<= 2**255:
        #     raise ValueError("Неверное значение p")
        # if p == m:
        #     raise ValueError("m не должно равняться p")
        # if not isprime(q) or m%q !=0 or not 2**254<q<2**256:
        #     raise ValueError("q должно быть порядком подгруппы эллиптической кривой")

        self.p = p
        self.a = a
        self.b = b
        self.m = m
        self.q = q
        self.curve = EllipseCurve(self.a,self.b,self.p,self.m)
    def generate_decryption_key(self, point:list[int], d:int=None):
        if not 0<d<self.q:
            raise ValueError("Неверный ключ шифрования")
        return self.curve.prod_point(point,d)

    def subscribe(self,message:str, point: list[int], key:int,):
        # Вычислиле число соответствующее хешу сообщения
        hash_obj_256 = gosthash.new('streebog256')
        hash_obj_256.update(bytearray(message.encode()))
        z = int(hash_obj_256.hexdigest(),16)

        # Вычислили e
        e = z%self.q
        if e == 0:
            e = 1

        while True:
            while True:
                # Сгенерировали k
                k = random.randint(0,self.q-1)
                # Вычислили новую точку кривой и rc
                c = self.curve.prod_point(point, k)
                r = c[0] % self.q
                if r!=0: break
            s = (r*key + k*e) % self.q
            if s !=0: break
        #print(f"z:{z} e:{e} s:{s} r:{r}")
        return f"{bin(r)[2:].zfill(256)}{bin(s)[2:].zfill(256)}"

    def euler_totient(self, n):
        count = 0
        for i in range(1, n):
            if math.gcd(i, n) == 1:
                count += 1
        return count

    def check_correct(self, sub:str, message:str, desc_key:list[int], point:list[int]):
        if not len(sub) == 512:
            return False
        r = int("0b"+sub[:len(sub)//2],2)
        s = int("0b"+sub[len(sub)//2:],2)
        if not (0<r<self.q and 0<s<self.q):
            raise False

        # Вычислиле число соответствующее хешу сообщения
        hash_obj_256 = gosthash.new('streebog256')
        hash_obj_256.update(bytearray(message.encode()))
        z = int(hash_obj_256.hexdigest(), 16)

        # Вычислили e
        e = z % self.q
        if e == 0:
            e = 1
        print(f"z:{z} e:{e} s:{s} r:{r}")
        # Вычислили v
        v = pow(e,self.euler_totient(q)-1,self.q)
        #Вычислили z1 и z2
        z1 = (s*v)%self.q
        z2 = (-r*v)%self.q
        # Вычислили точку эллиптической кривой
        C = self.curve.sum_points(self.curve.prod_point(point, z1),self.curve.prod_point(desc_key, z2))
        R = C[0] % self.q
        print(f"z1:{z1} z2:{z2} v:{v} {R}")
        if r == R:
            return True
        else:
            return False

# Для кривой
p = 29
a = 28
b = 1

# Для группы
# Проверял на сайта с генератором точек
m = 37
q = 37
point = [1, 1]

# Для шифроки/дешифровки
d_key = 10
message = "I hate cryptooooooooo!!!!!!!!"
curve = EllipseCurve(a,b,p,calc_order=True)
print(curve.order)
print(point)


g = GOST(p,a,b,m,q)
q_point = g.generate_decryption_key(point,d_key)
result = g.subscribe(message,point,d_key)
print(f"Подпись {hex(int(result,2))}")
print(g.check_correct(result,message,q_point,point))