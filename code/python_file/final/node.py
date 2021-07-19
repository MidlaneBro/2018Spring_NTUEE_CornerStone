import numpy as np
from enum import IntEnum

class Direction(IntEnum):
    NORTH   = 1
    EAST    = 4
    SOUTH   = 2
    WEST    = 3

def reverse(dir):
    if dir == Direction.NORTH: return Direction.SOUTH
    if dir == Direction.SOUTH: return Direction.NORTH
    if dir == Direction.WEST:  return Direction.EAST
    if dir == Direction.EAST:  return Direction.WEST
    print("invalid Direction")
    return 0

class Node:
    def __init__(self, index=0):
        self.index = index
        self.Successors = []

    def getIndex(self):
        return self.index

    def getSuccessors(self):
        return self.Successors

    def setSuccessor(self, successor, direction, length=1):
        for succ in self.Successors:
            if(successor==succ[0]):
                print("Error: repeated index with "+str(succ[0]))
            elif(direction==succ[1]):
                print("Error: repeated direction with "+ str(succ[1]))
        self.Successors.append((successor, direction, length))
        	#TODO: check whether the input of the function is valid by comparing with the class member
        #TODO: Update the successors in data members 
        return

    def getSuccessor(self, direction):
        for succ in self.Successors:
            if(succ[1]==direction):
                return succ[0]
                #TODO: Check which successor matches the input corner and return
        # For the valid input, the below part shouldn't be entered
        print("Node(", self.index, ") Successor is not found")
        return 0

    def getDirection(self, nd):
        for succ in self.Successors:
            if(succ==nd):
                return succ[1]
            #TODO: Check which successor matches the input direction and return
        # For the valid input, the below part shouldn't be entered
        print("Error in Node.py, getDirection()")
        print("Node(",nd.getIndex(),") is not the Successor of node(",self.index,")")
        return 0

    def isSuccessor(self, nd):
        for succ in self.Successors:
            if succ[0] == nd: return True
        return False

    def isEnd(self):
        return len(self.Successors) == 1 and self.index != 1
