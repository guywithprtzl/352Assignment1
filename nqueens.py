"""
CISC 352 Assignment 1
nqueens.py
Sean Tippett - 10108181
Heni Virag - 10142490
"""
import random

def initialize(n):
    initialMatrix = []
    for i in range(1,n+1):
        initialMatrix.append(i)
    random.shuffle(initialMatrix)
    return initialMatrix

