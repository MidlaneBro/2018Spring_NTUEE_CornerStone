from node import *
import maze as mz
import score
#import student
import BT

import numpy as np
import pandas
import time
import sys
import os

def main():
    btooth = BT.bluetooth()
    port = input("PC bluetooth port name: ")
    while(not btooth.do_connect(port)):
        if(port == "quit"):
            btooth.disconnect()
            quit()
            port = input("PC bluetooth port name: ")
    input("Press enter to start.")  

    maze = mz.Maze("demo/final_maze.csv")
    cur_nd = maze.getStartPoint()
    car_dir = 2
    point = score.Scoreboard("demo/UID_score.csv")
    game_type = int(input("Which game to play? (1/2)"))
    while((game_type!=1)and(game_type!=2)):
        game_type = int(input("Which game to play? (1/2)"))
    #interface = student.interface()         the part of calling student.py was commented out.
    if(game_type==1):
    #if(sys.argv[1] == '0'): #game 1
        '''
        #TODO: Implement your algorithm here and return the UID for evaluation function
        ndList = maze.strategy(next_nd)
        # ================================================
        # Basically, you will get a list of nodes and corresponding UID strings after the end of algorithm.
        # The function add_UID() would convert the UID string score and add it to the total score.
        # In the sample code, we call this function after getting the returned list. 
        # You may place it to other places, just make sure that all the UID strings you get would be converted.
        # ================================================
        for i in range(1, len(ndList)):
            node = 0
            get_UID = "just a test"
            point.add_UID(get_UID)
        break
        '''
        time = int(input("time limit (sec): "))
        actionList = maze.game_1(time, car_dir)
        for i in actionList:
            print(i)
            btooth.SerialWrite(chr(i+48))
        btooth.SerialWrite(chr(48))
        print(0)
        
        while (1):
            if(btooth.ser.in_waiting!=0):
                point.add_UID(btooth.SerialReadByte())
                btooth.ser.reset_input_buffer()
    elif(game_type==2):
    #elif(sys.argv[1] == '1'):   #game 2
        
        #input five endpoints at a time or,
        nds = []
        while(1):
            nds.append(maze.nd_dict[int(input("destination: "))])
            if(nds[-1].getIndex() == 1):
                print("start process")
                print('')
                break
        nds.remove(maze.nd_dict[1])
        actionList = []
        for i in nds:
            path = maze.Dijkstra(cur_nd,i,car_dir)
            actionList += path[1]
            car_dir = path[2]
            cur_nd = i
        
        for j in actionList:
            btooth.SerialWrite(chr(j+48))
        btooth.SerialWrite('0')
                             
        #print (actionList)
        while (1):
            if(btooth.ser.in_waiting!=0):
                point.add_UID(btooth.SerialReadString())
                btooth.ser.reset_input_buffer()
        '''
        #input one at a time
        while (1):
            next_nd = maze.nd_dict[int(input("destination: "))]
            if(next_nd.getIndex() == 0):
            	print("end process")
            	print('')
            	break

            path = maze.Dijkstra(cur_nd,next_nd,car_dir)
            actionList = path[1]
            car_dir = path[2]
            cur_nd = next_nd
            for i in actionList:
                btooth.SerialWrite(i.encode("utf-8"))
            #print (actionList)
            while (1):
                if(btooth.ser.in_waiting!=0):
                    uid=btooth.SerialReadByte()
                    print("uid值:"+uid)
                    point.add_UID(uid)
                    break
        '''
            
    """
    node = 0
    while(not node):
        node = interface.wait_for_node()

    interface.end_process()
    """
    print("complete")
    print("")
    a = point.getCurrentScore()
    print("The total score: ", a)

if __name__=='__main__':
    main()
