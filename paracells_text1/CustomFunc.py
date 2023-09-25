import ParaCellsError
import abc
from Cell import Cell
from Environment import Env


class AbstractMethod(metaclass=abc.ABCMeta):
    pass


# The CellMethod abstract class is the part that needs to be implemented by the user
# which contains a custom method for the operation of a single cell.
class CellMethod(AbstractMethod):
    @abc.abstractmethod
    def run(self, cell: Cell):
        pass


# The CellEnvMethod abstract class contains a custom method for the operation of one cell and the environment
# which also needs to be accomplish by user.
class CellEnvMethod(AbstractMethod):
    @abc.abstractmethod
    def run(self, cell: Cell, env: Env):
        pass


# test
# class MyMethod(CellMethod):
#     def run(self, cell: Cell):
#         print("ok")
#
#
# m = MyMethod()
# print(m.__class__.__base__ == CellMethod)
