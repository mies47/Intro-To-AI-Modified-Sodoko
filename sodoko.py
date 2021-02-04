import copy
class Cell:
    'A class for each cell of the sudoko table'
    def __init__(self, number:int, color:str, numberValues:list, colorValues:list):
        self.number = number
        self.color = color
        self.numberDomain = numberValues
        self.colorDomain = colorValues


class State:
    'A class to keep track of cells of the table at any point of time'
    def __init__(self, cells:list):
        self.table = cells

def initialState(number:int, colors:list, inputData:list):
    cells = [[0 for i in range(number)] for j in range(number)] 

    for i in range(number):
        for j in range(number):
            num , color = splitNumColor(inputData[(i*j) + j])
            numberDomain = [k+1 for k in range(number)]
            colorDomain = copy.deepcopy(colors)
            if not num == -1:
                numberDomain = [num]
            if not color == '#':
                colorDomain = [color]
            cells[i][j] = Cell(num, color, numberDomain, colorDomain)

    return cells


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


x = initialState(3, ['r','g','b','y','p'], ['1#', '*b', '*#','*#', '3r', '*#','*g', '1#', '*#'])