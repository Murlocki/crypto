import math


def solve_lefts(coefs:list[list[int]]) -> int:
    def solve_linear_congruence(a, b, m):
        d = math.gcd(a, m)
        if b % d != 0:
            return []  # No solution exists

        a_prime = a // d
        b_prime = b // d
        m_prime = m // d

        try:
            inv_a = pow(a_prime, -1, m_prime)
        except ValueError:
            return []  # This should theoretically never happen since a' and m' are coprime

        x0 = (inv_a * b_prime) % m_prime
        return x0 % m
    if not math.gcd(coefs[0][2],coefs[1][2]) == math.gcd(coefs[1][2],coefs[2][2]) == 1:
        return None
    mult = coefs[0][2] * coefs[1][2] * coefs[2][2]
    new_bs = [mult//coefs[0][2],mult//coefs[1][2],mult//coefs[2][2]]
    solutions = []
    for i in range(0,len(coefs)):
        solutions.append(solve_linear_congruence(new_bs[i], coefs[i][1], coefs[i][2]))
    return sum(new_bs[i] * sol for i,sol in enumerate(solutions)) % mult
#print(solve_lefts([[1,8,6],[1,13,35],[1,4,11]]))
def solve_lin():
    def extended_gcd(a1, m1):
        def calc_extended_gcd(r1,r2,s1,s2,t1,t2):
            if r2 == 0:
                print()
                return r1, s1, t1
            else:
                q = r1//r2
                print(f'Коэффициенты алгоритма Евклида: q:{q} r1:{r1} r2:{r2} r:{r1%r2} s1:{s1} s2:{s2} s:{s1-q*s2} t1:{t1} t2:{t2} t:{t1-q*t2}')
                return calc_extended_gcd(r2,r1%r2,s2,s1-q*s2,t2,t1-q*t2)
        print()
        return calc_extended_gcd(a1,m1,1,0,0,1)
    def euler_phi(n):
        print()
        print('Рассчет Эйлеровой функции:')
        count = 0
        for i in range(1,n):
            if math.gcd(i, n) == 1:
                count += 1
            print(f'Текущее число:{i}, текущее количество взаимнопростых с {n}:{count}')
        print()
        return count

    def calc_pow_phi(n,m,power):
        st = 1
        print('Рассчет обратного элемента через функцию Эйлера')
        for i in range(power):
            st = (st * n) % m
            print(f'Текущее значение степени {power}, текущее значение {n} в степени:{st}')
        return st
    def solve_linear_congruence(a, b, m):
        # На всякий случай приводим коэффициенты к модулю
        a = a % m
        b = b % m

        # Вычисляем нод для сокращения
        d = math.gcd(a, m)
        if b % d != 0:
            print("Решение отсутствует.")
            return
        a //= d
        b //= d
        m //= d
        print(f"Количество серий решений:{d}")
        print(f"Коэффициенты сокращенные на Нод(a,m):a:{a} b:{b} m:{m}")
        # Ищем через расширенный Евклид коэффициенты для разложения qa+sm = 1
        res = extended_gcd(m,a)
        print(f"Разложение для Нод(a_new:{a},m_new:{m}):{res[2]}*{a}+{m}*{res[1]} = 1")


        phi = euler_phi(m)
        print(f"Функция Эйлера φ({m}) = {phi}")



        x0 = (b * res[2]) % m
        print()
        print(f"Образующий элемент для решений по расширенному алгоритму Евклида {b}*{res[2]} mod {m}={x0}")
        print()
        print(f"Образующий элемент для решений по формуле Эйлера ({a}^{phi-1}*{b}) mod {m}={(calc_pow_phi(a,m,phi-1)*b)%m}")
        print()

        if d == 1:
            print("Единственное решение:")
            print(f"x ≡ {x0} + {m*d}*k")
        else:
            period = m
            print(f"Период решений: {period}")
            solutions = [(x0 + k * period) % (m*d) for k in range(d)]
            print("Все решения:")
            for sol in solutions:
                print(f"x ≡ {sol} + {m*d}*k")

    a = int(input("Введите a: "))
    b = int(input("Введите b: "))
    m = int(input("Введите m: "))

    solve_linear_congruence(a, b, m)
#solve_lin()

class ModularArithmetic:
    def __init__(self, modulus):
        if modulus <= 0:
            raise ValueError("Модуль должен быть положительным целым числом")
        self.modulus = modulus

    def add(self, a, b):
        return (a + b) % self.modulus

    def multiply(self, a, b):
        return (a * b) % self.modulus

    def power(self, base, exponent):
        base = base % self.modulus  # Приводим base к допустимому диапазону
        if exponent < 0:
            phi = self.euler_totient(self.modulus)  # Функция Эйлера
            exponent = (exponent % phi + phi)  # Приводим отрицательную степень к положительной
        if math.gcd(base, self.modulus) == 1:
            exponent = exponent % self.euler_totient(self.modulus)
        result = 1
        while exponent > 0:
            result = self.multiply(base, result)
            exponent -=1
        return result

    def euler_totient(self, n):
        count = 0
        for i in range(1, n):
            if math.gcd(i, n) == 1:
                count += 1
        return count

mod_arith = ModularArithmetic(17)
print(mod_arith.power(3, -4))  # 3^4 % 17 = 81 % 17 = 13