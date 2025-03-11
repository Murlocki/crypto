import math


# Функция для факторизации числа методом Ферма
def fermat_factorization(n):
    """Факторизация числа n методом Ферма."""
    a = math.isqrt(n) + 1
    b2 = a * a - n
    while not is_square(b2):
        a += 1
        b2 = a * a - n
        print(a,b2,n)
    b = math.isqrt(b2)
    return (a - b, a + b)


# Функция для проверки, является ли число полным квадратом
def is_square(m):
    """Проверка, является ли m полным квадратом."""
    k = math.floor(math.isqrt(m))
    return k * k == m


# Функция для проверки, является ли число простым
def is_prime(m):
    """Проверка, является ли m простым числом."""
    if m < 2:
        return False
    for i in range(2, math.isqrt(m) + 1):
        if m % i == 0:
            return False
    return True


# Функция для факторизации числа
def factor(n):
    """Факторизация числа n."""
    factors = {}
    if(n%2==0): factors[2]= 0
    while n%2==0:
        factors[2] += 1
        n = n//2
    def _factor(n):
        if n == 1:
            return
        if is_prime(n):
            factors[n] = factors.get(n, 0) + 1
            return
        d = fermat_factorization(n)
        _factor(d[0])
        _factor(d[1])

    _factor(n)
    return factors


# Функция для вычисления символа Лежандра
def legendre_symbol(a, p):
    """Вычисление символа Лежандра (a|p)."""
    if p < 2:
        raise ValueError("p должно быть простым числом больше 2.")
    if a % p == 0:
        return 0
    ls = pow(a, (p - 1) // 2, p)
    if ls == p - 1:
        return -1
    return ls


# Функция для проверки, является ли число квадратичным вычетом
def is_quadratic_residue(a, p):
    """Проверка, является ли a квадратичным вычетом по модулю p."""
    return legendre_symbol(a, p) == 1


# Функция для решения квадратичного сравнения по модулю p
def solve_mod_p(a, p):
    """Решение x^2 ≡ a mod p."""
    if not is_quadratic_residue(a, p):
        return []
    solutions = []
    for x in range(p):
        if (x * x) % p == a % p:
            solutions.append(x)
    return solutions


# Функция для подъема решения с использованием метода Гензеля
def hensel_lifting(a, p, k, x0):
    """Подъем решения x^2 ≡ a mod p^k с использованием метода Гензеля."""
    x = x0
    for i in range(1, k):
        f_x = x * x - a
        f_prime_x = 2 * x
        if f_prime_x % p == 0:
            if f_x % p ** (i + 1) == 0:
                x = x
            else:
                return None
        else:
            inv_f_prime = pow(f_prime_x, -1, p)
            x = (x - f_x * inv_f_prime) % p ** (i + 1)
    return x


# Функция для решения квадратичного сравнения по модулю p^k
def solve_mod_pk(a, p, k):
    """Решение x^2 ≡ a mod p^k."""
    if p == 2:
        if k == 1:
            if a % 2 == 0:
                return [0]
            else:
                return [1]
        elif k == 2:
            if a % 4 == 0:
                return [0, 2]
            elif a % 4 == 1:
                return [1, 3]
            else:
                return []
        else:
            if a % 8 != 1:
                return []
            # Для k >= 3, решение имеет 4 корня
            x0 = 1
            x = x0
            for i in range(3, k + 1):
                x = x if (x * x) % (2 ** i) == a % (2 ** i) else x + 2 ** (i - 2)
            return [x, -x % 2 ** k, x + 2 ** (k - 1), -x - 2 ** (k - 1) % 2 ** k]
    else:
        solutions_mod_p = solve_mod_p(a, p)
        if not solutions_mod_p:
            return []
        solutions = []
        for x0 in solutions_mod_p:
            x = hensel_lifting(a, p, k, x0)
            if x is not None:
                solutions.append(x)
        return solutions


# Функция для решения квадратичного сравнения по модулю n
def solve_quadratic_congruence(a, n):
    """Решение квадратичного сравнения x^2 ≡ a mod n."""
    factors = factor(n)
    congruences = []
    print(factors)
    for p, exp in factors.items():
        m = p ** exp
        if p == 2:
            if a % 8 != 1 and exp >= 3:
                return []  # Нет решений для 2^k, если a не ≡ 1 mod 8
        elif not is_quadratic_residue(a % p, p):
            return []  # Нет решений, если a не является квадратичным вычетом
        solutions = solve_mod_pk(a, p, exp)
        congruences.append((solutions, m))
        print(congruences)

    # Китайская теорема об остатках
    def crt(congruences):
        from functools import reduce
        def extended_gcd(a, b):
            if b == 0:
                return (a, 1, 0)
            else:
                g, x, y = extended_gcd(b, a % b)
                return (g, y, x - (a // b) * y)

        def chinese_remainder(a, n):
            total = 0
            prod = reduce(lambda a, b: a * b, n)
            for a_i, n_i in zip(a, n):
                p = prod // n_i
                g, x, y = extended_gcd(p, n_i)
                if g != 1:
                    return None  # Нет решения
                total += a_i * x * p
            return total % prod

        a_list = [cong[0] for cong in congruences]
        n_list = [cong[1] for cong in congruences]
        return chinese_remainder(a_list, n_list)

    # Генерация всех возможных комбинаций решений
    from itertools import product
    all_solutions = []
    for sols in product(*[cong[0] for cong in congruences]):
        x = crt(list(zip(sols, [cong[1] for cong in congruences])))
        if x is not None:
            all_solutions.append(x)

    return sorted(set(all_solutions))


# Пример использования
a = 1
n = 48
solutions = solve_quadratic_congruence(a, n)
print(f"Решения x^2 ≡ {a} mod {n}: {solutions}")