from argparse import ArgumentError


class EllipseCurve:
    def __init__(self, a:int, b:int, p:int, order:int=0, calc_order:bool = False):
        """
        Создает экземпляр класса эллиптической кривой
        :param a: int - коэффициент a
        :param b: int - коэффициент b
        :param p: int - модуль p
        """
        if 4*a**3 + 27*b**2 == 0: raise ValueError("Коэффиценты a и b не должны удовлетворять 4*a**3 + 27*b**2 =0")
        self.p = p
        self.a = a % p
        self.b = b % p
        self.__order = self.__calcOrder() if calc_order else order

    @property
    def order(self):
        return self.__order
    @property
    def curve_invariant(self):
        """
        Получает инварианту кривой по формуле J(E) = 1728 * (4*a**3)/(4*a**3 + 27*b**2) mod p
        :return:int - значение инварианты
        """
        return (1728 * (4*self.a**3)/(4*self.a**3 + 27*self.b**2)) % self.p

    def __calcOrder(self):
        """
        Вычисляет порядок группы эллиптической кривой
        :return: int - порядок группы эллиптической кривой
        """
        result = 1
        for i in range(self.p):
            vic = i**3+self.a*i+self.b
            if vic**((self.p-1)//2)%self.p == 1:
                result += 2
            elif vic**((self.p-1)//2)%self.p == 0:
                result += 1
        return result

    def prod_point(self,point:list[int], k:int)-> list[int]:
        """
        Вычисляет произведение точки на константу
        :param point: list[int] - точка для умножения
        :param k: int - константа
        :return: list[int] - результат умножения
        """
        result = point
        for i in range(k-1):
            result = self.sum_points(point,result)
        return result

    def sum_points(self,point1:list[int],point2:list[int])->list[int]:
        """
        Вычисляет сумму двух точек на кривой
        :param point1: list[int] - первая точка
        :param point2: list[int] - вторая точка
        :return: list[int] - результат умножения
        """
        x1,y1 = point1
        x2,y2 = point2
        if x1 == x2:
            y1_2_inv = (2*y1)**(self.p-2)%self.p
            l = ((3*x1**2+self.a)*y1_2_inv)%self.p
            x = (l**2-2*x1)%self.p
            y = (l*(x1-x) - y1)%self.p
            return [x,y]
        else:
            x1_x2_inv = (x2-x1)**(self.p-2)%self.p
            l = ((y2-y1)*x1_x2_inv) % self.p
            x = (l**2 - x1 - x2) % self.p
            y = (l*(x1-x) - y1) % self.p
            return [x,y]