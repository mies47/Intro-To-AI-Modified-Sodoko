
class Cell:
    'A class for each cell of the sudoko table'
    def __init__(self, numColor:str, numberValues:int, colorValues:list):
        self.number , self.color = splitNumColor(numColor)
        self.numberDomain = numberValues
        self.colorDomain = colorValues


class State:
    'A class to keep track of cells of the table at any point of time'
    def __init__(self, cells:list):
        self.table = cells


def splitNumColor(numColor:str):
    num = 0
    color = ''
    if numColor.startswith('*'):
        num = -1
        color = numColor[-1]
    else:
        num = int(numColor[:-1])
        color = numColor[-1]
    return(num , color)
