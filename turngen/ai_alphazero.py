import state as s
import numpy as np
import game as g
import turn as t
from ai_base import ai_base
from turngen import TurnGen
from alphazero.NeuralNet import NeuralNet

class ai_alphazero(ai_base):
	def __init__(self, player):
		super().__init__(player)
		self.NN = NeuralNet()
		self.game = g.Game()

	
	def loadAI(self, file):
		#do things
		print("loaded ai (not)")
	
			
	
	def calculateTurn(self, board):
		state = s.State(board, self.player)
		_, turns = self.NN.predict(state)

		index = turns.index(np.amax(turns))
		trn = self.game.calculateTurnFromIndex(index, self.player)
		
		return trn
		