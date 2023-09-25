from CellSystem import CellSystem
from CustomFunc import *
from CustomClass import *
import random
import UpdateTools
from demo1.Rand import *
from demo1.Settings import *

# 增殖状态
Type = 'Type'
profq = 'profq'
# 年龄
age = 'age'
# 表观遗传状态
X0 = 'X0'
X1 = 'X1'

# 环境参数
time = 'time'
prolif = 'prolif'
NumPoolCell = 'NumPoolCell'
restingNum = 'restingNum'
diffNum = 'diffNum'
dieNum = 'dieNum'
divNum = 'divNum'
divNumNew = 'divNumNew'
U = 'u'


# 死亡率计算
def fdeathrate(u: float, x2: float):
    _c = 1
    f0 = 3
    f = f0 * pow(x2, u) * pow(1 - x2, 1 - u)
    mu = mu0 / (1.0 + _c * math.exp(f))
    return mu


def fbeta(n0, x1, x2):
    theta = theta0 + pow(x2, 8.5) * theta1 / (pow(0.4, 8.5) + pow(x2, 8.5))
    beta = beta0 * (1.0 / (1.0 + n0 / theta)) * ((a1 * x1 + pow(a2 * x1, 3.5)) / (1 + pow(a3 * x1, 3.5)))
    return beta


def fkappa(x1):
    kappa = kappa0 * 1.0 / (1.0 + pow(b1 * x1, 6.0))
    return kappa


# 计算继承的表观遗传状态
def GetnextEpi(j, x1, x2, u):
    c1 = 0.055
    c2 = 0.06
    a = 1.3
    b = 0.68 * u + 0.35

    if j == 1:
        phi = c2 + b * pow(alpha2 * x2, 2.1) / (1 + pow(alpha2 * x2, 2.1))
    else:
        phi = c1 + a * pow(alpha1 * x1, 1.5) / (1 + pow(alpha1 * x1, 1.5))
    a = eta * phi
    b = eta * (1 - phi)

    z = BetaDistribution(a, b)
    return z


# 环境函数
def func_env(t, flag):
    flag = int(flag)
    if flag == 0:
        u = 0.1
    else:
        if t < 10:
            u = 0.1
        if 10 <= t < 15:
            if flag == 1:
                u = 0.016 * t - 1.5
            elif flag == 2:
                u = -0.00032 * pow(t, 2) + (0.016 - 0.00032 * 250) * t - 1.5 + 0.00032 * 15000
            elif flag == 3:
                u = -0.06 * t / (-160 + t)
            elif flag == 4:
                u = 0.8 / (1 + math.exp((125 - t) / 5)) + 0.125
            elif flag == 5:
                u = 0.9
        if 15 <= t < 25:
            u = 0.9
        if 25 <= t < 30:
            if flag == 1:
                u = -0.016 * (t - 50) + 4.1
            elif flag == 2:
                u = -0.00032 * pow((t - 50), 2) - (0.016 + 0.00032 * 450) * (t - 50) + 4.1 - 50000 * 0.00032
            elif flag == 3:
                u = 0.02195 * (t - 50) / (-195.1 + (t - 50))
            elif flag == 4:
                u = 0.81103 / (1 + math.exp(((t - 50) - 225) / 5)) + 0.0944
            elif flag == 5:
                u = 0.1
        if t >= 30:
            u = 0.1
    return u


class InitCells(CellEnvMethod):
    def run(self, cell: Cell, env: Env):
        cell.setAttr(Type, 0)
        cell.setAttr(age, 0)
        cell.setAttr(profq, 0)
        cell.setAttr(X0, random.uniform(0, 1))
        cell.setAttr(X1, random.uniform(0, 0.1))
        env.setAttr(time, T0)
        env.setAttr(prolif, 1)
        env.setAttr(NumPoolCell, N0)
        env.setAttr(restingNum, 0)
        env.setAttr(diffNum, 0)
        env.setAttr(dieNum, 0)
        env.setAttr(divNum, 0)
        env.setAttr(divNumNew, 0)


class FateDecision(CellEnvMethod):
    def run(self, cell: Cell, env: Env):
        mu = func_env(env.getAttr(U), cell.getAttr(X1)) * dt
        beta = fbeta(N0, cell.getAttr(X0), cell.getAttr(X1)) * dt
        kappa = fkappa(cell.getAttr(X0)) * dt
        # Type变为0
        cell.setAttr(Type, 0)
        # 判断是否进入分裂期、是否完成分裂
        if cell.getAttr(profq) == 0:
            rand = random.uniform(0,1)
            if rand < kappa:
                cell.setAttr(Type, 3)
            elif rand < (kappa + beta):
                cell.setAttr(Type, 4)
                cell.setAttr(profq, 1)
                cell.setAttr(age, 0)
        elif cell.getAttr(profq) == 1:
            rand = random.uniform(0, 1)
            if rand < mu:
                cell.setAttr(Type, 2)
            else:
                if cell.getAttr(age) < tau:
                    cell.setAttr(Type, 4)
                    cell.incrAttr(age, dt)
                else:  # 分裂处理
                    cell.setAttr(Type, 1)
                    cell.setAttr(X0, GetnextEpi(0, cell.getAttr(X0), cell.getAttr(X1), env.getAttr(U)))
                    cell.setAttr(profq, 0)
                    cell.setAttr(age, 0)

        #
        ty = cell.getAttr(Type)
        if ty == 3:  # 分化
            env.incrAttr(diffNum, 1)
            cell.remove()
        elif ty == 0:  # 静息态
            env.incrAttr(restingNum, 1)
        elif ty == 4:  # 分裂期
            env.incrAttr(divNum, 1)
            cell.incrAttr(age, dt)
        elif ty == 1:  # 分裂过程
            if env.getCellNum() <= MAXCELLNUM:  # 分裂完成
                cell.proliferate()
                _age = cell.getAttr(age)
                _profq = cell.getAttr(profq)
                _x0 = cell.getAttr(X0)
                _x1 = cell.getAttr(X1)
                cell.setDaughtersAttr(age, _age)
                cell.setDaughtersAttr(profq, _profq)
                cell.setDaughtersAttr(X0, _x0)
                cell.setDaughtersAttr(X1, _x1)
                cell.setDaughtersAttr(Type, 0)
                env.incrAttr(divNumNew, 2)
            else:
                env.incrAttr(restingNum, 1)  # 退回静息态
        elif ty == 2:  # 死亡
            env.incrAttr(dieNum, 1)
            cell.remove()




