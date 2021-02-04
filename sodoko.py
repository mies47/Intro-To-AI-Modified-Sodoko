import copy
import math

allColors = {}
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
            num , color = splitNumColor(inputData[(i*number) + j])
            numberDomain = [k+1 for k in range(number)]
            colorDomain = copy.deepcopy(colors)
            if not num == -1:
                numberDomain = [num]
            if not color == '#':
                colorDomain = [color]
            cells[i][j] = Cell(num, color, numberDomain, colorDomain)

    for i in range(len(colors)):
        allColors[colors[i]] = i
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
            if col.number == -1 or col.color == '#':
                return False
    
    return True

def MRV(state: list):
    'Minimum Remaining Value Heuristic'
    minimum = math.inf
    for row in state:
        for col in row:
            if not(len(col.numberDomain) == 1 and len(col.colorDomain) == 1) and minimum > len(col.numberDomain) * len(col.colorDomain):
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
    if row - 1 >= 0 and state[row - 1][column].color == '#':
        num += 1
    if column - 1 >= 0 and state[row][column -1].color == '#':
        num += 1
    if row + 1 < len(state) and state[row + 1][column].color == '#':
        num += 1
    if column + 1 < len(state) and state[row][column + 1].color == '#':
        num += 1

    return num

def degree(state: list):
    'Returns a cell row and column with minimum remaining value and most constraints with unassigned variables'
    minimum = MRV(state)
    maximumConstraint = -1
    maximumRow , maximumCol = 0, 0
    for row in range(len(state)):
        for col in range(len(state)):
            if minimum == len(state[row][col].numberDomain) * len(state[row][col].colorDomain):
                constraints = checkRowConstraint(state, row) + checkColumnConstraint(state, col) + checkColorConstraint(state, row, col)
                if constraints > maximumConstraint:
                    maximumConstraint = constraints
                    maximumRow = row
                    maximumCol = col

    return (maximumRow , maximumCol)

def checkValid(state:list , cellRow:int , cellCol:int , num:int, color:str):
    '''Checks and returns if the chosen number and color values are valid for assigning based on
    Row and Column repetition and color priority of its neighbors'''
    for col in range(len(state)):
        if col != cellCol and state[cellRow][col].number == num:
            return False
    for row in range(len(state)):
        if row != cellRow and state[row][cellCol].number == num:
            return False
    if cellRow - 1 >= 0 and not state[cellRow - 1][cellCol].color == '#':
        if state[cellRow - 1][cellCol].color == color:
            return False
        if ((allColors[color] < allColors[state[cellRow - 1][cellCol].color] and num < state[cellRow - 1][cellCol].number)
            or (allColors[color] > allColors[state[cellRow - 1][cellCol].color] and num > state[cellRow - 1][cellCol].number)):
            return False

    if cellRow + 1 < len(state) and not state[cellRow + 1][cellCol].color == '#':
        if state[cellRow + 1][cellCol].color == color:
            return False
        if ((allColors[color] < allColors[state[cellRow + 1][cellCol].color] and num < state[cellRow + 1][cellCol].number)
            or (allColors[color] > allColors[state[cellRow + 1][cellCol].color] and num > state[cellRow + 1][cellCol].number)):
            return False

    if cellCol - 1 >= 0 and not state[cellRow][cellCol - 1].color == '#':
        if state[cellRow][cellCol - 1].color == color:
            return False
        if ((allColors[color] < allColors[state[cellRow][cellCol - 1].color] and num < state[cellRow][cellCol - 1].number)
            or (allColors[color] > allColors[state[cellRow][cellCol - 1].color] and num > state[cellRow][cellCol - 1].number)):
            return False

    if cellCol + 1 < len(state) and not state[cellRow][cellCol + 1].color == '#':
        if state[cellRow][cellCol - 1].color == color:
            return False
        if ((allColors[color] < allColors[state[cellRow][cellCol + 1].color] and num < state[cellRow][cellCol + 1].number)
            or (allColors[color] > allColors[state[cellRow][cellCol + 1].color] and num > state[cellRow][cellCol + 1].number)):
            return False

    return True
    

def numberFC(state: list, row: int, col: int, number: int):
    'Forward Checking to remove invalid values from cells in the same row and column numberDomain'
    for i in state[row]:
        if number in i.numberDomain:
            i.numberDomain.remove(number)
    
    for i in state:
        if number in i[col].numberDomain:
            i[col].numberDomain.remove(number)

    return state

def colorFC(state: list, row: int, col: int, number: int, color: str):
    #top cell
    if row - 1 >= 0 and color in state[row - 1][col].colorDomain:
        state[row - 1][col].colorDomain.remove(color)
    if row - 1 >= 0 and state[row - 1][col].color == '#' and state[row - 1][col].number != -1:
        if state[row - 1][col].number > number:
            for colorItem , priority in allColors.items():
                if(allColors[color] < priority):
                    state[row - 1][col].colorDomain.remove(colorItem)
        else:
            for colorItem , priority in allColors.items():
                if(allColors[color] > priority):
                    state[row - 1][col].colorDomain.remove(colorItem)
    elif row - 1 >= 0 and state[row - 1][col].color != '#' and state[row - 1][col].number == -1:
        if allColors[state[row - 1][col].color] < allColors[color]:
            for i in range(len(state[row - 1][col].numberDomain)):
                if state[row - 1][col].numberDomain[i] < number:
                    state[row - 1][col].numberDomain.pop(i)
        else:
            for i in range(len(state[row - 1][col].numberDomain)):
                if state[row - 1][col].numberDomain[i] > number:
                    state[row - 1][col].numberDomain.pop(i)
    #bottom cell
    if row + 1 < len(state) and color in state[row + 1][col].colorDomain:
        state[row + 1][col].colorDomain.remove(color)
    if row + 1 < len(state) and state[row + 1][col].color == '#' and state[row + 1][col].number != -1:
        if state[row + 1][col].number > number:
            for colorItem , priority in allColors.items():
                if(allColors[color] < priority):
                    state[row + 1][col].colorDomain.remove(colorItem)
        else:
            for colorItem , priority in allColors.items():
                if(allColors[color] > priority):
                    state[row + 1][col].colorDomain.remove(colorItem)
    elif row + 1 < len(state) and state[row + 1][col].color != '#' and state[row + 1][col].number == -1:
        if allColors[state[row + 1][col].color] < allColors[color]:
            for i in range(len(state[row + 1][col].numberDomain)):
                if state[row + 1][col].numberDomain[i] < number:
                    state[row + 1][col].numberDomain.pop(i)
        else:
            for i in range(len(state[row + 1][col].numberDomain)):
                if state[row + 1][col].numberDomain[i] > number:
                    state[row + 1][col].numberDomain.pop(i)
    #left cell
    if col - 1 >= 0 and color in state[row][col - 1].colorDomain:
        state[row][col - 1].colorDomain.remove(color)
    if col - 1 >= 0 and state[row][col - 1].color == '#' and state[row][col - 1].number != -1:
        if state[row][col - 1].number > number:
            for colorItem , priority in allColors.items():
                if(allColors[color] < priority):
                    state[row][col - 1].colorDomain.remove(colorItem)
        else:
            for colorItem , priority in allColors.items():
                if(allColors[color] > priority):
                    state[row][col - 1].colorDomain.remove(colorItem)
    elif col - 1 >= 0 and state[row][col - 1].color != '#' and state[row][col - 1].number == -1:
        if allColors[state[row][col - 1].color] < allColors[color]:
            for i in range(len(state[row][col - 1].numberDomain)):
                if state[row][col - 1].numberDomain[i] < number:
                    state[row][col - 1].numberDomain.pop(i)
        else:
            for i in range(len(state[row][col - 1].numberDomain)):
                if state[row][col - 1].numberDomain[i] > number:
                    state[row][col - 1].numberDomain.pop(i)
    #right cell
    if col + 1 < len(state) and color in state[row][col + 1].colorDomain:
        state[row][col + 1].colorDomain.remove(color)
    if col + 1 < len(state) and state[row][col + 1].color == '#' and state[row][col + 1].number != -1:
        if state[row][col + 1].number > number:
            for colorItem , priority in allColors.items():
                if(allColors[color] < priority):
                    state[row][col + 1].colorDomain.remove(colorItem)
        else:
            for colorItem , priority in allColors.items():
                if(allColors[color] > priority):
                    state[row][col + 1].colorDomain.remove(colorItem)
    elif col + 1 < len(state) and state[row][col + 1].color != '#' and state[row][col + 1].number == -1:
        if allColors[state[row][col + 1].color] < allColors[color]:
            for i in range(len(state[row][col + 1].numberDomain)):
                if state[row][col + 1].numberDomain[i] < number:
                    state[row][col + 1].numberDomain.pop(i)
        else:
            for i in range(len(state[row][col + 1].numberDomain)):
                if state[row][col + 1].numberDomain[i] > number:
                    state[row][col + 1].numberDomain.pop(i)

    return state

def assignValue(state: list, row: int, col: int, num: int, color: str):
    state = numberFC(state, row, col, num)
    state = colorFC(state, row, col, num ,color)
    state[row][col].number = num
    state[row][col].color = color
    state[row][col].numberDomain = [num]
    state[row][col].colorDomain = [color]
    return state


def backtrack(state: list):
    if(isComplete(state)):
        return state
    
    cellRow, cellCol = degree(state)
    cell = state[cellRow][cellCol]

    if cell.number == -1 and cell.color == '#':
        for num in cell.numberDomain:
            for color in cell.colorDomain:
                if checkValid(state, cellRow, cellCol, num, color):
                    newState = copy.deepcopy(state)
                    newState = assignValue(newState,cellRow, cellCol, num, color)
                    result = backtrack(newState)
                    if not result == 'failure':
                        return result
    elif cell.number == -1:
        for num in cell.numberDomain:
            if checkValid(state, cellRow, cellCol, num, cell.color):
                newState = copy.deepcopy(state)
                newState = assignValue(newState,cellRow, cellCol, num, cell.color)
                result = backtrack(newState)
                if not result == 'failure':
                    return result
    else:
        for color in cell.colorDomain:
            if checkValid(state, cellRow, cellCol, cell.number, color):
                newState = copy.deepcopy(state)
                newState = assignValue(newState,cellRow, cellCol, cell.number, color)
                result = backtrack(newState)
                if not result == 'failure':
                    return result

    return 'failure' 

x = initialState(3, ['r','g','b','y','p'], ['*#', '*#', '*#','*#', '*#', '*#','*#', '*#', '*#'])
result = backtrack(x)
if result == 'failure':
    print(result)
else:
    for row in result:
        for col in row:
            print("%d%s " % (col.number , col.color), end="")
        print()