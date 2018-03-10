"""
############################
############################
CISC 352 Assignment 1
nqueens.py
Sean Tippett - 10108181
Heni Virag - 10142490
############################
############################
"""
import random
import time

totalTimeInRandomCol = 0
totalTimeInUpdateCon = 0
totalTimeInEmptyCol = 0

def initialize(masterList, csp):
    global totalTimeInRandomCol
    global totalTimeInUpdateCon
    global totalTimeInEmptyCol
    initialMatrix = masterList[0]
    colCounts = masterList[1]
    leftDiagonalCounts = masterList[2]
    rightDiagonalCounts = masterList[3]
    emptyColumns = masterList[4]

    startTimePREINIT = time.time()
    
    for i in range(0,csp): 
        initialMatrix.append(0) # set up all available rows
        colCounts.append(0)
        leftDiagonalCounts.append(0) # diagonalCounts need 2(csp)-1 spots 
        leftDiagonalCounts.append(0) # as there are that many diagonals
        rightDiagonalCounts.append(0) # for each spot in a "csp" size list we make 2 in the
        rightDiagonalCounts.append(0) # 2(csp)-1 sized lists
        emptyColumns.append(i+1)
        
    leftDiagonalCounts.remove(0) # accounts for the "-1" part of 2(csp)-1
    rightDiagonalCounts.remove(0)
    
    endTimePREINIT = time.time()

    print("Pre-initialization time was %g seconds" % (endTimePREINIT - startTimePREINIT))
    random.shuffle(emptyColumns)
    for row in range(0, csp): 
        bestCol = bestColumn(row, masterList, csp)
        initialMatrix[row] = bestCol
        if bestCol in emptyColumns:
            emptyColumns.remove(bestCol)

    print("Total time in randomColumnChecker: ", (totalTimeInRandomCol))
    print("Total time in emptyColumnChecker: ", (totalTimeInEmptyCol))
    print("Total time in updateConflictsHypothetical: ", totalTimeInUpdateCon)

    return masterList


def updateConflictsHypothetical(masterList, row, newColumn, oldColumn, csp):
    global totalTimeInUpdateCon
    startTimeUCH = time.time()
    colCounts = masterList[1]
    leftDiagonalCounts = masterList[2]
    rightDiagonalCounts = masterList[3]

    if newColumn != 0:
    #update new conflicts
        colCounts[newColumn-1] += 1
        leftDiagonalCounts[(csp-1)-(row-(newColumn-1))] += 1
        rightDiagonalCounts[row + (newColumn - 1)] += 1

    if (oldColumn != 0):
    #update new conflicts
        colCounts[oldColumn-1] -= 1
        leftDiagonalCounts[(csp-1)-(row-(oldColumn-1))] -= 1
        rightDiagonalCounts[row + (oldColumn - 1)] -= 1
    endTimeUCH = time.time()
    totalTimeInUpdateCon += endTimeUCH - startTimeUCH

    return masterList
    

def bestColumn(queen, masterList, csp):
    global totalTimeInRandomCol
    global totalTimeInEmptyCol
    originalColumn = int(masterList[0][queen])
    startTimeECC = time.time()
    bestColumn = emptyColumnChecker(queen, masterList, csp, originalColumn)
    endTimeECC = time.time()
    totalTimeInEmptyCol += (endTimeECC - startTimeECC)
    if bestColumn == -1:
        # there isn't a column with zero conflict
        startTimeRCC = time.time()
        bestColumn = randomColumnChecker(queen, masterList, csp, originalColumn)
        endTimeRCC = time.time()
        totalTimeInRandomCol += (endTimeRCC - startTimeRCC)
        if bestColumn == -1:
            # there isn't a column with a single conflict that could be found randomly
            print("Column can't be found randomly in bestColumn")
            bestColumn = seanSaysWeAreCheckingAllSquares(queen, masterList, csp, originalColumn)
            return bestColumn
        else:
            return bestColumn
    else:
        return bestColumn


def emptyColumnChecker(queen, masterList, csp, originalColumn):
    initialMatrix = masterList[0]
    emptyColumns = masterList[4]
    previousColumn = originalColumn
    for column in emptyColumns:
        initialMatrix[queen] = column

        #######
        masterList = updateConflictsHypothetical(masterList, queen, column, previousColumn, csp)
        #######
        
        columnConflicts = conflicts(queen, masterList, csp)
        if columnConflicts == 0:
            return column
        previousColumn = column
        
    initialMatrix[queen] = originalColumn
    
    #######
    masterList = updateConflictsHypothetical(masterList, queen, originalColumn, previousColumn, csp)
    #######

    return -1


def randomColumnChecker(queen, masterList, csp, originalColumn):
    initialMatrix = masterList[0]
    k = 100
    previousColumn = originalColumn
    if csp <= 100:
        k = int(csp) # reset
    randomColumnsList = random.sample(range(1, csp+1), k)


    for column in randomColumnsList:
        initialMatrix[queen] = column

        #######
        masterList = updateConflictsHypothetical(masterList, queen, column, previousColumn, csp)
        #######

        columnConflicts = conflicts(queen, masterList, csp)
        if columnConflicts == 1:
            return column
        previousColumn = column

    initialMatrix[queen] = originalColumn
    
    #######
    masterList = updateConflictsHypothetical(masterList, queen, originalColumn, column, csp)
    #######
    
    return -1


def seanSaysWeAreCheckingAllSquares(queen, masterList, csp, originalColumn):
    initialMatrix = masterList[0]
    previousColumn = originalColumn

    for column in range(1, csp+1):
        initialMatrix[queen] = column

        #######
        masterList = updateConflictsHypothetical(masterList, queen, column, previousColumn, csp)
        #######
        
        columnConflicts = conflicts(queen, masterList, csp)
        if columnConflicts == 1:
            return column
        previousColumn = column
        
    initialMatrix[queen] = originalColumn

    #######
    masterList = updateConflictsHypothetical(masterList, queen, originalColumn, previousColumn, csp)
    #######
    
    return initialMatrix[queen]


def conflicts(queen, masterList, csp):
    current = masterList[0]
    row = queen # for clarity
    column = current[row]
    totalConflicts = 0
    columnConflicts = masterList[1][column-1] # -1 conflict as that accounts for the current queen being in that position
    leftDiagConflicts = leftDiagonalConflicts(queen, masterList, csp) # don't need to subtract 1 conflict as that's accounted
    rightDiagConflicts = rightDiagonalConflicts(queen, masterList) # for in the functions
    totalConflicts = (columnConflicts + leftDiagConflicts + rightDiagConflicts) - 3
    return totalConflicts # returns the total number of conflicts for this queen, an int
    

# returns false if any of the 4 constraints have been violated for any of the queens, true otherwise
def constraints(masterList):
    colCounts = list(masterList[1])
    leftDiagonalCounts = list(masterList[2])
    rightDiagonalCounts = list(masterList[3])

    result = True
    colCounts.sort()
    colCounts.reverse()
    for c in colCounts:
        if c > 1:
            return False
    leftDiagonalCounts.sort()
    leftDiagonalCounts.reverse()
    for ld in leftDiagonalCounts:
        if ld > 1:
            return False
    rightDiagonalCounts.sort()
    rightDiagonalCounts.reverse()
    for rd in rightDiagonalCounts:
        if rd > 1:
            return False
    if result == True:
        print("--------------------------SOLVED--------------------------")
    return result


def minConflicts(csp):
    global totalTimeInUpdateCon
    totalTimeInUpdateCon = 0
    global totalTimeInRandomCol
    totalTimeInRandomCol = 0
    global totalTimeInEmptyCol
    totalTimeInEmptyCol = 0
    startTimeINIT = time.time()
    masterList = [[],[],[],[],[]] # current, colCounts, LD, RD, emptyColumns
    masterList = initialize(masterList, csp)
    endTimeINIT = time.time()
    print("Initialization time was %g seconds" % (endTimeINIT - startTimeINIT))
    current = masterList[0]
    colCounts = masterList[1]
    leftDiagonalCounts = masterList[2]
    rightDiagonalCounts = masterList[3]
    emptyColumns = masterList[4]
    maxSteps = csp

    if csp < 1000:
        maxSteps = 1000
    
    currentStep = 0
    changed = True # start with this as true to allow constraints to check if the initial board is correct
    listOfQueensUnmoved = random.sample(range(0, csp), csp)
    listOfQueensMoved = []
    queensLeft = csp
    queenToRepair = 0
    cantFindAQueen = 0
    startTimeREPAIR = time.time()

    while currentStep <= maxSteps:
        if changed: # constrains below so that it's only called if necessary
            if constraints(masterList) == True:
                endTimeREPAIR = time.time()
                print("currentStep is: ", currentStep)
                print("Repair time was %g seconds" % (endTimeREPAIR - startTimeREPAIR))
                
                return masterList

        if csp > 500:
            queenToRepair = listOfQueensUnmoved[random.randint(0,queensLeft-1)]
        else:
            queenToRepair = random.randint(0,csp-1)
            
        if conflicts(queenToRepair, masterList, csp) != 0:
            # we want to repair this queen
            changed = True
            oldColumn = current[queenToRepair]
            bestCol = bestColumn(queenToRepair, masterList, csp)
            
            if csp > 500:
                while legalMove(queenToRepair, listOfQueensMoved, bestCol, masterList, csp) == False:
                    bestCol = bestColumn(queenToRepair, masterList, csp)

            current[queenToRepair] = bestCol
            if bestCol in emptyColumns:
                emptyColumns.remove(bestCol)
            if colCounts[oldColumn-1] == 0:
                emptyColumns.append(oldColumn)
            
            currentStep += 1
            cantFindAQueen = 0

            if csp > 500:
                queensLeft -= 1
                listOfQueensUnmoved.remove(queenToRepair)
                listOfQueensMoved.append(queenToRepair)
        else:
            cantFindAQueen += 1
            changed = False
                
    return masterList


"""
Distributes the load from main to minConflicts
"""
def algoHandler(csp):
    attempts = 0
    attempt = []
    if csp <= 1000: #small
        attempts = 10
    elif csp > 1000 and csp <= 100000: #medium
        attempts = 20
    elif csp > 100000 and csp <= 10000000: # large
        attempts = 3
    else:
        print (csp, " does not fit in any of the specified ranges.")

    for i in range(0,attempts):
        print("attempt #:", i+1)
        print("=========================================================")
        print("=========================================================")
        print("=========================================================")
        print("=========================================================")
        attemptMasterList = minConflicts(csp)
        print("=========================================================")
        print("=========================================================")
        print("=========================================================")
        if constraints(attemptMasterList) == True:
            break
        
    return attemptMasterList[0]


def main():
    solutions = []
    with open("nqueens.txt", "r") as f:
        for line in f:
            cspAsString = line.rstrip()
            csp = int(cspAsString)
            print(csp)
            startTime = time.time()
            solutions.append(algoHandler(csp))
            endTime = time.time()
            print("Elapsed time was %g seconds" % (endTime - startTime))
            print("-----------------------------------------------------------------")
            print("-----------------------------------------------------------------")
    solutionsAsString = []
    
    for solution in solutions:
        solutionsAsString.append(str(solution))
        
    with open("nqueens_out.txt", "w") as f:
        f.write('\n'.join(solutionsAsString))


def leftDiagonalConflicts(queen, masterList, csp):
    current = masterList[0]
    row = queen # for clarity
    column = current[row]
    leftDiagonalCounts = masterList[2]
    leftDiagonalIndex = (csp-1) - (row - (column-1) )
    leftDiagonalConflicts = leftDiagonalCounts[leftDiagonalIndex] # don't count the current queen as a conflict
    return leftDiagonalConflicts # for this queen, returns an int


def rightDiagonalConflicts(queen, masterList):
    current = masterList[0]
    row = queen # for clarity
    column = current[row]
    rightDiagonalCounts = masterList[3]
    rightDiagonalIndex = (row + (column - 1)) # extra minus 1 because we are using 0 based lists
    rightDiagonalConflicts = rightDiagonalCounts[rightDiagonalIndex] # don't count the current queen as a conflict
    return rightDiagonalConflicts # for this queen, returns an int


def legalMove(queenToRepair, queensMoved, potentialColumn, masterList, csp):
    current = masterList[0]
    for movedQueen in queensMoved:
        movedQueenCol = current[movedQueen]
        if potentialColumn == movedQueenCol:
            return False
        else:
            leftDiagIndexMovedQueen = (csp-1) - (movedQueen - (movedQueenCol-1) )
            leftDiagIndexQueenToRepair = (csp-1) - (queenToRepair - (potentialColumn-1) )
            if leftDiagIndexMovedQueen == leftDiagIndexQueenToRepair:
                return False
            else:
                rightDiagIndexMovedQueen = (movedQueen + (movedQueenCol - 1))
                rightDiagIndexQueenToRepair = (queenToRepair + (potentialColumn - 1))
                if rightDiagIndexMovedQueen == rightDiagIndexQueenToRepair:
                    return False
    return True


main()