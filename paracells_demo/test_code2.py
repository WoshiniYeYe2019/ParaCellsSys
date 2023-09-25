from CellSystem import CellSystem
from CustomFunc import *
from CustomClass import *
import random
import UpdateTools

# 这里是测试不设置custom_class的代码

if __name__ == '__main__':
    age = 'age'
    rate = 'rate'

    count = 'count'

    cell_ids = [age, rate]
    env_ids = [count]

    class FateMethod(CellMethod):
        def run(self, cell: Cell):
            cell.incrAttr(age, 1)
            if cell.getAttr(rate) > 0.6:
                cell.proliferate()
                cell.setDaughtersAttr(age, 0)
                cell.setDaughtersAttr(rate, random.uniform(0, 1))
            elif cell.getAttr(rate) < 0.4:
                cell.remove()

    class InitialMethod(CellMethod):
        def run(self, cell: Cell):
            cell.setAttr(rate, random.uniform(0, 1))

    class StatisticMethod(CellEnvMethod):
        def run(self, cell: Cell, env: Env):
            if cell.getAttr(rate) >= 0.5:
                env.incrAttr(count, 1)


    fate_method = FateMethod()
    init_method = InitialMethod()
    statistic_method = StatisticMethod()
    pool_padding = UpdateTools.PoolPadding()

    my_system = CellSystem(initCellNum=10, cellAttr=cell_ids, envParam=env_ids, maxCellNum=30)
    my_system.addCells(10)
    my_system.updateSystem(init_method, fate_decision=False)

    for i in range(10):
        print('time = ', i, '\n')
        my_system.updateSystem(fate_method, fate_decision=True)
        my_system.setEnvParam(count, 0)
        my_system.updateSystem(statistic_method, fate_decision=False)
        my_system.updateSystem(pool_padding)
        my_system.printAll()
        print('')
