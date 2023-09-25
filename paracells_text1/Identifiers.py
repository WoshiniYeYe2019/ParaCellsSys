import ParaCellsError


# Identifiers is designed to manage the relationship between attributes' names and indexes.
# It enables user to access attribute's index using strings.
# It's basically invisible to the user.
class Identifiers:
    def __init__(self, names: list):
        self.__names = list()
        self.__names = [str(i) for i in names]

    def getNames(self):
        return self.__names

    def getNum(self):
        return len(self.__names)

    def addName(self, name: str):
        if name in self.__names:
            ParaCellsError.raiseError("This attribute name has existed!")
            return
        else:
            self.__names.append(name)
            return True

    def findName(self, name: str):
        if name in self.__names:
            return self.__names.index(name)
        else:
            return -1

