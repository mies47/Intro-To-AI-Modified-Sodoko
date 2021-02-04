import copy
import math
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


def isComplete(state: list):
    'Check to see if all variables are assigned'
    for row in state:
        for col in row:
            if col.num == -1 or col.color == '#':
                return False
    
    return True

def MRV(state: list):
    'Minimum Remaining Value Heuristic'
    minimum = math.inf
    for row in state:
        for col in row:
            if minimum > len(col.numberDomain) * len(col.colorDomain):
                minimum = len(col.numberDomain) * len(col.colorDomain)
    
    return minimum

def checkRowConstraint(state: list, row:int):
    num = 0
    for i in state[row]:
        if i.number == -1:
            num += 1
    
    return num

def checkColumnConstraint(state: list, column:int):
    num = 0
    for i in state:
        if i[column].number == -1:
            num += 1

    return num

def checkColorConstraint(state: list, row: int, column: int):
    num = 0
    if row - 1 > 0 and state[row - 1][column].color == '#':
        num += 1
    if column - 1 > 0 and state[row][column -1].color == '#':
        num += 1
    if row + 1 < len(state) and state[row + 1][column].color == '#':
        num += 1
    if column + 1 < len(state) and state[row][column + 1].color == '#':
        num += 1

    return num

def degree(state: list):
    'Returns a cell with minimum remaining value and most constraints with unassigned variables'
    minimum = MRV(state)
    maximumConstraint = -1
    maximumRow , maximumCol = 0, 0
    for row in len(state):
        for col in len(row):
            if minimum == len(state[row][col].numberDomain) * len(state[row][col].colorDomain):
                constraints = checkRowConstraint(state, row) + checkColumnConstraint(state, col) + checkColorConstraint(state, row, col)
                if constraints > maximumConstraint:
                    maximumConstraint = constraints
                    maximumRow = row
                    maximumCol = col

    return (maximumRow , maximumCol)



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