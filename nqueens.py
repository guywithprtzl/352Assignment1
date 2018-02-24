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

def initialize(csp):
    initialMatrix = []
    availableColumns = []
    
    for i in range(1,csp+1): # column count starts at 1
        availableColumns.append(i)
        initialMatrix.append(0) # set up all available rows
        
    random.shuffle(availableColumns)
    #print("availableColumns:", availableColumns)
    for row in range(0, csp): # looking at indices now so range is back to normal
        #go through the initial matrix starting at row 0 and decide which of the available columns
        #cause the least number of conflicts
        #print("=====================")
        #print("initialMatrix:",initialMatrix)
        
        minConflicts = csp # impossible to have more conflicts than there are queens
        minConflictsColumn = 0 # keep track of which column has the least number of conflicts
        availableTestColumns = list(availableColumns) # copy allows us to remove tested columns
        availableTestColumnsRemaining = len(availableTestColumns)
        currentColumnIndex = 0
        # while loop is for hypothetical testing of the current state of initialMatrix
        # use a while loop so we can shrink availableColumns to avoid unnecessary iterations
        while availableTestColumnsRemaining > 0:
            #print("---------------")
            #print("currentColumnIndex:",currentColumnIndex)
            #print("availableTestColumnsRemaining:",availableTestColumnsRemaining)
            initialMatrixCopy = list(initialMatrix) # to see what would happen to the current matrix IF we changed it
            testColumn = availableTestColumns[currentColumnIndex] # get the current column
            initialMatrixCopy[row] = testColumn
            testColumnConflicts = conflicts(row, initialMatrixCopy, csp)
            #print("testColumn:",testColumn)
            #print("testColumnConflicts:",testColumnConflicts)
            # if there are no conflicts for the current column
            # stop iterating through the available columns
            # instead, use the current column to save time
            if testColumnConflicts == 0:
                minConflictsColumn = testColumn
                availableTestColumns.remove(testColumn)
                availableTestColumnsRemaining -= 1
                break
            
            elif testColumnConflicts < minConflicts: # just found a better column to use
                minConflicts = testColumnConflicts
                minConflictsColumn = testColumn
                availableTestColumns.remove(testColumn)
                availableTestColumnsRemaining -= 1

            #print("minConflictsColumn:",minConflictsColumn)
            #currentColumnIndex += 1

            # DON'T WE NEED TO GET HERE EVEN WHEN THE "if" CONDITION IS TRUE?
            # OTHERWISE, NOT ALL INDIVIDUAL QUEENS GET A UNIQUE COLUMN
            # LOOP RESTARTS TOO SOON b/c OF break
            # infinite loop

            #availableTestColumns.remove(testColumn)
            #availableTestColumnsRemaining -= 1

        # once we've gone through all available columns
        # use the best one for the current row and remove the column from contention
        initialMatrix[row] = minConflictsColumn
        availableColumns.remove(minConflictsColumn)
    
    return initialMatrix

def initializeListOfConflicts(current, csp):
    listOfConflicts = []
    for queen in range(0,csp):
        listOfConflicts.append(conflicts(queen, current, csp))
    print("listOfConflicts:",listOfConflicts)
    return listOfConflicts

# returns number of conflicts (diagonal only as there are never any row or column conflicts)
def conflicts(queen, current, csp):
    return calculateLeftDiag(queen, current, csp) + calculateRightDiag(queen, current, csp)
    

# returns false if any of the 4 constraints have been violated for any of the queens
# returns true otherwise
def constraints(listOfConflicts):
    result = True
    for queen in listOfConflicts:
        if queen != 0:
            result = False
            break
    return result

"""
Caution: big algorithm below
"""

def minConflicts(csp):
    current = initialize(csp)
    print("initialMatrix:", current)
    maxSteps = csp*0.5 #CHANGE THIS FOR THE LOVE OF GOD
    
    for i in range(0, maxSteps):
        listOfConflicts = initializeListOfConflicts(current, csp)
        if constraints(listOfConflicts) == True:
            return current
        else:
            queen = mostConflicts(listOfConflicts, csp)
            row = queen
            minConflicts = conflicts(queen, current, csp)
            minConflictsRow = row
            # swaps taking into account the number of conflicts that are being created
            for otherQueen in range(0, csp):
                if otherQueen != queen: # don't bother testing swapping a queen with itself
                    currentCopy = list(current)
                    currentCopy = queenSwap(currentCopy, queen, otherQueen)
                    createdConflicts = conflicts(queen, currentCopy, csp)
                    if createdConflicts == 0:
                        minConflictsRow = otherQueen
                        break
                    elif createdConflicts < minConflicts:
                        minConflicts = createdConflicts
                        minConflictsRow = otherQueen

            current = queenSwap(current, queen, minConflictsRow)

            #WE ARE HERE
                
                
    return current


def main():
    solutions = []
    with open("nqueens.txt", "r") as f:
        csp = int(f.read())
        solutions.append(minConflicts(csp))
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
 takes in the current matrix,
    the index of the queen we care about and csp
    returns the number of left diagonal conflicts
"""
def calculateLeftDiag(queen, current, csp):
    #print("LEFT DIAG")
    #print("============")
    row = queen
    column = current[queen]
    conflicts = 0
    diagNum = row-column
    otherRow = 0
    #print("row:", row)
    #print("column:",column)
    #print("diagNum:",diagNum)
    while otherRow < (csp):
        if otherRow != row:
            otherColumn = current[otherRow]
            if otherColumn != 0: #for stopping this from caring about initialization columns (which are zero) during initialization
                otherDiagNum = otherRow - otherColumn
                if diagNum == otherDiagNum:
                    conflicts += 1
        otherRow += 1
    #print("conflicts(left diag):", conflicts)
    return conflicts

"""
 takes in the current matrix,
    the index of the queen we care about and csp
    returns the number of right diagonal conflicts
"""
def calculateRightDiag(queen, current, csp):
    row = queen
    column = current[queen]
    conflicts = 0
    diagNum = row + column
    otherRow = 0
    while otherRow != (csp-1):
        if otherRow != row:
            otherColumn = current[otherRow]
            if otherColumn != 0: #for stopping this from caring about initialization columns (which are zero) during initialization
                otherDiagNum = otherRow + otherColumn
                if diagNum == otherDiagNum:
                    conflicts += 1
        otherRow += 1
    #print("conflicts(right diag):", conflicts)
    return conflicts
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

def queenSwap(currentCopy, queen1, queen2):
    column1 = currentCopy[queen1]
    currentCopy[queen1] = currentCopy[queen2]
    currentCopy[queen2] = column1
    return currentCopy

def updateListOfConflicts(listOfConflicts, thisQueen, thatQueen):

    return listOfConflicts

"""
Timing Functions
"""
