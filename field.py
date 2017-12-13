
import operator
import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import namedtuple 
import seaborn as sns
import pandas as pd 

## The Soccer Field basic info


####################################  Variables   ###########################################################
Trial = 2
Game = 30
Movement = 50
score = 1000

field = (9, 4)
states = [(x, y) for x in range(field[0]) for y in range(field[1])]
actions = [ (0, 1), (1, 0),(-1, 0), (0, -1)]

player_goal = ((-1, 1), (-1, 2))
opponent_goal = ((9, 1), (9, 2))

player_start = ((4, 2),(4, 1),(2, 2))
opponent_start = [(4, 3)]

front_field = (0, int(field[0]/3-1))
middle_field = (int(field[0]/3), int(2*field[0]/3-1))
back_field = (int(2*field[0]/3), int(field[0]))
subFields = {'front': front_field, 'middle': middle_field, 'back': back_field}


playerQ = {(state, p_action, o_action): 0 for state in states for p_action in actions for o_action in actions}
opponentQ = {(state, p_action, o_action): 0 for state in states for p_action in actions for o_action in actions}
playerPi = {(state, action): 1/len(actions) for state in states for action in actions}
opponentPi = {(state, action): 1/len(actions) for state in states for action in actions}


partition_r = 100
goal_r = 1000
w_p = 0.8
vare = 0.9



####################################  Functions   ###########################################################

def getGoal(player):

	if player.current_state in player.goal and player.ball:
		return True
	else:
		return False

def meetUp(player, opponent):
	if player.current_state == opponent.current_state:
		player.ball = not player.ball
		opponent.ball = not opponent.ball


def newState(player, action):
	new_s =  tuple(map(operator.add, player.current_state, action))
	if (new_s in player.states) or ((new_s in player.goal) and (player.ball == True)):
		return new_s
	else:
		return player.current_state
		
	
def getpartitionR(player):
	if player.subField != None:
		if player.current_state in subField[player.subField]:
			return partition_r  
		else:
			return 0
	else: 
		return 0

def underlyReward(player, opponent):  ## Return the (player.reward, opponent.reward)
	if (player.current_state in player_goal) and (player.ball == True) :
		return (goal_r, -goal_r)
		
	elif (opponent.current_state in opponent_goal) and (opponent.ball == True):
		return (-goal_r, goal_r)
	else:
		return (0, 0)

def getReward(player, opponent):
	p_under_r = underlyReward(player, opponent)[0]
	o_under_r = underlyReward(player, opponent)[1]
	p_r = (1- w_p)*p_under_r + w_p * getpartitionR(player)
	o_r = (1- w_p)*o_under_r + w_p * getpartitionR(opponent)
	return (p_r, o_r)







































