import time
import random
import math
import numpy as np

RANDPI = 3.1415936
RANDMAX = 23371.0  # 32767

t = time.time()
random.seed(t)

# 得到随机数组x和随机数c,均为0-1的均匀分布
x = []
for i in range(97):
    x.append(random.uniform(0, 1))
c = random.uniform(0, 1)


def Value(a: float = None, b: float = None):
    j = random.uniform(0, 1)
    if a is not None and b is not None:
        return a + (b - a) * j
    return j


def NormalDistribution(mu: float = None, sigma: float = None):
    f1 = Value()
    f2 = Value()
    _x = math.sqrt(-2 * math.log10(f1)) * math.cos(RANDPI * f2)

    if mu is not None and sigma is not None:
        _x = sigma * _x + mu

    return _x


def BinomiaDistribution(n: int, p: float):
    r = Value()
    if p > 1.0 - 1e-6:
        k = n
    else:
        a0 = (1 - p) ** n
        _sum = a0
        if _sum > r:
            k = 0
        else:
            k = 1
            while k <= n:
                a1 = a0 * (1.0 * (n - k + 1.0) / 1.0 * k) * (p / 1 - p)
                _sum += a1
                if _sum > r:
                    break
                else:
                    a0 = a1
                k += 1
    return k


def WienerGen():
    f1 = Value()
    f2 = Value()
    _x = math.sqrt(-2 * math.log10(f1)) * math.cos(RANDPI * f2)
    return _x


def GammaDistribution(a: float, b: float):
    E = 2.71828
    n = math.floor(a)
    delta = a - n
    xi = 0
    if delta > 1e-6:
        for k in range(1, 101):
            U = Value()
            V = Value()
            W = Value()
            if U <= E / (E + delta):
                xi = pow(V, 1 / delta)
                eta = W * pow(xi, delta - 1)
            else:
                xi = 1 - math.log10(V)
                eta = W * pow(E, -xi)
            if eta < pow(xi, delta) * pow(E, -xi):
                break
    for k in range(1, n+1):
        xi -= math.log10(Value())

    return b * xi


def BetaDistribution(a: float, b: float):
    _x = GammaDistribution(a, 1)
    _y = GammaDistribution(b, 1)
    return _x / (_x + _y)


def Initialized(seed: int):
    global c
    random.seed(seed)
    for j in range(len(x)):
        f = float(random.randint(0, 32767))
        x[j] = (f % RANDMAX) / RANDMAX
    c = (random.randint(0, 32767) % RANDMAX) / RANDMAX


# test
