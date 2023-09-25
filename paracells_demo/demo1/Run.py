from CellSystem import CellSystem
from CustomFunc import *
from CustomClass import *
import random
import UpdateTools
from demo1.Rand import *
from demo1.Settings import *
from demo1.Functions import InitCells, func_env, FateDecision

if __name__ == '__main__':
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

    cell_ids = [Type, profq, age, X0, X1]
    env_ids = [time, prolif, NumPoolCell, restingNum, diffNum, dieNum, divNum, divNumNew, U]

    # 初始化实验系统
    system = CellSystem(N0, cell_ids, env_ids, maxCellNum=MAXCELLNUM)
    init_cells = InitCells()
    system.updateSystem(init_cells, fate_decision=False)
    fate_decision = FateDecision()
    # 设置记录的环境数据
    system.setRecordAttrs(time, NumPoolCell, restingNum, diffNum, dieNum, divNum, divNumNew)
    # system.setRecordAttrs(time, diffNum, dieNum, divNum, divNumNew)

    # 迭代循环
    while system.getEnvParam(time) < T1:
        # 环境统计数据清零
        system.setEnvParam(restingNum, 0)
        system.setEnvParam(dieNum, 0)
        system.setEnvParam(diffNum, 0)
        system.setEnvParam(divNum, 0)
        system.setEnvParam(divNumNew, 0)

        currentCellNum = system.getCellNum()
        # 计算u
        u = func_env(system.getEnvParam(time), uflag)
        system.setEnvParam(U, u)

        # 更新每个细胞
        system.updateSystem(fate_decision, fate_decision=True)

        system.setEnvParam(NumPoolCell, system.getCellNum())
        # 记录环境统计数据
        system.record()
        # 增加系统时间
        system.incrEnvParam(time, dt)
        system.printAll()

    system.genLineChart(time, show=False, url="demo1.png")
