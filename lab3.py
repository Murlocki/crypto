import math
from typing import List


class PolynomialSolver:
    def __init__(self, gf:int = 2, module:str = None):
        self.gf = gf
        if module is None:
            self.module = 1
        else:
            self.module = self.__parsePolynomial(module)
        #print(self.module)
        self.prim = {
            1: [[1,0],[1, 1]],
            2: [[1, 1, 1]],
            3: [[1, 0, 1, 1], [1, 1, 0, 1]],
            4: [[1, 0, 0, 1, 1], [1, 1, 1, 1, 1], [1, 1, 0, 0, 1]],
            5: [[1, 0, 0, 1, 0, 1], [1, 0, 1, 0, 0, 1], [1, 0, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1], [1, 1, 1, 0, 1, 1],
                  [1, 1, 1, 1, 0, 1]],
            6: [[1, 0, 0, 0, 0, 1, 1], [1, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 1, 1, 1], [1, 0, 1, 1, 0, 1, 1],
                  [1, 1, 0, 0, 0, 0, 1]]
        }
    def __parsePolynomial(self,polynomialStr:str):
        polynomialStr = polynomialStr + '+'
        elems = []
        currentElem = ''
        for s in polynomialStr:
            if s == '-':
                elems.append(currentElem)
                currentElem ='-'
            elif s == '+':
                elems.append(currentElem)
                currentElem =''
            else:
                currentElem += s
        coefs = []
        degrees = []
        for elem in elems:
            comp = elem.split('x')
            if len(comp) == 2:
                coef = int(comp[0]) if comp[0] else 1
                degree = int(comp[1][1:]) if comp[1] else 1
            else:
                coef = int(comp[0])
                degree = 0
            coefs.append(coef)
            degrees.append(degree)
        result = [0] * (degrees[0]+1)
        for i,degree in enumerate(degrees):
            result[degree] = coefs[i] % self.gf
        result.reverse()
        return result

    def __sumPols(self,polynomialFirstVector,polynomialSecondVector):
        if len(polynomialFirstVector) > len(polynomialSecondVector):
            result = polynomialFirstVector.copy()
        else:
            result = polynomialSecondVector.copy()
        for i in range(-1,-min(len(polynomialFirstVector),len(polynomialSecondVector))-1,-1):
            result[i] = (polynomialFirstVector[i] + polynomialSecondVector[i]) % self.gf
            #print(i,result[i],polynomialFirstVector[i],polynomialSecondVector[i],result)
        i = 0
        while i<len(result) and result[i] == 0:
            i = i+1
        return result[i:]

    def __delPols(self,polynomialVector,polynomialDelVector):
        if len(polynomialVector) < len(polynomialDelVector):
            return polynomialVector
        result = polynomialVector.copy()
        while True:
            antiDelVector= [(self.gf - elem) % self.gf for elem in polynomialDelVector]
            i = 0
            while i < len(result) and result[i] == 0:
                i = i + 1
            deliter = antiDelVector+[0]*(len(result)-i-len(antiDelVector))
            #print(result,deliter,i,polynomialDelVector)
            result = self.__sumPols(result,deliter)
            if not self.__greaterVector(result,polynomialDelVector):
                break
        i = 0
        while i < len(result) and result[i] == 0:
            i = i + 1
        if i == len(result):
            return [0]
        else:
            return result[i:]

    def __multPols(self,polynomialVector1,polynomialVector2):
        if len(polynomialVector1) < len(polynomialVector2):
            second,first = polynomialVector1,polynomialVector2
        else:
            first,second = polynomialVector1,polynomialVector2
        result = []
        for i in range(len(first)):
            result = self.__sumPols(result+[0],first[i]*second)
            #print(i,first[i],result)
        return result
    def __greaterVector(self,vector1,vector2):
        if len(vector1) == len(vector2):
            return True
        elif len(vector1) < len(vector2):
            return False
        return True
    def __vectorToStr(self,vector):
        result = ''
        if vector[0] == 0: return [0]
        for i in range(len(vector)):
            if vector[i] > 0:
                result += str(vector[i]) if i == len(vector)-1 or vector[i] > 1 and i < len(vector)-1 else ''
                if i < len(vector)-1:
                    result += 'x'
                if i<len(vector)-2:
                    result +='^'+str(len(vector)-i-1)
                result += '+'
        return result[:-1]

    def addPolynomial(self,polynomialFirst:str,polynomialSecond:str):
        firstVector = self.__parsePolynomial(polynomialFirst)
        secondVector = self.__parsePolynomial(polynomialSecond)
        #print(firstVector,secondVector)
        polSum = self.__sumPols(firstVector,secondVector)
        #print(polSum)
        result = self.__delPols(polSum,self.module)
        #print(result)
        return self.__vectorToStr(result)

    def multPolynomial(self, polynomialFirst: str, polynomialSecond: str):
        firstVector = self.__parsePolynomial(polynomialFirst)
        secondVector = self.__parsePolynomial(polynomialSecond)
        #print(firstVector, secondVector)
        polMult = self.__multPols(firstVector, secondVector)
        #print(polMult)
        result = self.__delPols(polMult, self.module)
        #print(result)
        return self.__vectorToStr(result)

    def numberToBase(self,n):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % self.gf))
            n //= self.gf
        return digits[::-1]
    def createNotPrivPolList(self,degree:int):
        for i in range(max(self.prim.keys())+1,degree//2+1):
            start = 2**(i)
            for j in range(start,2**(i+1)):
                currentPol = self.numberToBase(j)
                #print(currentPol)
                prim = True
                for k in range(1,i//2+1):
                    for pol in self.prim[k]:
                        if self.__delPols(currentPol,pol) == [0]:
                            prim = False
                            break
                    if not prim:
                        break
                if prim:
                    polList = self.prim.get(i,[])
                    polList.append(currentPol)
                    self.prim[i] = polList
        # for k in self.prim.keys():
        #     print(k,self.prim[k])
    def __checkIfPrime(self,polVector:List[int])->bool:
        vectorDegree = len(polVector) - 1
        self.createNotPrivPolList(vectorDegree)
        prim = True
        if polVector in self.prim.get(vectorDegree,[]):
            return True
        for k in range(1, vectorDegree // 2 + 1):
            for pol in self.prim[k]:
                if self.__delPols(polVector, pol) == [0]:
                    prim = False
                    break
            if not prim:
                break
        return prim
    def provePrivPolynomial(self,pol:str)->bool:
        polVector = self.__parsePolynomial(pol)
        return self.__checkIfPrime(polVector)

    def checkPrimalPolynomail(self,pol:str)->bool:
        polVector = self.__parsePolynomial(pol)
        if not self.__checkIfPrime(polVector):
            return False

        primSolver = PolynomialSolver(self.gf,pol)
        polDegree = len(polVector) - 1
        sq = [1,0]
        currentElemOfGF = sq.copy()
        i = 1
        alreadyWas = []
        while i <= 2**polDegree-1:
            currentElemOfGF = primSolver.__multPols(sq,currentElemOfGF)
            currentElemOfGF = primSolver.__delPols(currentElemOfGF, primSolver.module)
            i = i + 1
            print(primSolver.__vectorToStr(currentElemOfGF),end=', ')
            if currentElemOfGF == [1] or currentElemOfGF in alreadyWas:
                break
            alreadyWas.append(currentElemOfGF)
        if i == 2**polDegree-1:
            return True
        return False
    def createCicleClasses(self):
        seen = set()
        cicleClasses = {}
        for i in range(2**(len(self.module) - 1) - 1):
            currentDegree = i
            if currentDegree in seen:
                continue
            currentCycle = set()
            while currentDegree not in currentCycle:
                currentCycle.add(currentDegree)
                seen.add(currentDegree)
                currentDegree = (currentDegree * 2) % (2**(len(self.module) - 1)-1)
            cicleClasses[i] = currentCycle
        return cicleClasses
    def createGalueElems(self):
        result = {0:"1"}
        currentPol = "1"
        for i in range(1,2**(len(self.module) - 1) - 1):
            currentPol = self.multPolynomial(currentPol, "x")
            result[i] = (currentPol)
        return result
    def solveEquasion(self,equasion:List[str]):
        gals = ["0"]
        gals.extend(list(self.createGalueElems().values()))
        for i,gal in enumerate(gals):
            for j in range(i+1,len(gals)):
                print(gal,gals[j])
                if self.multPolynomial(gal,gals[j]) == equasion[1] and self.addPolynomial(gal,gals[j]) == equasion[0]:
                    return [gal,gals[j]]
        return []

    def returnPolynomomsForCycle(self):
        cycles = self.createCicleClasses()
        result = {"0":"M(g)=0"}
        for cycle in cycles:
            if cycle == 0: continue
            pol = f"M{cycle}(g)="
            for element in cycles[cycle]:
                currentPol = self.multPolynomial(f"x^{element}","1")
                pol += f"(g+{currentPol})"
            result[cycle] = pol
        return result

solver = PolynomialSolver(2,'x^4+x+1')
#print(solver.addPolynomial('x^3+x','x^2+1'))
#print(solver.createNotPrivPolList(16))
#print(solver.provePrivPolynomial('x^7+x^3+x^2+x+1'))
print(solver.createGalueElems())
print(solver.solveEquasion(["x^2+x","x^3+1"]))
#print(solver.createCicleClasses())
#print(solver.returnPolynomomsForCycle().values())

# import matplotlib.pyplot as plt
#
# # Данные
# x = ["0","1","g","g^2","g^3","g^4","g^5","g^6","g^7","g^8","g^9","g^10","g^11","g^12","g^13","g^14"]
# ticks = range(0,16)
# xVals = [0, 1, 1, 4, 4, 6, 6, 7, 7, 9, 9, 11, 11, 13, 13,]
# y = [1, 7, 14, 9, 14, 4, 12, 9, 15, 10, 13, 2, 9, 0, 11,]
#
# # Создание графика
# fig, ax = plt.subplots()
#
# # Рисуем точки и линию
# ax.scatter(xVals, y, marker='o', linestyle='-', color='b', label="Данные")
#
# # Устанавливаем произвольные тики на осях
# ax.set_xticks(ticks)
# ax.set_yticks(ticks)
# ax.set_yticklabels(x)  # Произвольные тики по Y
# ax.set_xticklabels(x)  # Произвольные тики по X
#
# # Добавляем сетку и оформление
# ax.grid(True, linestyle='--', alpha=0.6)
# ax.legend()
#
# # Отображаем график
# plt.show()

i = 1
while 2*i*31+1<2**29-1:
    y = 2**29 - 1
    x = 2*31*i+1
    print(x, y)
    if y%x == 0:
        break
    i = i +1