from CellSystem import CellSystem
import ParaCellsError


def readSystemSettings(url: str):
    """
    The target file should give several parameters as the following format:

    initCellNum=100
    maxCellNum=200
    dT=0.25
    T0=0
    T1=1000

    And the first two parameters are required.

    :param url:Target file url.
    :return:initCellNum, maxCellNum, dT, T0, T1
    """
    dic = {}
    fp = open(url, 'r')
    lines = fp.readlines()
    for line in lines:
        line = line.rstrip("\n")
        line_list = line.split('=')
        dic[line_list[0]] = line_list[1]

    if dic.get('initCellNum') is not None:
        initCellNum = int(dic['initCellNum'])
    else:
        ParaCellsError.raiseError('Could not find required parameter: initCellNum.')
    if dic.get('maxCellNum') is not None:
        maxCellNum = int(dic['maxCellNum'])
    else:
        ParaCellsError.raiseError('Could not find required parameter: maxCellNum.')
    if dic.get('dT') is not None:
        dT = float(dic['dT'])
    else:
        dT = 0
    if dic.get('T0') is not None:
        T0 = float(dic['T0'])
    else:
        T0 = 0
    if dic.get('T1') is not None:
        T1 = float(dic['T1'])
    else:
        T1 = 0

    return initCellNum, maxCellNum, dT, T0, T1



