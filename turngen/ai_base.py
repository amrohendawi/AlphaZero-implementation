from turn import Turn

class ai_base:
	# color is 0 for white or 1 for black
	def __init__(self, player):
		self.player = player
		
		
	def calculateTurn(self, board):
		return Turn(0,0,1,1,True)
	
