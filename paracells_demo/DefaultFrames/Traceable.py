from Cell import Cell
from Environment import Env
from CellSystem import CellSystem
from CustomFunc import *
from CustomClass import *
import SystemTools
import UpdateTools
import random

# Settings
MAXCELLNUM = 50
INITCELLNUM = 10
saving_file = 'historyEpoch'
T0 = 0
T1 = 10
dT = 1

# Cell attributes
parentsId = 'parentsId'
state = 'state'
attr1 = 'attr1'
attr2 = 'attr2'
age = 'age'
num = 'num'  # 细胞的随机标识，验证trace功能的正确性
# Environment parameters
time = 'time'
s0 = 's0'
s1 = 's1'
s2 = 's2'
sd = 'sd'
# Generate identifiers
cell_ids = [parentsId, state, attr1, attr2, age, num]
env_ids = [time, s0, s1, s2, sd]


# Define custom function
# Initial cells' attributes
class SimulateInitFunc(CellMethod):
    def run(self, cell: Cell):
        cell.setAttr(parentsId, -1)  # 初始一批细胞母细胞id为-1
        cell.setAttr(state, 0)
        cell.setAttr(attr1, random.randint(1, 6))
        cell.setAttr(attr2, random.randint(1, 6))
        cell.setAttr(age, 0)
        cell.setAttr(num, random.randint(0, 5000))


# Simulation fate decision function.
class SimulateFateFunc(CellEnvMethod):
    def run(self, cell: Cell, env: Env):
        a1 = cell.getAttr(attr1)
        a2 = cell.getAttr(attr2)
        ag = cell.getAttr(age)
        stt = cell.getAttr(state)

        # VERY IMPORTANT !!!!!
        cell.setAttr(parentsId, cell.getCellId())

        if stt == 0:  # 普通状态
            if ag > 5:
                cell.remove()  # 细胞衰老死亡
                env.incrAttr(sd, 1)
            elif a1 >= 5:  # 以1/3概率进入准备分裂阶段
                cell.setAttr(state, 1)  # 进入state1
                env.incrAttr(s1, 1)
            else:
                cell.setAttr(attr1, random.randint(1, 6))  # 重设随机数1
                env.incrAttr(s0, 1)
            # 2/3概率维持普通状态
        elif stt == 1:  # 准备分裂阶段
            if ag > 5:
                cell.remove()  # 细胞衰老死亡
                env.incrAttr(sd, 1)
            elif a2 == 1:  # 1/6概率在准备分裂时死亡
                cell.remove()
                env.incrAttr(sd, 1)
            elif a2 >= 4:  # 以1/2概率分裂增殖
                cell.setAttr(state, 2)  # 进入state2
                env.incrAttr(s2, 1)
                cell.proliferate()
                cell.setDaughtersAttr(parentsId, cell.getCellId())
                cell.setDaughtersAttr(age, 0)
                cell.setDaughtersAttr(state, 0)
                cell.setDaughter1Attr(attr1, random.randint(1, 6))
                cell.setDaughter1Attr(attr2, random.randint(1, 6))
                cell.setDaughter2Attr(attr1, random.randint(1, 6))
                cell.setDaughter2Attr(attr2, random.randint(1, 6))
            else:  # 维持准备分裂阶段
                env.incrAttr(s1, 1)
                cell.setAttr(attr2, random.randint(1, 6))  # 重设随机数2
        # 增加细胞年龄
        cell.incrAttr(age, 1)


if __name__ == '__main__':
    # 实例化所有更新系统函数
    init_func = SimulateInitFunc()
    fate_func = SimulateFateFunc()
    pool_padding = UpdateTools.PoolPadding(flag=state, state=1)  # 准备增殖状态的细胞不会因超出最大细胞数被删除
    # 初始化系统
    system = CellSystem(INITCELLNUM, cell_ids, env_ids, MAXCELLNUM)
    system.updateSystem(init_func, fate_decision=False)
    system.setEnvParam(time, 0)
    # 保存初始状态
    system.savePool_epoch(saving_file)
    while system.getEnvParam(time) < T1:
        # 增加系统时间
        system.incrEnvParam(time, dT)
        # 重设环境统计
        system.setEnvParam(s0, 0)
        system.setEnvParam(s1, 0)
        system.setEnvParam(s2, 0)
        system.setEnvParam(sd, 0)
        # 更新环境
        system.updateSystem(fate_func, fate_decision=True, incr_epoch=True)
        system.updateSystem(pool_padding, fate_decision=True)
        # 保存细胞池
        system.savePool_epoch(saving_file)
        system.printAll()

    ancestor = SystemTools.trace(system, saving_file, cellId=0, trace_attr=parentsId, to_epoch=0)
    print('祖先细胞为：', ancestor)

