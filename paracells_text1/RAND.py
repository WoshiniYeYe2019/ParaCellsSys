import random
import math

x = list([0] * 97)
c = 0

RANDMAX = 23371.0
RANDPI = 3.1415926


def rand():
    for i in range(97):
        f = random.randint(0, 32767)
        x[i] = (1.0 * math.fmod(f, RANDMAX)) / RANDMAX
    global c
    c = (1.0 * math.fmod(random.random(), RANDMAX)) / RANDMAX


def NormalDistribution_():
    f1 = Value_()
    f2 = Value_()
    X = math.sqrt(-2 * math.log(f1)) * math.cos(2 * RANDPI * f2)
    return X


def NormalDistribution(mu, sigma):
    X = NormalDistribution_()
    X = sigma * X + mu
    return X


def BinomialDistribution(n, p):
    r = Value_()
    if p > 1.0 - 1e-6:
        k = n
    else:
        a0 = pow(1 - p, n)
        Sum = a0
        if Sum > r:
            k = 0
        else:
            for k in range(1, n + 1):
                a1 = a0 * (1.0 * (n - k + 1.0) / (1.0 * k)) * (p / (1 - p))
                Sum = Sum + a1
                if Sum > r:
                    break
                else:
                    a0 = a1

    return k


def BetaDistribution(a, b):
    X = GammaDistribution(a, 1)
    y = GammaDistribution(b, 1)

    return X / (X + y)


def Value_():
    r = 0
    s = 64
    global c
    global x
    rand()
    d = 7654321.0 / 16777216.0
    d0 = 1677213.0 / 1677216.0
    if x[r] >= x[s]:
        x0 = x[r] - x[s]
    else:
        x0 = x[r] - x[s] + 1
    if c >= d:
        c = c - d
    else:
        c = c - d + d0
    if x0 >= c:
        U = x0 - c
    else:
        U = x0 - c + d0
    for i in range(96):
        x[i] = x[i + 1]
    x[96] = math.fmod(x0, 1)
    c = math.fmod(c, 1)
    f = math.fmod(U, 1)
    return f


def Value(a, b):
    return a + (b - a) * Value_()


def operator_():
    return Value_()


def operator(a, b):
    return Value(a, b)


def GammaDistribution(a, b):
    E = 2.71828
    n = math.floor(a)
    delta = a - n
    xi = 0

    if delta > 1e-6:
        for k in range(1, 101):
            U = Value_()
            V = Value_()
            W = Value_()
            if U <= E / (E + delta):
                xi = pow(V, 1 / delta)
                eta = W * pow(xi, delta - 1)
            else:
                xi = 1 - math.log(V)
                eta = W * pow(E, -xi)
            if eta < pow(xi, delta - 1) * pow(E, -xi):
                break

    for k in range(1, n + 1):
        xi = xi - math.log(Value_())

    return b * xi


def WienerGen():
    f1 = Value_()
    f2 = Value_()
    X = math.sqrt(-2 * math.log(f1)) * math.cos(2 * RANDPI * f2)
    return X


rand()
