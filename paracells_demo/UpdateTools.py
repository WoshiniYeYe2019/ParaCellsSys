from CustomFunc import *
import random


class PoolPadding(CellMethod):
    """
    !! Need fate_decision = True. !!
    """
    def __init__(self, flag: str = None, state=-1):
        """
        When the Cell's attribute 'flag' equal to the state, current cell won't be deleted in this way.

        :param flag: Attribute used as a judgment condition.
        :param state: Cell won't be removed when attribute value equal to the state.
        """
        if flag is not None:
            self.__flag = str(flag)
        else:
            self.__flag = None
        self.__state = state

    def run(self, cell: Cell):
        """
        !! Need fate_decision = True. !!
        """
        N = cell.getCellMat().shape[0]
        p0 = cell.getMaxCellNum() / N
        if self.__flag is not None and cell.getAttr(self.__flag) != self.__state:
            if random.uniform(0, 1) > p0:
                cell.remove()
        elif self.__flag is None:
            if random.uniform(0, 1) > p0:
                cell.remove()


