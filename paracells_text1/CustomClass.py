import abc
import ParaCellsError


# This abstract class acts as part of the cell to aid in computation.
# To use it, you need to implement its __init__() which is indispensable.
# You can also add more functions to make calculate easier,
# they can be called in your CustomFunctions. (both CellMethod and CellEnvMethod in CustomFunc.py)
class CustomClass(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass
