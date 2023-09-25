from Identifiers import Identifiers
from CustomClass import CustomClass
import copy
import SystemError
import numpy as np


class Cell:
    def __init__(self, cellMat, x, ids: Identifiers, maxCellNum: int, customObj: CustomClass = None):
        self.__cellMat = cellMat
        self.__x = x
        self.__ids = ids
        self.__maxCellNum = maxCellNum
        if customObj is not None:
            self.__customObj = customObj
            self.__daughter1Obj = copy.deepcopy(customObj)
            self.__daughter2Obj = copy.deepcopy(customObj)
        else:
            self.__customObj = None
            self.__daughter1Obj = None
            self.__daughter2Obj = None

        self.__resultCellNum = 1
        self.__daughter1Attr = None
        self.__daughter2Attr = None

    def getCellMat(self):
        """
        :return: All cells in the system.
        """
        return self.__cellMat

    def getCellId(self):
        """
        :return: Current cell id.
        """
        return self.__x

    def findName(self, name: str):
        """
        :param: The attribute name as str.\n
        :return: The name's index from identifiers.
        """
        return self.__ids.findName(name)

    def getMaxCellNum(self):
        """
        :return: Max cell number of current system.
        """
        return self.__maxCellNum

    def getCustomObj(self):
        """
        :return: Custom object of the current cell.
        """
        return self.__customObj

    def setAttr(self, attrName: str, value):
        """
        Reset the value of the chosen attribute.\n
        :param attrName: The name of the attribute which you want to reset.
        :param value: The new value of the chosen attribute.
        :return: nothing
        """
        index = self.findName(attrName)

        if index != -1:
            self.__cellMat[self.__x][index] = value

    def incrAttr(self, attrName: str, value):
        """
        Increase the given value to attribute.\n
        :param attrName: The name of the attribute which you want to increase.
        :param value: The increased value.
        :return: nothing
        """
        index = self.findName(attrName)

        if index != -1:
            self.__cellMat[self.__x][index] += value

    def getAttr(self, attrName):
        """

        :param attrName: The name of the attribute you want.
        :return: Value of the chosen attribute.
        """
        index = self.findName(attrName)

        if index != -1:
            return self.__cellMat[self.__x][index]
        else:
            return -1

    def remove(self):
        """
        Call this method to remove current cell from your system.\n
        This action will set the result cell number to 0.
        """
        if self.__resultCellNum != 1:
            return
        else:
            self.__resultCellNum = 0

    def proliferate(self):
        """
        Call this method to make current cell proliferate.\n
        This would set the result cell number to 2, which means current cell will
        be replaced by its 2 daughter cells in your system.
        """
        if self.__resultCellNum != 1:
            return
        else:
            self.__resultCellNum = 2
            self.__daughter1Attr = self.__cellMat[self.__x].copy()
            self.__daughter2Attr = self.__cellMat[self.__x].copy()

    def setDaughter1Attr(self, attrName: str, value):
        """
        Reset the first daughter cell's attribute.
        """
        if self.__resultCellNum != 2:
            return

        index = self.findName(attrName)

        if index != -1:
            self.__daughter1Attr[index] = value

    def setDaughter2Attr(self, attrName: str, value):
        """
        Reset the second daughter cell's attribute.
        """
        if self.__resultCellNum != 2:
            return

        index = self.findName(attrName)

        if index != -1:
            self.__daughter2Attr[index] = value

    def setDaughtersAttr(self, attrName: str, value, daughter_num: int = 0):
        """
        Set daughter cells' attribute.\n
        :param attrName: The attribute name to reset.
        :param value: The new value.
        :param daughter_num: Defaulted 0 to change both daughter cells, or transfer 1 or 2 to change one of them.
        :return: -1 and do nothing if daughter_num is other than (0, 1, 2).
        """
        if daughter_num == 0:
            self.setDaughter1Attr(attrName, value)
            self.setDaughter2Attr(attrName, value)
        elif daughter_num == 1:
            self.setDaughter1Attr(attrName, value)
        elif daughter_num == 2:
            self.setDaughter2Attr(attrName, value)
        else:
            return -1

    def getResultCellNum(self):
        """

        :return: The result cell number after the current cell calculate.
        """
        return self.__resultCellNum

    def getDaughter1Attr(self):
        """

        :return: The first daughter cell's attribute array.
        """
        return self.__daughter1Attr

    def getDaughter2Attr(self):
        """

        :return: The second daughter cell's attribute array.
        """
        return self.__daughter2Attr

    def getDaughtersObj(self, daughter_num: int = 0):
        """
        If you didn't create a custom object, calling of this method will raise a paraCellsError.\n
        :param daughter_num: Defaulted 0 to change both daughter cells, or transfer 1 or 2 to change one of them.
        :return: Daughter cells' custom object.
        """
        if self.__customObj is not None:
            if daughter_num == 0:
                return [self.__daughter1Obj, self.__daughter2Obj]
            elif daughter_num == 1:
                return self.__daughter1Obj
            elif daughter_num == 2:
                return self.__daughter2Obj
            else:
                return -1
        else:
            SystemError.raiseError("There's no custom objects in this cellSystem.")
            return
