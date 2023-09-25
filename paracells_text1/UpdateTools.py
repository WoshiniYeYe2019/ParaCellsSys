from CustomFunc import *
import random


class PoolPadding(CellMethod):
    """
    !! Need fate_decision = True. !!
    """
    def run(self, cell: Cell):
        N = cell.getCellMat().shape[0]
        p0 = cell.getMaxCellNum() / N
        if random.uniform(0, 1) > p0:
            cell.remove()
