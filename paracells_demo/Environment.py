import SystemError
from Identifiers import Identifiers


class Env:
    def __init__(self, envArray, ids:Identifiers, currentCellNum:int, maxCellNum:int):
        self.__envArray = envArray
        self.__ids = ids
        self.__currentCellNum = currentCellNum
        self.__maxCellNum = maxCellNum

    def getEnvArr(self):
        """

        :return: Environment attribute array.
        """
        return self.__envArray

    def getAttr(self, paramName:str):
        """

        :param paramName: The name of the attribute which you want to get.
        :return: The chosen attribute's value if found, otherwise return -1.
        """
        index = self.__ids.findName(paramName)
        if index != -1:
            return self.__envArray[index]
        else:
            return -1

    def setAttr(self, paramName:str, value):
        """
        Reset the value of the chosen environment attribute.\n
        :param paramName: The name of the attribute you want to reset.
        :param value: The new value.
        :return: nothing if success, otherwise return -1.
        """
        index = self.__ids.findName(paramName)
        if index != -1:
            self.__envArray[index] = value
        else:
            return -1

    def incrAttr(self, paramName:str, value):
        """
        Add a value on a chosen environment attribute.\n
        :param paramName: The name of the attribute.
        :param value: The increased value.
        :return: nothing if success, otherwise return -1.
        """
        index = self.__ids.findName(paramName)
        if index != -1:
            self.__envArray[index] = value + self.__envArray[index]
        else:
            return -1

    def getCellNum(self):
        """

        :return: Current cell number.
        """
        return self.__currentCellNum

    def getMaxCellNum(self):
        """

        :return: Max cell number of your system.
        """
        return self.__maxCellNum
