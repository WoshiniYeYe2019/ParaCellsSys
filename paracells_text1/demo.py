import math
import RAND
import time
import random
from CellSystem import CellSystem
from CustomFunc import *
from UpdateTools import PoolPadding

# 基础设定
RANDMAX = 23371.0
RANDPI = 3.1415926

beta0 = 0.12
kappa0 = 0.2
theta0 = 1e3
eta = 60
p_a1 = 5.8
p_a2 = 2.2
p_a3 = 3.75
p_a4 = 2.0
p_b1 = 4.0
mu0 = 2e-3
tau = 20

alpha1 = 1.65
alpha2 = 1.56

dt = 0.25
T0 = 50
T1 = 200
ntpr = 4
ntpx = 1
INITCELL = 1024  # 初始细胞数
MAXCELL = 1024  # 最大细胞数

# 设置细胞属性和环境参数
X0 = 'X0'
X1 = 'X1'
ProfQ = 'ProfQ'
Type = 'Type'
age = 'age'
cellAttributes = [X0, X1, ProfQ, Type, age]

t = 't'
Prolif = 'Prolif'
NumCell = 'NumCell'
NumPoolCell = 'NumPoolCell'
N0 = 'N0'
N1 = 'N1'
N2 = 'N2'
N3 = 'N3'
N4 = 'N4'
N5 = 'N5'
environmentParameters = [t, Prolif, NumCell, NumPoolCell, N0, N1, N2, N3, N4, N5]


# 数学计算函数(不属于系统的一部分, 项目中特有的函数)
def fdeathrate():
    mu = mu0
    return mu


def fbeta(N0_, x1, x2):
    theta = theta0 * (1.0 + pow(p_a4 * x2, 6.0) / (1.0 + pow(p_a4 * x2, 6.0)))
    beta = beta0 * (1.0 / (1.0 + N0_ / theta)) * (
            (p_a1 * x1 + pow(p_a2 * x1, 6.0)) / (1 + pow(p_a3 * x1, 6.0)))
    return beta


def fkappa(x1):
    kappa = kappa0 * 1.0 / (1.0 + pow(p_b1 * x1, 6.0))
    return kappa


def GetnextEpi(i, t_, x1, x2):
    if i == 0:
        phi = 0.08 + 1.0 * pow(alpha1 * x1, 1.8) / (1 + pow(alpha1 * x1, 1.8))
    elif i == 1:
        f = 1.0 / (1 + math.exp(-(t_ - T0) / 1000.0))
        phi = 0.08 + (1.0 + f * 0.4 / (1 + pow(2.5 * x1, 6))) * pow(alpha2 * x2, 1.8) / (1 + pow(alpha2 * x2, 1.8))

    a = eta * phi
    b = eta * (1 - phi)
    z = RAND.BetaDistribution(a, b)

    return z


# 所有细胞初始化函数
class CellInitial(CellMethod):
    def run(self, cell: Cell):
        cell.setAttr(X0, random.uniform(0, 1))
        cell.setAttr(X1, random.uniform(0, 0.1))


# 主要的迭代函数
class CellTypeDecisionFunc(CellEnvMethod):
    def run(self, cell: Cell, env: Env):
        mu = fdeathrate() * dt
        beta = fbeta(env.getAttr(N0), cell.getAttr(X0), cell.getAttr(X1)) * dt
        kappa = fkappa(cell.getAttr(X0)) * dt

        cell.setAttr(Type, 0)

        if int(cell.getAttr(ProfQ)) == 0:
            rand = RAND.Value_()
            if rand < kappa:
                cell.setAttr(Type, 3)
                cell.remove()
            else:
                if rand < kappa + beta:
                    cell.setAttr(Type, 4)
                    cell.setAttr(ProfQ, 1)
                    cell.setAttr(age, 0)

        if int(cell.getAttr(ProfQ)) == 1:
            rand = RAND.Value_()
            if rand < mu:
                cell.setAttr(Type, 2)
                cell.remove()
            else:
                if cell.getAttr(age) < tau:
                    cell.incrAttr(age, dt)

                else:
                    # 有丝分裂
                    cell.setAttr(Type, 1)
                    cell.proliferate()

                    # 修改子细胞属性
                    # 用setDaughtersAttr()不加第三个参数默认将子细胞1、2的数值全部修改
                    cell.setDaughtersAttr(X0, GetnextEpi(0, env.getAttr(t), cell.getAttr(X0),
                                                         cell.getAttr(X1)))
                    cell.setDaughtersAttr(X1, GetnextEpi(1, env.getAttr(t), cell.getAttr(X0),
                                                         cell.getAttr(X1)))
                    cell.setDaughtersAttr(ProfQ, 0)
                    cell.setDaughtersAttr(age, 0)

        if int(cell.getAttr(Type)) == 3:
            env.incrAttr(N1, 1)
        elif int(cell.getAttr(Type)) == 4 or int(cell.getAttr(Type)) == 0:
            env.incrAttr(N0, 1)
            if int(cell.getAttr(ProfQ)) == 0:
                env.incrAttr(N5, 1)
            else:
                env.incrAttr(N4, 1)
        elif int(cell.getAttr(Type)) == 1:
            env.incrAttr(N0, 2)
            env.incrAttr(N2, 1)
        elif int(cell.getAttr(Type)) == 2:
            env.incrAttr(N3, 1)


def main():
    Time = 0
    step = 0
    url = 'output.txt'
    # 实例化系统
    system = CellSystem(INITCELL, cellAttributes, environmentParameters, maxCellNum=MAXCELL)
    # 实例化迭代函数
    cellInitial = CellInitial()
    cellDecision = CellTypeDecisionFunc()
    poolPadding = PoolPadding()
    # 初始化细胞数值
    system.updateSystem(cellInitial, fate_decision=False)

    system.setEnvParam(NumCell, INITCELL)
    f = open(url, 'w', encoding='UTF-8-sig')
    while Time <= T1:
        system.setEnvParam(t, Time)
        system.setEnvParam(N0, 0)
        system.setEnvParam(N1, 0)
        system.setEnvParam(N2, 0)
        system.setEnvParam(N3, 0)
        system.setEnvParam(N4, 0)
        system.setEnvParam(N5, 0)
        system.setEnvParam(NumPoolCell, system.getCellNum())
        # 进行迭代
        system.updateSystem(cellDecision)
        # 每次迭代后的处理
        system.setEnvParam(Prolif, system.getEnvParam(N0) / system.getEnvParam(NumPoolCell))
        system.setEnvParam(NumCell,
                           system.getEnvParam(NumCell) * system.getEnvParam(Prolif))
        system.setEnvParam(NumPoolCell, system.getCellNum())
        system.updateSystem(poolPadding)
        Time += dt
        step += 1
        if step % ntpx == 0:
            for i in range(system.getEnvAttrNum() - 1):
                f.write("%.4f " % system.getEnv()[i])
            f.write('\n')
    f.close()


if __name__ == '__main__':
    # 监测运行时间
    time1 = time.time()
    main()
    print("所用时间：", time.time() - time1)


