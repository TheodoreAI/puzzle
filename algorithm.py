# Mateo Estrada
# CS325
# 03/01/2020
# Description: This algorithm checks to see if the input solution to the 8-puzzle (also known as the sliding puzzle) is solvable.


# Step 1: I choose my favorite puzzle: the 8-puzzle (puzzle number 12 from the list).


# Step 2: The following rules were taken from: file:///Users/mateog.estrada/Downloads/A_Survey_of_NP-Complete_puzzles.pdf

# I. Played on an mxm
# II. m^2 - 1 = n
# III. There is a blank tile that has a possible number of 2, 3, 4 adjacent tiles depending on the location of the blank tile.
# IV. Standard size is a 3x3 and a move of the blank tile will mean the adjacent tile will move to the blank.
# V. 181,440 possible variations that are solvable.


# Step 4: I will use the idea of counting the number of inversions between nodes. Given a board of size N where the size N is an odd integer,
# each legal move changes the number of inversions by an even number.
# If a board has an odd number of inversions, then it cannot lead to the goal board by a sequence of legal moves because the goal board has an even number of inversions.
# I will show my proof by example:

def getInversions(arr):
    """This function was taken from: https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/#:~:text=What%20is%208%20puzzle%3F,tiles%20into%20the%20empty%20space."""

    # we initially the count at 0
    countOfInversions = 0
    for i in range(0, len(arr)):
        for j in range(i + 1, len(arr)):
            # value 0 will be used to indicate the "blank"
            if arr[i] > arr[j] != 0:
                countOfInversions += 1
    return countOfInversions





class Solution:

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def hasSolution(self):
        # count inversions in 8 puzzle
        invertCount = getInversions(self.puzzle)

        return invertCount % 2 == 0

    def checkSolution(self):

        if self.hasSolution():
            print("Solvable!")
        else:
            print("Can't solve that! (Remember, for an 8-puzzle there must be an even number of inversions for the puzzle to have a solution! Please see pdf for more details!")


# The testing:

# this one you should be able to solve because it has an even number of inversions aka 1,3,4,2,5,7,8,6 inversions (3-2, 4-5, 7-6, 8-6)  and four inversions is even!
# p1 = [0, 1, 3, 4, 2, 5, 7, 8, 6]
# s1 = Solution(p1)
# s1.checkSolution()
#
# # this one you shouldn't because it has an odd number of inversions aka 8 - 7 is one inversion and one is odd!
# p2 = [1, 2, 3, 4, 5, 6, 8, 7, 0]
# s2 = Solution(p2)
# s2.checkSolution()

# Step 5: The proof is explained using some of the logic from this resource: https://www.cs.princeton.edu/courses/archive/spring13/cos226/assignments/8puzzle.html
