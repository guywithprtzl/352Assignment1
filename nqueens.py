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

def initialize(masterList, csp):
    initialMatrix = masterList[0]
    colCounts = masterList[1]
    leftDiagonalCounts = masterList[2]
    rightDiagonalCounts = masterList[3]
    masterList[4] = initializeListOfConflicts(masterList, csp)
    listOfConflicts = masterList[4]
    
    for i in range(0,csp): 
        initialMatrix.append(0) # set up all available rows
        colCounts.append(0)
        leftDiagonalCounts.append(0) # diagonalCounts need 2(csp)-1 spots 
        leftDiagonalCounts.append(0) # as there are that many diagonals
        rightDiagonalCounts.append(0) # for each spot in a "csp" size list we make 2 in the
        rightDiagonalCounts.append(0) # 2(csp)-1 sized lists
        
    leftDiagonalCounts.remove(0) # accounts for the "-1" part of 2(csp)-1
    rightDiagonalCounts.remove(0) 
        
    for row in range(0, csp): 
        
    print("++++++++++++++++++++++++++++++")
    print("Initial Matrix: ", initialMatrix)
    return initialMatrix

def bestSpot(queen, masterList, csp):
    listOfConflicts = masterList[4]
    min


def initializeConflictsByColumn(masterList, csp):
    conflictsByColumn = masterList[5]
    current = masterList[0]
    columnCounts = masterList[1]
    for column in range(0,csp):
        columnCount = columnCounts[column]
        for row in range(0, csp):
            conflictsByColumn.append(conflicts(row, masterList, csp))

    totalConflicts = 0
    totalQueensInConflict = 0
    return conflictsByColumn
    
def initializeConflictsByQueen(masterList, csp):
    conflictsByQueen = masterList[4]
    for queen in range(0,csp):
        conflictsByQueen.append(conflicts(queen, masterList, csp))
    #print("listOfConflicts:",listOfConflicts)
    totalConflicts = 0
    totalQueensInConflict = 0
    for i in conflictsByQueen:
        if i != 0:
            totalQueensInConflict += 1
            totalConflicts += i
    print("listOfConflicts Summed: ", totalConflicts)
    print("totalQueensInConflict: ", totalQueensInConflict)
    return conflictsByQueen


def conflicts(queen, masterList, csp):
    current = masterList[0]
    row = queen # for clarity
    column = current[row]
    totalConflicts = 0
    columnConflicts = masterList[1][column-1] - 1 # -1 conflict as that accounts for the current queen being in that position
    leftDiagConflicts = leftDiagonalConflicts(queen, masterList, csp) # don't need to subtract 1 conflict as that's accounted
    rightDiagConflicts = rightDiagonalConflicts(queen, masterList, csp) # for in the functions
    totalConflicts = columnConflicts + leftDiagConflicts + rightDiagConflicts
    return totalConflicts # returns the total number of conflicts for this queen, an int
    

# returns false if any of the 4 constraints have been violated for any of the queens
# returns true otherwise
def constraints(listOfConflicts):
    result = True
    for queen in listOfConflicts:
        if queen != 0:
            result = False
            break
    if result == True:
        print(result)
    return result

"""
Caution: big algorithm below
"""

def minConflicts(csp):
    masterList = [[],[],[],[],[],[]] # current, colCounts, LD, RD, conflictsByQueen, conflictsByColumn
    current = initialize(masterList,csp)
    #print("initialMatrix:", current)
    maxSteps = int(csp*4) #CHANGE THIS FOR THE LOVE OF GOD
    currentStep = 0
    while currentStep <= maxSteps:
        
        if constraints(listOfConflicts) == True:
            return current
        else:
            
                
    return current

"""
distributes the load from main to minConflicts
"""

def algoHandler(csp):
    attempts = 0
    attempt = []
    if csp <= 1000: #small
        attempts = 10
    elif csp > 1000 and csp <= 100000: #medium
        attempts = 5
    elif csp > 100000 and csp <= 10000000: # large
        attempts = 3
    else:
        print (csp, " does not fit in any of the specified ranges.")

    for i in range(0,attempts):
        print("attempt #:", i+1)
        if i == 0:
            attempt = minConflicts(csp)
        else:
            print("=========================================================")
            attempt = minConflicts(csp)
        
        solutionMaybe = initializeListOfConflicts(attempt, csp)
        
        if constraints(solutionMaybe) == True:
            break
        
    return attempt


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
Utility Function
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
    leftDiagonalIndex = (csp-1) - (row - column)
    leftDiagonalConflicts = leftDiagonalCounts[leftDiagonalIndex] - 1 # don't count the current queen as a conflict
    return leftDiagonalConflicts # for this queen, returns an int

def rightDiagonalConflicts(queen, masterList, csp):
    current = masterList[0]
    row = queen # for clarity
    column = current[row]
    rightDiagonalCounts = masterList[3]
    rightDiagonalIndex = (row + column - 1) -1 # extra minus 1 because we are using 0 based lists
    rightDiagonalConflicts = rightDiagonalCounts[rightDiagonalIndex] - 1 # don't count the current queen as a conflict
    return rightDiagonalConflicts # for this queen, returns an int

"""
Timing Functions
"""
