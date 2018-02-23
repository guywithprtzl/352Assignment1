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
    
    for i in range(1,csp+1): #this is our range so we don't have a 0 column
        availableColumns.append(i)
        initialMatrix.append(0) #set up all available rows
        
    #random.shuffle(availableColumns) #does shuffling help or should we keep it in order TEST THIS
    #print("availableColumns:", availableColumns)
    for row in range(0, csp): #looking at indicies now so range back to normal
        #we go through the initial matrix starting at row 0 and decide which of the available columns
        #cause the least number of conflicts
        #print("=====================")
        #print("initialMatrix:",initialMatrix)
        
        minConflicts = csp #impossible to have more conflicts than there are queens
        minConflictsColumn = 0 #keep track of which column has the least number of conflicts
        availableTestColumns = list(availableColumns) #need to make a copy so we can remove tested columns without saying that we're actually using this column in the initialMatrix
        availableTestColumnsRemaining = len(availableTestColumns)
        currentColumnIndex = 0
        #below loop is for hypothetical testing of the current state of initialMatrix
        while availableTestColumnsRemaining > 0: #use a while loop so we can shrink availableColumns so we don't have to iterate through it so much
            #print("---------------")
            #print("currentColumnIndex:",currentColumnIndex)
            #print("availableTestColumnsRemaining:",availableTestColumnsRemaining)
            initialMatrixCopy = list(initialMatrix) # want to look at what happens to our current matrix IF we change it without actually changing it so we make a copy
            testColumn = availableTestColumns[currentColumnIndex] #get our current column
            initialMatrixCopy[row] = testColumn
            testColumnConflicts = conflicts(row, initialMatrixCopy, csp)
            #print("testColumn:",testColumn)
            #print("testColumnConflicts:",testColumnConflicts)
            if testColumnConflicts == 0: #if there are no conflicts for the current column we will stop iterating through the available columns and just use the current column to save time
                minConflictsColumn = testColumn
                break
            
            elif testColumnConflicts < minConflicts: #if this condition is true then we will have found a better column to use
                minConflicts = testColumnConflicts
                minConflictsColumn = testColumn
            #print("minConflictsColumn:",minConflictsColumn)
            #currentColumnIndex += 1
            availableTestColumns.remove(testColumn)
            availableTestColumnsRemaining -= 1

        #once we've gone through all availble columns we need to use the best one for our current row and remove the column from contention
        initialMatrix[row] = minConflictsColumn
        availableColumns.remove(minConflictsColumn)
    
    return initialMatrix

def initalizeListOfConflicts(current, csp):
    listOfConflicts = []
    for queen in range(0,csp):
        listOfConflicts.append(conflicts(queen, current, csp))
    print("listOfConflicts:",listOfConflicts)
    return listOfConflicts

#returns number of conflicts (diagonal only as there are never any row or column conflicts)
def conflicts(queen, current, csp):
    return calculateLeftDiag(queen, current, csp) + calculateRightDiag(queen, current, csp)
    

#checks
def constraints(listOfConflicts):
    result = True
    for queen in listOfConflicts:
        if queen != 0:
            result = False
            break
    return result

"""
caution: big algorithim below
"""
def minConflicts(csp):
    current = initialize(csp)
    print("initialMatrix:", current)
    listOfConflicts = initalizeListOfConflicts(current, csp)
    maxSteps = csp*0.5 #CHANGE THIS FOR THE LOVE OF GOD
    
    for i in range(0,maxSteps):
        if constraints(listOfConflicts) == True:
            return current
        else:
            queen = mostConflicts(listOfConflicts, csp)
            row = queen
            minConflicts = conflicts(queen, current, csp)
            minConflictsRow = row
            for otherQueen in range(0,csp): #great
                if otherQueen != queen: #don't bother testing swapping a queen with itself
                    currentCopy = list(current)
                    currentCopy = queenSwap(currentCopy, queen, otherQueen)
                    createdConflicts = conflicts(queen, currentCopy, csp)
                    if createdConflicts == 0:
                        minConflictsRow = otherQueen
                        break
                    elif createdConflicts < minConflicts:
                        minConflicts = createdConflicts
                        minConflicts = otherQueen

            current = queenSwap(current, queen, otherQueen)
            listOfConflicts = updateListOfConflicts(listOfConflicts, queen, otherQueen)
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
    maxConflicts = listOfConflicts[queen] #use the first queen as our initial max conflicts amount
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

def updateListOfConflicts(listOfConflicts, 

"""
Timing Functions
"""
