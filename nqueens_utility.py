import random
"""
Populating the input file
"""

def populate(filename, sizes):
    sizesAsString = []
    for num in sizes:
        sizesAsString.append(str(num)) #need to convert int to string so it can be added to file
    with open(filename, "w") as f:
        
        f.write('\n'.join(sizesAsString))

def generateSizes(small, medium, large):
    sizes = []
    for i in range(0,small):
        sizes.append(random.randint(4,1001)) #bounds for small input are 3<n<=1000
    for i in range(0,medium):
        sizes.append(random.randint(1001,100001)) #bounds for medium input are 1000<n<=100,000
    for i in range(0,large):
        sizes.append(random.randint(100001,10000000)) #bounds for large input are 100,000<n<10,000,001
    return sizes



def main():
    small = int(input("How many small values?"))
    medium = int(input("How many medium values?"))
    large = int(input("How many large values?"))
    sizes = generateSizes(small, medium, large)
    populate("nqueens.txt", sizes)

main()
