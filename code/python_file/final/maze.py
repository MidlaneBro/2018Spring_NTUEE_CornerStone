#4 units 2.35s
#6 units + 1 turning 4.30s
import node
import numpy as np
import csv
import pandas
import itertools
from enum import IntEnum

class Action(IntEnum):
	ADVANCE     = 1
	TURN_RIGHT  = 2
	U_TURN      = 5
	TURN_LEFT   = 3
	BACK        = 4
	HALT        = 6

class Maze:
	def __init__(self, filepath):
		self.raw_data = pandas.read_csv(filepath).values
		self.nodes = [node.Node()]  #dummy node
		self.nd_dict = dict() # key: index, value: the correspond node
		self.explored = set()

		for dt in self.raw_data:
			self.nodes.append(node.Node(int(dt[0])))
			for i in range(1,5):
				if(not np.isnan(dt[i])):
					self.nodes[-1].setSuccessor(int(dt[i]),i,int(dt[i+4]))
			self.nd_dict[self.nodes[-1].getIndex()] = self.nodes[-1]
		'''
		for i in self.nodes:
			print(i.getIndex())
			print(":")
			print(i.getSuccessors())
		'''
		   
	def getStartPoint(self):
		if (len(self.nd_dict) < 2):
			print ("Error: the start point is not included.")
			return 0;
		return self.nd_dict[1]
	'''
	def BFS(self, nd):
		""" return a sequence of nodes from the node to the nearest unexplored deadend"""
		#TODO: design your data structure here for your algorithm
		ndList = []
		while (True):
			#TODO: Apply your algorithm here. Make sure your algorithm can update values and stop under some conditions.
			break
		#TODO: update the information of your data structure
		ndList.reverse()
		return ndList

	def BFS_2(self, nd_from, nd_to):
		""" return a sequence of nodes of the shortest path"""
		#TODO: similar to BFS but fixed start point and end point
		ndList = []

		return ndList
	'''

	def getAction(self, car_dir, next_dir):
		if(next_dir==car_dir):
			return 1
		elif(next_dir==self.reverseDir(car_dir)):
			return 4
		elif(((next_dir==4) and(car_dir==1)) or((next_dir==2) and(car_dir==4)) or((next_dir==3) and(car_dir==2)) or((next_dir==1) and(car_dir==3))):
			return 2
		elif(((next_dir==1) and(car_dir==4)) or((next_dir==4) and(car_dir==2)) or((next_dir==2) and(car_dir==3)) or((next_dir==3) and(car_dir==1))):
			return 3
		else:
			print("Error: getAction")
			return 0

	def reverseAct(self, action):
		if(action==6):
			return 6
		elif(action==1):
			return 4
		elif(action==2):
			return 3
		elif(action==3):
			return 2
		elif(action==4):
			print("Error: algorithm")
			return 1

	def reverseDir(self, direction):
		if(direction==1):
			return 2
		elif(direction==2):
			return 1
		elif(direction==3):
			return 4
		elif(direction==4):
			return 3
		else:
			print("Error: direction")
			return 0
	'''
	def getAction(self, car_dir, nd_from, nd_to):
		
		if nd_from.isSuccessor(nd_to):
			nd_dir = nd_from.getDirection(nd_to)
			#TODO: Return the action based on the current car direction and the direction to next node
			print("Error: Failed to get the action")
			return 0
		else:
			print("Error: Node(",nd_to.getIndex(),") is not the Successor of Node(",nd_from.getIndex(),")")
			return 0
	
	def strategy(self, nd):
		return self.BFS(nd)

	def strategy_2(self, nd_from, nd_to):
		return self.BFS_2(nd_from, nd_to)
	'''
	'''
	#version 1:
	def Dijkstra(self, nd_from, nd_to, current_dir):
		turning_cost=1.1
		block_cost=0.56
		cost = []   #float, cost from start to the point
		predecessor = []    #int
		drct = []   #int, direction with respect to its predecessor
		visit = []  #bool, true if hasn't been visited
		for i in range(len(self.nodes)):
			cost.append(-1)
			predecessor.append(0)
			drct.append(0)
			visit.append(True)
		p_queue=[nd_from.getIndex()]    #store a set of nodes' indices under consideration
		least=0
		cost[p_queue[least]]=0
		drct[p_queue[least]]=current_dir
		while(p_queue[least]!=nd_to.getIndex()):
			for i in self.nd_dict[p_queue[least]].Successors: #i is a tuple
				if(visit[i[0]]):
					if(i[1]==drct[p_queue[least]] or self.reverseDir(drct[p_queue[least]])): #no need to turn or backward
						if (cost[i[0]]== -1):
							p_queue.append(i[0])
							drct[i[0]]=i[1]
							predecessor[i[0]]=p_queue[least]
							cost[i[0]]=cost[p_queue[least]]+i[2]*block_cost
						elif (cost[p_queue[least]]+i[2]*block_cost<=cost[i[0]]):
							drct[i[0]]=i[1]
							predecessor[i[0]]=p_queue[least]
							cost[i[0]]=cost[p_queue[least]]+i[2]*block_cost
					elif(i[1]!=drct[p_queue[least]]): #need to turn
						if (cost[i[0]]== -1):
							p_queue.append(i[0])
							drct[i[0]]=i[1]
							predecessor[i[0]]=p_queue[least]
							cost[i[0]]=cost[p_queue[least]]+i[2]*block_cost+turning_cost
						elif (cost[p_queue[least]]+i[2]*block_cost+turning_cost<=cost[i[0]]):
							drct[i[0]]=i[1]
							predecessor[i[0]]=p_queue[least]
							cost[i[0]]=cost[p_queue[least]]+i[2]*block_cost+turning_cost
			visit[p_queue[least]]=False
			p_queue.pop(least)
			least=0
			for i in range(len(p_queue)):
				if(cost[p_queue[i]]<cost[p_queue[least]]):
					least=i
		index=nd_to.getIndex()  #now generating (cost, action_list[])
		action_list=[6]
		while(index!=nd_from.getIndex()):
			print(index,predecessor[index])
			action_list.append(self.getAction(drct[predecessor[index]],drct[index]))
			index=predecessor[index]
		action_list.reverse()
		#in reverse direction, should not happen except at start point
		for c, v in enumerate(action_list[:-1]):
			if(action_list[c+1]==6):
				if(v==5):   #backwards
					final_dir=self.reverseDir(drct[nd_to.getIndex()])
				else:
					final_dir=drct[nd_to.getIndex()]
			elif(v==5):   #backwards
				action_list[c+1]=self.reverseAct(action_list[c+1])
			

		return (cost[nd_to.getIndex()], action_list, final_dir) #(minimum cost, instructions, car direction when halting)
	'''
	#version 2:
	def Dijkstra(self, nd_from, nd_to, current_dir):
		turning_cost=1.05
		block_cost=0.7
		cost = []   #float, cost from start to the point
		predecessor = []    #int
		drct = []   #int, direction with respect to its predecessor
		visit = []  #bool, true if hasn't been visited
		for i in self.nodes:
			cost.append(-1)
			predecessor.append(0)
			drct.append(0)
			visit.append(True)
		p_queue=[nd_from.getIndex()]    #store a set of nodes' indices under consideration
		least=0
		cost[p_queue[least]]=0
		drct[p_queue[least]]=current_dir
		while(p_queue[least]!=nd_to.getIndex()):
			for i in self.nd_dict[p_queue[least]].Successors: #i is a tuple
				if(visit[i[0]]):
					if(i[1]==drct[p_queue[least]] or i[1]==self.reverseDir(drct[p_queue[least]])): #no need to turn or backward
						if (cost[i[0]]== -1):
							p_queue.append(i[0])
							drct[i[0]]=i[1]
							predecessor[i[0]]=p_queue[least]
							cost[i[0]]=cost[p_queue[least]]+i[2]*block_cost
						elif (cost[p_queue[least]]+i[2]*block_cost<=cost[i[0]]):
							drct[i[0]]=i[1]
							predecessor[i[0]]=p_queue[least]
							cost[i[0]]=cost[p_queue[least]]+i[2]*block_cost
					#elif(i[1]!=drct[p_queue[least]]): #need to turn
					else:
						if (cost[i[0]]== -1):
							p_queue.append(i[0])
							drct[i[0]]=i[1]
							predecessor[i[0]]=p_queue[least]
							cost[i[0]]=cost[p_queue[least]]+i[2]*block_cost+turning_cost
						elif (cost[p_queue[least]]+i[2]*block_cost+turning_cost<=cost[i[0]]):
							drct[i[0]]=i[1]
							predecessor[i[0]]=p_queue[least]
							cost[i[0]]=cost[p_queue[least]]+i[2]*block_cost+turning_cost
			visit[p_queue[least]]=False
			p_queue.pop(least)
			least=0
			for i in range(len(p_queue)):
				if(cost[p_queue[i]]<cost[p_queue[least]]):
					least=i
		action_list= []
		index=nd_to.getIndex()  #now generating (cost, action_list[])
		while(index!=nd_from.getIndex()):
			#print(index,predecessor[index])
			action_list.append(self.getAction(drct[predecessor[index]],drct[index]))
			index=predecessor[index]
		action_list.reverse()
		final_dir=drct[nd_to.getIndex()]

		return (cost[nd_to.getIndex()], action_list, final_dir) #(minimum cost, instructions, car direction when halting)
	'''
	def ndToPath(self, ndList, init_dir):	#starts from node 1
		path = self.Dijkstra(self.nd_dict[1],self.nd_dict[ndList[0]],init_dir)
		car_dir = path[2]
		action=[path[0], path[1]]
		for c, v in enumerate(ndList[:-1]):
			path = self.cost_btn_ep[(v,ndList[c+1])]
			action[0] += path[0]
			car_dir = path[2]
			action[1] += path[1]
		return action
	'''
	def ndToPath(self, ndList, init_nd, init_dir):	#starts from arbitrary endpoint
		path = self.Dijkstra(self.nd_dict[init_nd],self.nd_dict[ndList[0]],init_dir)
		car_dir = path[2]
		action=[path[0], path[1]]
		for c, v in enumerate(ndList[:-1]):
			path = self.cost_btn_ep[(v,ndList[c+1])]
			action[0] += path[0]
			car_dir = path[2]
			action[1] += path[1]
		return action

	def NToP_with_time_limit(self, ndList, init_dir, limit, distance):	#does not return full path if exceeding time limit
		path = self.Dijkstra(self.nd_dict[1],self.nd_dict[ndList[0]],init_dir)
		action = [path[0], path[1], 0]	#[cost, action, score]
		car_dir = init_dir
		for c, v in enumerate(ndList[:-1]):
			path = self.cost_btn_ep[(v,ndList[c+1])]
			if(action[0]+path[0]>limit):
				return action
			else:
				action[0] += path[0]
				car_dir = path[2]
				action[1] += path[1]
				action[2] += distance[ndList[c+1]]
		return action
	
	def exhaustiveAttack(self, ndList, init_nd, init_dir):
		action = []
		mint = 0
		flag = True
		p = list(itertools.permutations(ndList))
		for a in p:	#a is a list of ends
			action.append(self.ndToPath(list(a),init_nd,init_dir))
			
			if(flag):
				mint = len(action)-1
				flag = False
			elif(action[-1][0]<action[mint][0]):
				mint = len(action)-1
		return [action[mint],list(p[mint])]

	def optimalPath(self, ndList, init_nd, init_dir):
		if(len(ndList)==0):
			return [[0,[]],[]]
		elif(len(ndList)<=self.nd_num_upperbound):
			return self.exhaustiveAttack(ndList, init_nd, init_dir)
		else:
			cos = []
			mi=0
			me=ndList[0]
			for i in ndList:
				if(init_nd==1):
					path = self.Dijkstra(self.nd_dict[init_nd],self.nd_dict[i],init_dir)
				else:
					path = self.cost_btn_ep[(init_nd,i)]
				cos.append(path[0])
				if(cos[-1]<cos[mi]):
					mi=len(cos)-1
					me=i
			path = self.Dijkstra(self.nd_dict[init_nd],self.nd_dict[me],init_dir)
			action = [[path[0], path[1]],[init_nd, me]]
			car_dir = path[2]
			ndList.remove(me)
			next_act = self.optimalPath(ndList, me, car_dir)
			action[0][0] += next_act[0][0]
			action[0][1] += next_act[0][1]
			action[1] += next_act[1]
			return action

	def score_of_ends(self, t, distance):
		s = 0
		for e in t:
			s += distance[e]
		return s

	def game_1(self, time, init_dir):
		buff = 1.0	#buffer is time*(1-buff)
		time*=buff
		self.nd_num_upperbound=8
		#generate list of endpoints
		ends = []
		for k,v in self.nd_dict.items():
			if(v.isEnd()):
				ends.append(k)

		#calculate Manhattan distance between start and each endpoint
		#I.e., the expected value of treasure
		distance = []   #int, distance from start to the point
		drct = []   #int, direction with respect to its predecessor
		visit = []  #bool, true if hasn't been visited
		for i in self.nodes:
			distance.append(-1)
			drct.append(0)
			visit.append(True)
		p_queue=[self.nd_dict[1].getIndex()]    #store a set of nodes' indices under consideration
		least=0
		distance[p_queue[least]]=0
		drct[p_queue[least]]=init_dir
		while(len(p_queue)!=0):
			for i in self.nd_dict[p_queue[least]].Successors: #i is a tuple
				if(visit[i[0]]):
					if (distance[i[0]]== -1):
						p_queue.append(i[0])
						distance[i[0]]=distance[p_queue[least]]+i[2]
						drct[i[0]]=i[1]
					elif (distance[p_queue[least]]+i[2]<=distance[i[0]]):
						distance[i[0]]=distance[p_queue[least]]+i[2]
						drct[i[0]]=i[1]
			visit[p_queue[least]]=False
			p_queue.pop(least)
			least=0
			for i in range(len(p_queue)):
				if(distance[p_queue[i]]<distance[p_queue[least]]):
					least=i

		#generate dict of cost between two endpoints
		self.cost_btn_ep = dict()
		for i in ends:
			for j in ends:
				if(i!=j):
					self.cost_btn_ep[(i, j)] = self.Dijkstra(self.nd_dict[i],self.nd_dict[j],drct[i])

		#calculate total score
		total = 0
		for e in ends:
			total += distance[e]

		#determine which algorithm to use according to nodes
		if(0):
		#if(len(ends)<self.nd_num_upperbound):	#20 secs at most, calculate all
			action = []
			mint = 0
			maxs = 0
			flag = True
			p = list(itertools.permutations(ends))
			for a in p:	#a is a list of ends
				action.append(self.NToP_with_time_limit(list(a),init_dir,time,distance))
				
				if(action[-1][2]==total):
					if(flag):
						mint = len(action)-1
						flag = False
					elif(action[-1][0]<action[mint][0]):
						mint = len(action)-1
				if(flag):
					if(action[-1][2]>action[maxs][2]):
						maxs = len(action)-1
			if(flag):
				return action[maxs][1]
			else:
				return action[mint][1]

		else:	#call optimalPath
			subgroups = []
			for i in range(len(ends),0,-1):
				subgroups += list(itertools.combinations(ends,i))
			subgroups = sorted(subgroups, key = lambda t: self.score_of_ends(t,distance), reverse=True)
			action = self.optimalPath(list(subgroups[0]), 1, init_dir)
			optGroup = subgroups[0]
			index = 1
			while(action[0][0]>=time):
				action = self.optimalPath(list(subgroups[index]), 1, init_dir)
				optGroup = subgroups[index]
				index += 1
				if(index==len(subgroups)):
					break
				while(self.score_of_ends(subgroups[index],distance) == self.score_of_ends(subgroups[index-1],distance)):
					actionPrime = self.optimalPath(list(subgroups[index]), 1, init_dir)
					if(actionPrime[0][0]<action[0][0]):
						action = actionPrime
						optGroup = subgroups[index]
					index += 1
			compGroup = []
			for e in ends:
				if e not in optGroup:
					compGroup.append(e)
			actionPrime = self.optimalPath(compGroup, action[1][-1], drct[action[1][-1]])
			print (optGroup)
			print (compGroup)
			print (actionPrime)
			print (action)
			action[0][1] += actionPrime[0][1]
			print (action)
			return action[0][1]


		if(0):	#too unefficient to list all
		
			#shortest path in negligence of score
			n = [1]
			car_dir = init_dir
			flag=True
			for c,v in enumerate(ends):
				cos = []
				mi=0
				for i in ends:
					if(i not in n):
						path = self.Dijkstra(self.nd_dict[n[c]],self.nd_dict[i],car_dir)
						cos.append(path[0])
						if(flag):
							me=i
							flag=False
						if(cos[-1]<cos[mi]):
							mi=len(cos)-1
							me=i
				n.append(me)
				path = self.Dijkstra(self.nd_dict[n[c]],self.nd_dict[me],car_dir)
				car_dir=path[2]
				flag=True
			n.remove(1)
			action = self.ndToPath(n, 1, init_dir)
			if(action[0]<time):	#can reach all treasures within time limit
				return action[1]
			
			#TODO, inspect from lowest score endpoint combination to the highest before reaching nd_num_upperbound

			#else, calculate all possibilities
			action = []
			#mint = 0
			#maxt = 0
			maxs = 0
			#mins = 0
			p = list(itertools.permutations(ends))
			for a in p:	#a is a list of ends
				action.append(self.NToP_with_time_limit(list(a),init_dir,time,distance))
				'''
				if(action[-1][0]<action[mint][0]):
					mint = len(action)-1
				if(action[-1][0]>action[maxt][0]):
					maxt = len(action)-1
				'''
				if(action[-1][2]>action[maxs][2]):
					maxs = len(action)-1
				'''	
				if(action[-1][2]<action[mins][2]):
					mins = len(action)-1
				'''
			'''
			for i in action:
				print(i)
			
			print("best path with no time limit (shortest path in negligence of score):")
			print (action[mint])
			print(p[action.index(action[mint])])
			print("worst path with no time limit (longest path in negligence of score):")
			print (action[maxt])
			'''
			print("best path under time limit (highest score possible):")
			print (action[maxs])
			print(p[action.index(action[maxs])])
			'''
			print("worst path under time limit (lowest score possible):")
			print (action[mins])
			'''
			#or by density
			density = dict()
			maxi = 1
			for i,n in self.nd_dict.items():
				d=0
				for k in ends:
					if(k==i):
						continue
					else:
						path = self.Dijkstra(n,self.nd_dict[k],drct[i])
						d+=distance[k]/float(path[0])
				density[i] = d
				if(density[i]>density[maxi]):
					maxi = i
				#print(i,density[i])
			'''
			ndList = []
			for k in ends:
				if(k==maxi):
					continue
				else:
					path = self.Dijkstra(self.nd_dict[maxi], self.nd_dict[k], drct[maxi])
					ndList.append([k, distance[k]/float(path[0])])
			for i in ndList:
				print i
			
			print("cost of what i think is optimum:")
			a = [13, 7, 12, 18, 15, 20, 6, 8]
			print(self.NToP_with_time_limit(list(a), init_dir, time, distance))
			print a
			'''
		return 
		
