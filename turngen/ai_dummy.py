
from ai_base import ai_base
import game as g
import state as s
from random import randint
from turn import Turn

class ai_dummy(ai_base):
	def __init__(self, player):
		super().__init__(player)
		self.player = player
		self.game = g.Game()
	
	def calculateTurn(self, board):
		state = s.State(board, self.player)
		turnlist = self.game.turnlist(state)
		turn = turnlist[randint(0,len(turnlist)-1)]
		# translate turn back to turnobject
		x1 = ord(turn[0]) - ord('a')
		y1 = ord(turn[1]) - ord('1')
		# turn[2] ist '-'
		x2 = ord(turn[3]) - ord('a')
		y2 = ord(turn[4]) - ord('1')
		return Turn(x1,y1,x2,y2)
		