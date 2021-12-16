import tensorflow as tf
import numpy as np
import state as s
import game as g

from keras.models import Model
from keras.layers import *
from keras.utils.vis_utils import plot_model

# this is hacky, but we dont want every file in the same folder
import sys
sys.path.insert(0,'..')


class NeuralNet:
	def __init__(self):
		#NN initialization
		inputshape = Input((8,8,5))
		x = Conv2D (32,(3,3), padding = "same", activation = "relu")(inputshape)
		x = Conv2D (64,(3,3), activation = "relu")(x)
		
		# Output 1 -> Win propability
		out1 = Flatten()(x)
		out1 = Dense(32)(out1)
		out1 = Dense(1, activation = "softmax")(out1) # only 1 value

		# Output 2 -> Turns probability
		out2 = Conv2D(64,(3,3), activation = "relu")(x)
		out2 = Conv2D(128,(3,3), padding = "same", activation = "relu")(out2)
		out2 = Flatten()(out2)
#		out2 = Dense(512)(out2)
#		out2 = Dense(2048)(out2)
		# Exactly 64*9 = 576 outputs
		out2 = Dense(576, activation = "softmax")(out2)
		
		self.model = Model(inputshape, [out1,out2])
		self.model.compile(optimizer = "Adam", loss = "mean_squared_error")
		
		self.turnorder = [[(-1,0),(-1,1),(0,1),(1,1),(1,0),(-2,1),(-1,2),(1,2),(2,1)],
						[(-1,0),(-1,-1),(0,-1),(1,-1),(1,0),(-2,-1),(-1,-2),(1,-2),(2,-1)]]
		self.game = g.Game()
		
		
	def plot_model(self, filename):
		plot_model(self.model, to_file = filename, show_shapes=True, show_layer_names = True)
		
		
	def setupBoards(self,state):
		# Calculate Bitmaps from board (and potentially from the old boards)
		if state.player == 1: # black
			pawns = state.board == 4
			enemypawns = state.board == 1
			knights = (state.board == 5)|(state.board == 6)
			enemyknights = (state.board == 2)|(state.board == 3)
		else: # white
			pawns = state.board == 1
			enemypawns = state.board == 4
			knights = (state.board == 2)|(state.board == 3)
			enemyknights = (state.board == 5)|(state.board == 6)
		
		input = -np.ones([1,8,8,5])
		input[0,:,:,0] = pawns
		input[0,:,:,1] = enemypawns
		input[0,:,:,2] = knights
		input[0,:,:,3] = enemyknights
		input[0,:,:,4] = state.player
		return input
	
		
	def predict(self, state): # input is 8x8x5 array
							  # returns winvalue, turnprobability (without filtering)
		# Calculate Binary arrays from board
		input = self.setupBoards(state)
		
		# run actual NN
		ret = self.model.predict(input)
		win = ret[0][0][0] # win probablity
		rawpolicy = ret[1][0]
		
		#normalize win probability to [-1,1]
		win = win*2-1

		# Get all valid Turns with a turngen
		fromX, fromY, toX, toY = self.game.turnlistasArray(state)
		# Turn 
		# Array mit 64 Startpositionen und von jeder 3 Möglichkeiten 
		# mit Bauern sich zu bewegen, 2 mit Bauern zu schlagen und 
		# 4 mit Springern zu springen, also insgesamt 64*(3+2+4)
		# = 540 Einträge (davon sind etwa 406 überhaupt möglich und bleiben
		# auf dem Board, die anderen sind nur beinhaltet, damit wir einfach
		# den index ausrechnen können)
		# Diese müssen anschließend gefiltert werden, sodass nur noch
		# legale Züge eine Wahrscheinlichkeit > 0 haben

		policy = np.zeros_like(rawpolicy)
		for i in range(len(fromX)):
			ind = fromX[i]*9*8 + fromY[i]*9 + self.turnorder[state.player].index((toX[i]-fromX[i], toY[i]-fromY[i]))
			policy[ind] = rawpolicy[ind]
		return win, policy/np.sum(policy)
		


