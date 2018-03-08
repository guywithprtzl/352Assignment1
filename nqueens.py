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
import copy

def initialize(masterList, csp):
    initialMatrix = masterList[0]
    colCounts = masterList[1]
    leftDiagonalCounts = masterList[2]
    rightDiagonalCounts = masterList[3]
    emptyColumns = masterList[4]

    
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
    



##    print("current: ", masterList[0])
##    print("colCounts: ", masterList[1])
##    print("leftDiagonals: ", masterList[2])
##    print("rightDiagonals: ", masterList[3])
##    print("emptyColumns: ", masterList[4])

        
    for row in range(0, csp): 
        bestCol = bestColumn(row, masterList, csp)
        initialMatrix[row] = bestCol
        if bestCol in emptyColumns:
            emptyColumns.remove(bestCol)
##        print("current: ", masterList[0])
##        print("colCounts: ", masterList[1])
##        print("leftDiagonals: ", masterList[2])
##        print("rightDiagonals: ", masterList[3])
##        print("emptyColumns: ", masterList[4])
        #masterList = updateConflicts(masterList, row, bestCol, 0, csp)
        

##        print("current: ", masterList[0])
##        print("colCounts: ", masterList[1])
##        print("leftDiagonals: ", masterList[2])
##        print("rightDiagonals: ", masterList[3])
##        print("emptyColumns: ", masterList[4])
##    print("++++++++++++++++++++++++++++++")
##    print("Initial Matrix: ", initialMatrix)
    return masterList

def updateConflicts(masterList, row, newColumn, oldColumn, csp):
    colCounts = masterList[1]
    leftDiagonalCounts = masterList[2]
    rightDiagonalCounts = masterList[3]
    emptyColumns = masterList[4]


    #update new conflicts
    colCounts[newColumn-1] += 1
    leftDiagonalCounts[(csp-1)-(row-(newColumn-1))] += 1
    rightDiagonalCounts[row + (newColumn - 1)] += 1

    if (oldColumn != 0):
        #update old conflicts if not initializing
        #print("here--------------")
        colCounts[oldColumn-1] -= 1
        leftDiagonalCounts[(csp-1)-(row-(oldColumn-1))] -= 1
        rightDiagonalCounts[row + (oldColumn - 1)] -= 1
        if colCounts[oldColumn-1] == 0:
            emptyColumns.append(oldColumn)
            


    return masterList
    
def updateConflictsHypothetical(masterList, row, newColumn, oldColumn, csp):
    colCounts = masterList[1]
    leftDiagonalCounts = masterList[2]
    rightDiagonalCounts = masterList[3]
    emptyColumns = masterList[4]

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

    return masterList
    

def bestColumn(queen, masterList, csp):
    emptyColumns = masterList[4]
    originalColumn = int(masterList[0][queen])
    bestColumn = emptyColumnChecker(queen, masterList, csp, originalColumn)
    if  bestColumn == -1:
        # there isn't a column with zero conflict
        bestColumn = randomColumnChecker(queen, masterList, csp, originalColumn)
        if bestColumn == -1:
            # there isn't a column with a single conflict that could be found randomly
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
        #print("queen in question(index):",queen," | hypotheticalMatrix:", initialMatrix," | columnConflicts:",columnConflicts)
        if columnConflicts == 0:
            #print("emptyColumnChecker || queen in question(index):",queen," | hypotheticalMatrix:", initialMatrix," | columnConflicts:",columnConflicts)
            #initialMatrix[queen] = originalColumn
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

        #if column != originalColumn:
            initialMatrix[queen] = column

            #######
            masterList = updateConflictsHypothetical(masterList, queen, column, previousColumn, csp)
            #######
            # print("current: ", masterList[0])
            # print("colCounts: ", masterList[1])
            # print("leftDiagonals: ", masterList[2])
            # print("rightDiagonals: ", masterList[3])
            # print("emptyColumns: ", masterList[4])
        
            columnConflicts = conflicts(queen, masterList, csp)
            #print("conflicts for current queen: ", columnConflicts)
            if columnConflicts == 1:
                #print("randomColumnChecker || queen in question(index):",queen," | hypotheticalMatrix:", initialMatrix," | columnConflicts:",columnConflicts)
                #initialMatrix[queen] = originalColumn
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
        #if column != originalColumn:
            initialMatrix[queen] = column

            #######
            masterList = updateConflictsHypothetical(masterList, queen, column, previousColumn, csp)
            #######
        
            columnConflicts = conflicts(queen, masterList, csp)
            if columnConflicts == 1:
                #print("seanSaysWeAreCheckingAllSquares || queen in question(index):",queen," | hypotheticalMatrix:", initialMatrix," | columnConflicts:",columnConflicts)
                #initialMatrix[queen] = originalColumn
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
    #print("conflicts row: ", row)
    column = current[row]
    totalConflicts = 0
    columnConflicts = masterList[1][column-1] # -1 conflict as that accounts for the current queen being in that position
    leftDiagConflicts = leftDiagonalConflicts(queen, masterList, csp) # don't need to subtract 1 conflict as that's accounted
    rightDiagConflicts = rightDiagonalConflicts(queen, masterList, csp) # for in the functions
    totalConflicts = (columnConflicts + leftDiagConflicts + rightDiagConflicts) - 3
    #print(totalConflicts)
    return totalConflicts # returns the total number of conflicts for this queen, an int
    

# returns false if any of the 4 constraints have been violated for any of the queens
# returns true otherwise
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

"""
Caution: big algorithm below
"""
# NOTES:
    # 1. Choose queen for repair
    # 2. How to check if board is solved? <- Sean wants to know
def minConflicts(csp):
    masterList = [[],[],[],[],[]] # current, colCounts, LD, RD, emptyColumns
    masterList = initialize(masterList, csp)
    current = masterList[0]
    colCounts = masterList[1]
    leftDiagonalCounts = masterList[2]
    rightDiagonalCounts = masterList[3]
    emptyColumns = masterList[4]
    #print("initialMatrix:", current)
    #print("initialEmptyColumns:", emptyColumns)
    maxSteps = csp #CHANGE THIS FOR THE LOVE OF GOD
    currentStep = 0
    changed = True # start with this as true to allow constraints to check if the initial board is correct
    while currentStep <= maxSteps:
##        print("current: ", masterList[0])
##        print("colCounts: ", masterList[1])
##        print("leftDiagonals: ", masterList[2])
##        print("rightDiagonals: ", masterList[3])
##        print("emptyColumns: ", masterList[4])
        if changed: # constrains below so that it's only called if necessary
            if constraints(masterList) == True:
                print("currentStep is: ", currentStep)
                return masterList
            
        queenToRepair = random.randint(0,csp-1)
        if conflicts(queenToRepair, masterList, csp) != 0:
            # we want to repair this queen
            changed = True
            oldColumn = current[queenToRepair]
            #print("in minConflict, just before bestCol is called, oldColumn is: ", oldColumn)
            bestCol = bestColumn(queenToRepair, masterList, csp)
            #print("minConflict, just after bestCol is called, bestCol is: ", bestCol)
            current[queenToRepair] = bestCol
            if bestCol in emptyColumns:
                emptyColumns.remove(bestCol)
            if colCounts[oldColumn-1] == 0:
                emptyColumns.append(oldColumn)
            
            #masterList = updateConflicts(masterList, queenToRepair, bestCol, oldColumn, csp)
            currentStep += 1
        else:
            changed = False
                
    return masterList

"""
distributes the load from main to minConflicts
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
        # print("current: ", attemptMasterList[0])
        # print("colCounts: ", attemptMasterList[1])
        # print("leftDiagonals: ", attemptMasterList[2])
        # print("rightDiagonals: ", attemptMasterList[3])
        # print("emptyColumns: ", attemptMasterList[4])
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

"""
#################
Utility Functions
#################
"""

"""
mostConflicts takes in listOfConflicts and csp and returns the queen with the most conflicts
"""

def mostConflicts(listOfConflicts, csp):
    queen = 0
    maxConflicts = listOfConflicts[queen] # initially, first queen has the max number of conflicts
    currentQueen = 0
    while currentQueen < csp:
        if listOfConflicts[currentQueen] > maxConflicts:
            queen = currentQueen
        currentQueen += 1
    return queen


def leftDiagonalConflicts(queen, masterList, csp):
    current = masterList[0]
    row = queen # for clarity
    column = current[row]
    leftDiagonalCounts = masterList[2]
    leftDiagonalIndex = (csp-1) - (row - (column-1) ) #-1
    #print("row: ", row, " col: ", column, " ld index: ", leftDiagonalIndex)
    leftDiagonalConflicts = leftDiagonalCounts[leftDiagonalIndex] # don't count the current queen as a conflict
    return leftDiagonalConflicts # for this queen, returns an int

def rightDiagonalConflicts(queen, masterList, csp):
    current = masterList[0]
    row = queen # for clarity
    column = current[row]
    rightDiagonalCounts = masterList[3]
    rightDiagonalIndex = (row + (column - 1)) # extra minus 1 because we are using 0 based lists
    rightDiagonalConflicts = rightDiagonalCounts[rightDiagonalIndex] # don't count the current queen as a conflict
    return rightDiagonalConflicts # for this queen, returns an int

"""
Timing Functions
"""
main()

def paramChanger(bob):
    bobby = list(bob[0])
    bobby[0] = 99
    return 1
