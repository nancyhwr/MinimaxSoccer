from collections import namedtuple 
from math import exp
import random
import operator
from scipy.optimize import linprog
import numpy as np
import math
from ast import literal_eval as make_tuple
from math import exp

# Player file: epsilon-greedy exploration; MinimaxQ Learning


class Player:

	
	def __init__(self, goal, ball, states, actions, Q, pi, state_state, alpha=1, decay = .9999954, gamma = .9, epsilon=.4):  #T, cool_down, subField, partition_r,
	
		self.goal = goal
		self.ball = ball
		self.actions = actions
		self.states = states
		self.Q = Q
		self.pi = pi
		self.V =  {s: 0 for s in states}
		for g in self.goal:
			self.V[g] = 1000
		
		##### Question: do I need to assign V-value for the goal states?????
		#######################
		self.alpha = alpha
		self.decay = decay
		self.gamma = gamma
		self.epsilon = epsilon
		#######################
		self.T = 0
		self.cool_down = 0
		#######################
		self.partition_r = 0
		self.subField = []
		#######################
		self.current_state = (0, 0)
		self.subField = None

		

	######### Take actions following epsilon-greedy policy
	def takeAction(self):
		######## Epsilon exploration policy ##########
		if random.uniform(0, 1) < self.epsilon:
			action = random.choice(self.actions)
			return action
		### Follow the mixed policy
		else:
			prob = [self.pi[self.current_state, a] for a in self.actions]

			###### temporarily solve the problem that the prob sometimes are negative even though I set the constraints! 
			###### I guess it's something with the package "linprog"
			for i in range(len(prob)):
				if prob[i] < 0:
					prob[i] = 0
			prob = [prob[i]/sum(prob) for i in range(len(prob))]
			action = np.random.choice(len(self.actions),1, replace=False, p = prob) 
			return self.actions[action[0]]


	def updateQ(self, initialState, finalState, action_p, action_o, reward, restrictActions=None):
		
		self.Q[initialState, action_p, action_o] = (1 - self.alpha) * self.Q[initialState, action_p, action_o] + \
			self.alpha * (reward + self.gamma * self.V[finalState])
		self.V[initialState] = self.updatePolicy(initialState)  
		self.alpha = self.alpha * self.decay


	def updatePolicy(self, state, retry=False):

		numActionsB, numActionsA = len(self.actions), len(self.actions)
		c = np.zeros(numActionsA + 1)
		c[0] = -1
		A_ub = np.ones((numActionsB, numActionsA + 1))
		A_ub[:, 1:] = [[-1 * self.Q[state, a, o] for a in self.actions] for o in self.actions]
		b_ub = np.zeros(numActionsB)
		A_eq = np.ones((1, numActionsA + 1))
		A_eq[0, 0] = 0
		b_eq = [1]
		bounds = ((None, None),) + ((0, 1),) * numActionsA
		res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

		if res.success: # and self.satisfyBound(res.x[1:])
			# le = res.x[1:]
			# self.normalPi(state, le)
			self.updatePi(state, self.modifyProb(res.x[1:], state))
		elif not retry:
			return self.updatePolicy(state, retry=True)
		else:
			return self.V[state]
		return res.x[0]
	

	def satisfyBound(self, le):
		for i in range(len(le)):
			if le[i] < 0:
				return False
		return True

	def modifyProb(self, probRes, state):
		start = False
		listLen = 1
		matchList = [math.inf] * len(self.actions)
		result = [0] * len(self.actions)

		if 1 in probRes:
			for i in range(len(probRes)):
				newList = list(self.Q[state, self.actions[i], o] for o in self.actions)
				if start == True and newList == matchList:
					result[i] = 1
				if probRes[i] == 1:
					result[i] = 1
					matchList = list(self.Q[state, self.actions[i], o] for o in self.actions)
					start = True

		for j in range(len(probRes)):
			if result[j] == 1:
				probRes[j] = 1/sum(result)
		return probRes


	def updatePi(self, state, probRes):

		for i in range(len(self.actions)):
			self.pi[state, self.actions[i]] = probRes[i]

	def updateState(self, new_state):

		self.current_state = new_state

	