import math

def millerTest(number:int):
    k = 0
    n = number - 1
    while n%2==0:
        k = k+1
        n = n//2
    pred = 2**n%number
    if pred == 1 or pred == number-1:
        return True

    for i in range(1,k):
        current = pred**2
        if current%number == 1 and pred!=1:
            return False
        elif current%number == number-1:
            return True
        pred = current
    return False
def squareTest(number:int):
    for i in range(1,number):
        if i**2%number == 1 and i!=1 and i!=number-1:
            print(i)
            return False
    return True

def factorizeFerm(number:int):
    x = math.ceil(math.sqrt(number))
    print(x)
    while x<=(number+1)/2:
        y = math.sqrt(x**2 - number)
        print(x**2,y**2)
        if math.floor(y) == y:
            return x+y,x-y
        x = x+1
    return [1,number]
def factorizeRho(number:int):
    x = 5
    y = 26
    print(math.gcd(abs(x-y),number))
    k = math.gcd(abs(x - y), number)
    while math.gcd(abs(x-y),number) == 1:
        x = (x**2+1)%number
        y = (y**2+1)%number
        y = (y**2+1)%number
        print(x,y,math.gcd(abs(x-y),number))
        k = math.gcd(abs(x-y),number)
    return k,number/k
def factorizeP1(number:int):
    B = 2
    while True:
        a = 2
        e = 2
        while e<=B:
            a = a**e%number
            e = e+1
        p = math.gcd(a-1,number)
        if 1<p<number:
            print(a,e)
            return p
        B +=1
print(factorizeP1(35))
def findVich(number:int):
    degree:int = (number-1)//2
    for x in range(0,number):
        print(x,x**degree%number)
#findVich(19)
#print(vactorizeRho(1219))