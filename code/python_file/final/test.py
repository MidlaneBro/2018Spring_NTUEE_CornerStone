import maze
import node
import numpy as np
def main():
    m = maze.Maze("test_dis_20180502.csv")
    print (m.game_1(10,2))

    i=50
    while(i>0):
        print (i)
        print (m.game_1(i,2))
        i-=1

if __name__ == "__main__":
    main()
