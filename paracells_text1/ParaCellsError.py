import sys


# The specialized Exception of ParaCellSystem.
class ParaCellsError(BaseException):
    def __init__(self, message=None, file=None, line=None, isFromCUDA=None):

        if message is None or file is None or line is None or isFromCUDA is None:
            self.__message = None
        else:
            self.__err = "[ParaCells Error] "

            self.__message = self.__err + file + "(" + str(line) + "):" + message

    def __str__(self):
        return self.__message

    # def getMessage(self):
    #     return self.__message


def raiseError(msg):
    raise ParaCellsError(msg, __file__, sys._getframe().f_lineno, False)

