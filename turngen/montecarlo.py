# https://github.com/suragnair/alpha-zero-general/blob/master/MCTS.py
import game as g
import state as s 
import numpy as np
import alphazero.NeuralNet
import turn 
import math

class MCTS:

	def __init__(self, cpuct):
		self.game = g.Game()
		self.visits = {}
		self.vact = {}
		self.actions = {}
		self.Q = {}
		self.cpuct = cpuct

	def search(self, state, nnet):
		if self.game.CheckWon(state): return -1

		if state not in self.visits:
			self.visits[state] = 0
			v, self.actions[state] = nnet.predict(state)
			return -v
			
		curr_best =  -float('inf')
		best_act =  -1
		for i in range(576):
			if self.actions[state][i] != 0:
				if (state, i) in self.Q:
					curr = self.Q[(state, i)] + self.cpuct * self.actions[state][i] * math.sqrt(self.visits[state]) / (1 + self.vact[(state, i)])
				else:
					curr = self.cpuct * self.actions[state][i] * math.sqrt(self.visits[state]) / (1 + self.vact[(state, i)])
				
				if curr > curr_best:
					curr_best = curr
					best_act = i

		i = best_act
		
		trn = self.game.calculateTurnFromIndex(i, state.player)
		nxt = self.game.ExecuteTurn(state, trn) 
		
		v = self.search(nxt, nnet)

		if (state, i) in self.Q:
			self.Q[(state,i)] = (self.vact[(state,i)]*self.Q[(state,i)] + v) / (self.vact[(state,i)] + 1)
			self.vact[(state, i)] += 1

		else:
			self.Q[(state, i)] = v
			self.vact[(state, i)] = 1

		self.visits[state] += 1
		return -v

