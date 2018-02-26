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

def initialize(csp, shuffle):
    initialMatrix = []
    availableColumns = []
    
    for i in range(1,csp+1): # column count starts at 1
        availableColumns.append(i)
        initialMatrix.append(0) # set up all available rows
    if shuffle == True:
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
            #print("availableTestColumns:",availableTestColumns)
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
                break
            
            elif testColumnConflicts < minConflicts: # just found a better column to use
                minConflicts = testColumnConflicts
                minConflictsColumn = testColumn
                availableTestColumns.remove(testColumn)
                availableTestColumnsRemaining -= 1

            

            else:
                availableTestColumns.remove(testColumn)
                availableTestColumnsRemaining -= 1
                
            #print("minConflictsColumn:",minConflictsColumn)

        # once we've gone through all available columns
        # use the best one for the current row and remove the column from contention
        initialMatrix[row] = minConflictsColumn
        availableColumns.remove(minConflictsColumn)
    print("++++++++++++++++++++++++++++++")
    print("Initial Matrix: ", initialMatrix)
    return initialMatrix

def initializeListOfConflicts(current, csp):
    listOfConflicts = []
    for queen in range(0,csp):
        listOfConflicts.append(conflicts(queen, current, csp))
    #print("listOfConflicts:",listOfConflicts)
    totalConflicts = 0
    totalQueensInConflict = 0
    for i in listOfConflicts:
        if i != 0:
            totalQueensInConflict += 1
            totalConflicts += i
    print("listOfConflicts Summed: ", totalConflicts)
    print("totalQueensInConflict: ", totalQueensInConflict)
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
    if result == True:
        print(result)
    return result

"""
Caution: big algorithm below
"""

def minConflicts(csp, shuffle):
    current = initialize(csp, shuffle)
    #print("initialMatrix:", current)
    maxSteps = int(csp*4) #CHANGE THIS FOR THE LOVE OF GOD
    currentStep = 0
    stuck = 0
    recentlySwapped0 = -1 #stop pointless swapping back and forth
    recentlySwapped1 = -1
    while currentStep <= maxSteps:
        listOfConflicts = initializeListOfConflicts(current, csp)
        
        if constraints(listOfConflicts) == True:
            return current
        else:
            queen = mostConflicts(listOfConflicts, csp)
            row = queen
            initialConflicts = conflicts(queen, current, csp)
            minConflicts = initialConflicts
            minConflictsRow = row
            # swaps taking into account the number of conflicts that are being created
            for otherQueen in range(0, csp):
                if otherQueen != queen and ((recentlySwapped0 != queen or recentlySwapped1 != otherQueen) and (recentlySwapped1 != queen or recentlySwapped0 != otherQueen)): # don't bother testing swapping a queen with itself
                    currentCopy = list(current)
                    currentCopySwapped = queenSwap(currentCopy, queen, otherQueen, False)
                    swappedConflicts = conflicts(queen, currentCopySwapped, csp)
                    createdConflicts = swappedConflicts - initialConflicts
                    

                    if createdConflicts < 0:
                        if swappedConflicts == 0:
                            minConflictsRow = otherQueen
                            break
                    
                        elif swappedConflicts < minConflicts:
                            minConflicts = swappedConflicts
                            minConflictsRow = otherQueen
        
        
            if queen != minConflictsRow:
                
                current = queenSwap(current, queen, minConflictsRow, True)
                recentlySwapped0 = queen
                recentlySwapped1 = minConflictsRow
                currentStep += 1
                stuck = 0
            else:
                if stuck == (csp + 1):
                    currentStep = maxSteps + 1 #stop an infinite loop where the current setup is unsolvable
                else:
                    stuck += 1
            #print("current:",current)
        print("currentStep: ", currentStep)
            #WE ARE HERE
                
                
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
            attempt = minConflicts(csp, False)
        else:
            print("=========================================================")
            attempt = minConflicts(csp, True)
        
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
            if otherColumn != 0: # prevents conflicts with non-columns (0 which is used to populate the matrix)
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

def queenSwap(currentCopy, queen1, queen2, real):
    if real:
        print("Swapping queen ", queen1, ", column #", currentCopy[queen1], " with queen ", queen2, ", column #", currentCopy[queen2])
    column1 = currentCopy[queen1]
    currentCopy[queen1] = currentCopy[queen2]
    currentCopy[queen2] = column1
    if real:
        print("Resulting Matrix: ", currentCopy)
        
    return currentCopy


"""
Timing Functions
"""
