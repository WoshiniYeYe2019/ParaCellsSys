from Identifiers import Identifiers
import ParaCellsError
from Environment import Env
from Cell import Cell
from CustomClass import CustomClass
from CustomFunc import *
import copy
import numpy as np


class CellSystem:
    def __init__(self, initCellNum: int, cellAttr: list, envParam: list, maxCellNum: int = 100,
                 customObj: CustomClass = None, dT:float = 0, T0:float = 0, T1:float = 0):
        """

        :param initCellNum: This number decided the starting cell number of your system.
        :param cellAttr: This parameter should be a list[string] of all the attributes' name of cells in your system.
        :param envParam: A list of the environment parameters' name in string.
        :param maxCellNum: Defaulted is 100. This parameter wouldn't impact your system's calculation.
        :param customObj: This part is optional. Give an instantiated custom object and the system would deepcopy
         as many times as the initial number of cells.
        """
        self.__cellAttrIds = Identifiers(cellAttr)
        self.__envParamIds = Identifiers(envParam)
        self.__maxCellNum = maxCellNum
        self.dT = dT
        self.T0 = T0
        self.T1 = T1

        if initCellNum <= 0:
            initCellNum = 1

        self.__pool = np.zeros((initCellNum, self.__cellAttrIds.getNum()))
        self.__array = np.zeros(self.__envParamIds.getNum())
        if customObj is not None:
            self.__objs = [copy.deepcopy(customObj) for i in range(initCellNum)]
            self.__objModel = copy.deepcopy(customObj)
        else:
            self.__objs = None
            self.__objModel = None

    def getCellNum(self):
        """

        :return: Current cell number.
        """
        return self.__pool.shape[0]

    def getCellAttrNum(self):
        """

        :return: Amount of attributes of each cells.
        """
        return self.__pool.shape[1]

    def getEnvAttrNum(self):
        """

        :return: Amount of parameters of the environment.
        """
        return self.__array.shape[0]

    def getPool(self):
        """

        :return: Whole cell pool matrix in your system.
        """
        return self.__pool

    def getEnv(self):
        """

        :return: The environment array.
        """
        return self.__array

    def getMaxCellNum(self):
        """

        :return: The setting max cell number.
        """
        return self.__maxCellNum

    def getObjs(self):
        """
        If you didn't instantiated any object at the initial state of the system, it will raise an error.\n
        :return: A list of all the cells' custom objects.
        """
        if self.__objs is not None:
            return self.__objs
        else:
            ParaCellsError.raiseError("No custom objects are instantiated.")
            return -1

    def addCells(self, num: int, method: AbstractMethod = None):
        """
        Add a given number of cells to the cell pool.\n
        :param num: Number of cells to be added.
        :param method: A method of operating on newly added cells.
        :return: nothing
        """
        for i in range(num):
            newCell = np.zeros((1, self.__pool.shape[1]))
            self.__pool = np.vstack((self.__pool, newCell))
            if self.__objs is not None:
                self.__objs.append(copy.deepcopy(self.__objModel))

            if method is not None:
                if method.__class__.__base__ == CellEnvMethod:
                    if self.__objs is not None:
                        cell = Cell(self.__pool, self.getCellNum() - 1, self.__cellAttrIds, self.__maxCellNum,
                                    self.__objs[self.getCellNum() - 1])
                    else:
                        cell = Cell(self.__pool, self.getCellNum() - 1, self.__cellAttrIds, self.__maxCellNum)
                    env = Env(self.__array, self.__envParamIds, self.getCellNum(), self.getMaxCellNum())
                    method.run(cell, env)
                elif method.__class__.__base__ == CellMethod:
                    if self.__objs is not None:
                        cell = Cell(self.__pool, self.getCellNum() - 1, self.__cellAttrIds, self.__maxCellNum,
                                    self.__objs[self.getCellNum() - 1])
                    else:
                        cell = Cell(self.__pool, self.getCellNum() - 1, self.__cellAttrIds, self.__maxCellNum)
                    method.run(cell)

    def addCellsFromMatrix(self, matrix: np.ndarray, method: AbstractMethod = None):
        """
        Pass in a matrix as a new part of the cell pool.\n
        :param matrix: Matrix of new cells.
        :param method: A method of operating on newly added cells.
        :return: nothing
        """
        if matrix.__class__ is not np.ndarray:
            matrix = np.array(matrix)
        num = matrix.shape[0]
        start = self.getCellNum()
        self.__pool = np.vstack((self.__pool, matrix))
        if self.__objs is not None:
            for i in range(num):
                self.__objs.append(copy.deepcopy(self.__objModel))

        if method is not None:
            if method.__class__.__base__ == CellEnvMethod:
                for i in range(num):
                    if self.__objs is not None:
                        cell = Cell(self.__pool, start + i, self.__cellAttrIds, self.__maxCellNum,
                                    self.__objs[start + 1])
                    else:
                        cell = Cell(self.__pool, start + i, self.__cellAttrIds, self.__maxCellNum)
                    env = Env(self.__array, self.__envParamIds, self.getCellNum(), self.__maxCellNum)
                    method.run(cell, env)
            elif method.__class__.__base__ == CellMethod:
                for i in range(num):
                    if self.__objs is not None:
                        cell = Cell(self.__pool, start + i, self.__cellAttrIds, self.__maxCellNum,
                                    self.__objs[start + 1])
                    else:
                        cell = Cell(self.__pool, start + i, self.__cellAttrIds, self.__maxCellNum)
                    method.run(cell)

    def addCellAttr(self, attrName: str, method: AbstractMethod = None):
        """
        Add a new cell attribute.\n
        :param attrName: New attribute's name.
        :param method: The operation on each cell to initialize new properties.
        :return: nothing
        """
        self.__cellAttrIds.addName(str(attrName))

        newAttr = np.zeros((self.getCellNum(), 1))
        self.__pool = np.hstack((self.__pool, newAttr))

        if method is not None:
            if method.__class__.__base__ == CellEnvMethod:
                for i in range(self.getCellNum()):
                    cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum,
                                self.__objs[i])
                    env = Env(self.__array, self.__envParamIds, self.getCellNum(), self.__maxCellNum)
                    method.run(cell, env)
            elif method.__class__.__base__ == CellMethod:
                for i in range(self.getCellNum()):
                    cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum,
                                self.__objs[i])
                    method.run(cell)

    def addEnvParam(self, paramName: str, value):
        """
        Add a new environment parameter.\n
        :param paramName: New parameter's name.
        :param value: New parameter's value.
        :return: nothing
        """
        self.__envParamIds.addName(str(paramName))
        self.__array = np.append(self.__array, value)

    def setCellAttr(self, cellId: int, attrName: str, value):
        """
        Reset an attribute of a cell.\n
        :param cellId: Cell's id you need to reset.
        :param attrName: Attribute's name.
        :param value: New value.
        :return: nothing or -1 if false.
        """
        index = self.__cellAttrIds.findName(attrName)

        if index != -1:
            self.__pool[cellId][index] = value
        else:
            return -1

    def incrCellAttr(self, cellId: int, attrName: str, value):
        """
        Increments a cell's attribute by one value
        :param cellId: Cell's id you need to increase.
        :param attrName: Attribute's name.
        :param value: Increased value.
        :return: nothing or -1 if false.
        """
        index = self.__cellAttrIds.findName(attrName)

        if index != -1:
            self.__pool[cellId][index] += value
        else:
            return -1

    def setEnvParam(self, paramName: str, value):
        """
        Reset a parameter of a cell.\n
        :param paramName: Parameter's name you need to reset.
        :param value: New value.
        :return: nothing or -1 if false.
        """
        index = self.__envParamIds.findName(paramName)

        if index != -1:
            self.__array[index] = value
        else:
            return -1

    def incrEnvParam(self, paramName: str, value):
        """
        Increments a env parameter by one value.\n
        :param paramName: Parameter's name.
        :param value: Increased value.
        :return: nothing or -1 if false.
        """
        index = self.__envParamIds.findName(paramName)

        if index != -1:
            self.__array[index] += value
        else:
            return -1

    def getCellAttr(self, cellId: int, attrName: str):
        """

        :param cellId: The cell's id you want.
        :param attrName: Attribute's name.
        :return: The value of the given cell's given attribute.
        """
        index = self.__cellAttrIds.findName(attrName)

        if index != -1:
            return self.__pool[cellId][index]
        else:
            return -1

    def getEnvParam(self, paramName: str):
        """

        :param paramName: Parameter's name you want.
        :return: Value of the given paramName.
        """
        index = self.__envParamIds.findName(paramName)

        if index != -1:
            return self.__array[index]
        else:
            return -1

    def __updateSystem_FateDecision(self, method: AbstractMethod = None):
        num = self.getCellNum()

        dieCellsIndex = list()

        if method is not None:
            if method.__class__.__base__ == CellEnvMethod:
                for i in range(num):
                    if self.__objs is not None:
                        cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum, self.__objs[i])
                    else:
                        cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum)
                    env = Env(self.__array, self.__envParamIds, num, self.__maxCellNum)

                    method.run(cell, env)

                    if cell.getResultCellNum() == 2:
                        self.__pool[i] = cell.getDaughter1Attr()
                        self.__pool = np.vstack(
                            (self.__pool, cell.getDaughter2Attr().reshape((1, self.getCellAttrNum()))))
                        if self.__objs is not None:
                            self.__objs[i] = cell.getDaughtersObj(1)
                            self.__objs.append(cell.getDaughtersObj(2))
                    elif cell.getResultCellNum() == 0:
                        dieCellsIndex.append(i)
            elif method.__class__.__base__ == CellMethod:
                for i in range(num):
                    if self.__objs is not None:
                        cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum, self.__objs[i])
                    else:
                        cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum)

                    method.run(cell)

                    if cell.getResultCellNum() == 2:
                        self.__pool[i] = cell.getDaughter1Attr()
                        self.__pool = np.vstack(
                            (self.__pool, cell.getDaughter2Attr().reshape(1, self.getCellAttrNum())))
                        if self.__objs is not None:
                            self.__objs[i] = cell.getDaughtersObj(1)
                            self.__objs.append(cell.getDaughtersObj(2))
                    elif cell.getResultCellNum() == 0:
                        dieCellsIndex.append(i)

        if len(dieCellsIndex) > 0:
            self.__pool = np.delete(self.__pool, dieCellsIndex, 0)
            if self.__objs is not None:
                for i in range(len(dieCellsIndex)):
                    self.__objs.pop(dieCellsIndex[i])
                    dieCellsIndex = (np.array(dieCellsIndex) - 1).tolist()

    def __updateSystem_noFateDecision(self, method: AbstractMethod = None):
        num = self.getCellNum()

        if method is not None:
            if method.__class__.__base__ == CellEnvMethod:
                for i in range(num):
                    if self.__objs is not None:
                        cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum, self.__objs[i])
                    else:
                        cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum)
                    env = Env(self.__array, self.__envParamIds, num, self.__maxCellNum)

                    method.run(cell, env)
            elif method.__class__.__base__ == CellMethod:
                for i in range(num):
                    if self.__objs is not None:
                        cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum, self.__objs[i])
                    else:
                        cell = Cell(self.__pool, i, self.__cellAttrIds, self.__maxCellNum)

                    method.run(cell)

    def updateSystem(self, method: AbstractMethod = None, fate_decision=True):
        """
        Update each cell of the system using the given method.\n
        :param method: Must be an instantiated subclass of the abstract classes: CellMethod or CellEnvMethod.
        :param fate_decision: Choose if you want to enable the method to proliferate or remove cells.
        If fate_decision = False, the cell number won't change even if there's any proliferate or remove
        operations in your method.
        :return: nothing
        """
        if fate_decision:
            self.__updateSystem_FateDecision(method)
        else:
            self.__updateSystem_noFateDecision(method)

    def sumAttr(self, attrName: str):
        """
        Sum the given attribute of all cells.\n
        :param attrName: Attribute's name.
        :return: Sum value of the given attribute if found or -1 otherwise.
        """
        sums = np.sum(self.__pool, 0)
        index = self.__cellAttrIds.findName(attrName)

        if index != -1:
            return sums[index]
        else:
            return -1

    def printCells(self):
        print("==========Cells (", self.getCellNum(), ")==========")
        print("ID", end="")
        for i in self.__cellAttrIds.getNames():
            print("\t", i, end="")

        print("\n", end="")

        for i in range(self.getCellNum()):
            print(i, end="")
            for j in range(self.getCellAttrNum()):
                print("\t%.4f" % self.__pool[i][j], end="")
            print("\n", end="")

        print("\n", end="")

    def printEnvAttr(self):
        print("==========Environment Attributes (", self.getEnvAttrNum(), ")==========")
        print("Name\tValue")
        identifiers = self.__envParamIds.getNames()

        for i in range(self.getEnvAttrNum()):
            print(identifiers[i], "\t", "%.4f" % self.__array[i])

    def printAll(self):
        self.printCells()
        self.printEnvAttr()
