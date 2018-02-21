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
    for i in range(1,csp+1):
        initialMatrix.append(i)
    random.shuffle(initialMatrix)
    return initialMatrix


def conflicts(queen, var, current, csp):
    pass

def constraints(current):
    pass
    




"""
#################
Utility Functions
#################
"""

"""
 takes in the current matrix,
    the index of the queen we care about 
"""
def calculateLeftDiag(queen, current):
    row = queen
    column = current[queen]
    conflicts = 0
    #helpful code here
    return conflicts

def calculateRightDiag(queen, current):
    row = queen
    column = current[queen]
    conflicts = 0
    #helpful code here
    return conflicts

