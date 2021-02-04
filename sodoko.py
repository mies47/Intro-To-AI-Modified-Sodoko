import copy
class Cell:
    'A class for each cell of the sudoko table'
    def __init__(self, number:int, color:str, numberValues:list, colorValues:list):
        self.number = number
        self.color = color
        self.numberDomain = numberValues
        self.colorDomain = colorValues


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


def backtrack(state: list):
    if(isComplete(state)):
        return state
    
    cellRow, cellCol = unassignedCell(state)
    cell = state[cellRow][cellCol]

    for num in cell.numberDomain:
        for color in cell.colorDomain:
            if checkValid(state, cellRow, cellCol, num, color):
                newState = copy.deepcopy(state)
                newState = assignValue(newState, num, color)
                result = backtrack(newState)
                if not result == 'failure':
                    return result

    return 'failure' 

x = initialState(3, ['r','g','b','y','p'], ['1#', '*b', '*#','*#', '3r', '*#','*g', '1#', '*#'])