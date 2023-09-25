from CellSystem import CellSystem
from Cell import Cell
import SystemError
import numpy as np


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
        SystemError.raiseError('Could not find required parameter: initCellNum.')
    if dic.get('maxCellNum') is not None:
        maxCellNum = int(dic['maxCellNum'])
    else:
        SystemError.raiseError('Could not find required parameter: maxCellNum.')
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


def trace(system: CellSystem, saving_file: str, cellId: int, trace_attr: str, to_epoch: int = 0):
    current_ep = system.epoch
    current_id = int(cellId)
    cell_ids = system.getCellIds()
    index = cell_ids.findName(trace_attr)
    while current_ep > to_epoch:
        pool = np.load(saving_file + '/epoch' + str(current_ep) + '.npy')
        current_id = int(current_id)
        current_id = pool[current_id][index]
        current_ep -= 1

    return int(current_id)

