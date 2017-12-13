from player import Player
import operator
import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import namedtuple 
import seaborn as sns
import pandas as pd 
from field import * 

## Record each independent game's scores for player and opponent respectively.
playerWin = [] 
opponentWin = []

for i in range(Trial):

	player = Player(player_goal[0], True, states, actions, playerQ, playerPi, player_start[0])
	opponent = Player(opponent_goal, False, states, actions, opponentQ, opponentPi, opponent_start[0])

	pWin = 0
	oWin = 0

	for j in range(Game):

		player.updateState(player_start[0])
		opponent.updateState(opponent_start[0])

		for k in range(Movement):

			p_current_state = player.current_state
			o_current_state = opponent.current_state

			if getGoal(player):
				pWin = pWin + 1
				break
			elif getGoal(opponent):
				oWin = oWin + 1
				break

			pAction = player.takeAction()
			oAction = opponent.takeAction()

			pState = newState(player, pAction)
			oState = newState(opponent, oAction)

			player.updateState(pState)
			opponent.updateState(oState)
			
			meetUp(player, opponent)

			pR = getReward(player, opponent)[0]
			oR = getReward(player, opponent)[1]

			player.updateQ(p_current_state, player.current_state, pAction, oAction, pR)
			opponent.updateQ(o_current_state, opponent.current_state, oAction, pAction, oR)

			player.updatePolicy(p_current_state)
			opponent.updatePolicy(o_current_state)


	playerWin.append(pWin)
	opponentWin.append(oWin)
	
	del player
	del opponent



# print('player = ', playerWin)
# print('opponent = ', opponentWin)

















