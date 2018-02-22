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
import sys

def initialize(csp):
    initialMatrix = []
    for i in range(1,csp+1):
        initialMatrix.append(i)
    random.shuffle(initialMatrix)
    return initialMatrix


def conflicts(queen, value, current, csp):
    calculate
    pass

#checks
def constraints(listOfConflicts):
    
    pass
    


def main():
    solutions = []
    with open("nqueens.txt", "r") as f:
        csp = f.read()
        solutions.append(min_conflicts(csp))
    solutionsToString
    with open(filename, "w") as f:
        f.write('\n'.join(sizesAsString))

"""
#################
Utility Functions
#################
"""

"""
 takes in the current matrix,
    the index of the queen we care about 
"""
def calculateLeftDiag(queen, current, csp):
    row = queen
    column = current[queen]
    conflicts = 0
    diagNum = row-column
    otherRow = 0
    while otherRow != (csp-1):
        if otherRow != row:
            otherColumn = current[otherRow]
            otherDiagNum = otherRow - otherColumn
            if diagNum == otherDiagNum:
                conflicts++
        otherRow++
    return conflicts

def calculateRightDiag(queen, current, csp):
    row = queen
    column = current[queen]
    conflicts = 0
    diagNum = row + column
    otherRow = 0
    while otherRow != (csp-1):
        if otherRow != row:
            otherColumn = current[otherRow]
            otherDiagNum = otherRow + otherColumn
            if diagNum == otherDiagNum:
                conflicts++
        otherRow++
    return conflicts

