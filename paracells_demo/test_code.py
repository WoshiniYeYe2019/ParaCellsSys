from Cell import Cell
from CellSystem import CellSystem
from CustomFunc import *
from CustomClass import *
import random
import UpdateTools

if __name__ == '__main__':
    # 确定细胞属性和环境参数
    # cell attributes
    state = 'state'
    age = 'age'
    # environment parameters
    time = 'time'
    statistic = 'statistic'
    other_param = 'other_param'
    # 构建字符串列表
    cell_ids = [state, age]
    env_ids = [time, statistic, other_param]


    # 自定义细胞内对象, 继承抽象类CustomClass
    class X(CustomClass):
        def __init__(self):
            super().__init__()
            # 假设细胞内有两个隐藏的随机参数
            self.x1 = random.uniform(0, 1)
            self.x2 = random.uniform(0, 1)

        def reRand(self):
            # 重新生成数值
            self.x1 = random.uniform(0, 1)
            self.x2 = random.uniform(0, 1)


    # 创建自定义方法, 继承抽象类CellEnvMethod或CellMethod之一
    class UpdateFunc(CellEnvMethod):
        # 这个方法是传入细胞和环境的方法(CellEnvMethod)
        def run(self, cell: Cell, env: Env):
            obj = cell.getCustomObj()
            # 为功能示范模拟的分支语句
            if obj.x1 > obj.x2:
                # 如果隐藏随机数1大于隐藏随机数2, 统计数据加1
                env.incrAttr(statistic, 1)
            if obj.x1 + obj.x2 >= 1:
                # 如果两个隐藏随机数之和大于1, 修改细胞属性
                cell.setAttr(state, 1)
                # 重设随机数
                obj.reRand()
            if cell.getAttr(state) == 1:
                # 另外一个环境统计参数加1
                env.incrAttr(other_param, 1)


    class FateFunc(CellMethod):
        # 继承CellMethod抽象类的方法只传入Cell, 也就是无法对环境参数修改
        # 这样分类的目的是今后尝试实现cpu并行时, 避免多进程访问共享数据造成数据污染
        def run(self, cell: Cell):
            # 模拟细胞年龄增长
            cell.incrAttr(age, 1)
            # 获取细胞内自定义对象
            obj = cell.getCustomObj()
            # 细胞增殖的逻辑判断, 这里只是用比较简单的逻辑演示
            if cell.getAttr(age) == 3:
                # 调用cell.proliferate()函数使细胞在系统层面处于增殖态
                cell.proliferate()
                # 重设子细胞的属性值
                cell.setDaughtersAttr(age, 0)
                cell.setDaughtersAttr(state, 0)
                # 获得子细胞自定义对象的函数默认daughter_num参数为0, 返回两个子细胞对象的二元list
                d_objs = cell.getDaughtersObj(daughter_num=0)
                # 对每个子细胞对象重新生成随机数
                for i in d_objs:
                    i.reRand()
            # 一个简单的细胞移除判断逻辑
            elif obj.x1 + obj.x2 > 1.5:
                cell.remove()


    # 创建系统时, 如果需要使用自定义对象功能, 需要传入一个实例化的CustomClass子类对象
    OBJ = X()
    # 将所有更新系统的method实例化
    fate_func = FateFunc()
    update_func = UpdateFunc()
    # 这里为了不让系统内的细胞过多，使用了Tools.py的PoolPadding方法, 实际上和自定义的method原理相同
    # 将来可以把常用的科学计算方法都写在Tools内
    pool_padding = UpdateTools.PoolPadding()
    # 实例化CellSystem
    my_system = CellSystem(initCellNum=10, cellAttr=cell_ids, envParam=env_ids, maxCellNum=30, customObj=OBJ)
    my_system.addCells(10)
    maxT = 1000
    dT = 1
    # 设置需要记录的环境参数(可选)
    my_system.setRecordAttrs(time, statistic, other_param)
    # 如果需要, 可以写循环对系统迭代多次
    while my_system.getEnvParam(time) <= maxT:
        # 设置系统模拟时间
        my_system.incrEnvParam(time, dT)
        # 用如下格式传入自定义的方法并迭代系统
        my_system.updateSystem(method=fate_func, fate_decision=True)
        # 重设环境统计参数
        my_system.setEnvParam(statistic, 0)
        my_system.setEnvParam(other_param, 0)
        my_system.updateSystem(method=update_func, fate_decision=False)
        # 调用PoolPadding削减细胞池内数量
        my_system.updateSystem(method=pool_padding, fate_decision=True)
        # 输出显示细胞和环境及其各属性的状态
        my_system.printAll()
        # 每次迭代记录参数
        my_system.record()
    # 终端输出每次迭代记录的环境参数
    my_system.printRecord()
    # 生成折线图，用time环境属性作为横坐标
    my_system.genLineChart(time, show=False, url="graph/test_code1.png")
    # 生成散点图
    my_system.genScatterChart(time, show=False, url="graph/test_code2.png")
