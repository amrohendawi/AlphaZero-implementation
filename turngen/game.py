import time
import numpy as np
import state as s
import shift

class Game:

	# Werte der Felder:
	# 0 -> Leer
	# 1 -> Bauer Farbe 0 (white)
	# 2 -> Springer ww
	# 3 -> Springer bw
	# 4 -> Bauer Farbe 1 (white)
	# 5 -> Springer bb
	# 6 -> Springer wb
	# -1 -> Verbotenes/nicht definiertes Feld
	
	def initCheckWon(self):
		self.player0won = np.zeros((8,8), dtype = bool)
		self.player0won[7,:] = 1
		self.player1won = np.zeros((8,8), dtype = bool)
		self.player1won[0,:] = 1

	def initExecuteTurn(self):
		self.exTransFrom = np.array([0,0,1,4,0,4,1,-1])
		self.exTransTo = np.array([[1,2,0,0,1,3,2,-1],[4,4,6,5,5,0,0,-1]])

	def initCheckTurn(self):
		self.legalTarget = np.array([[[0,1,1],[4,5,6]],[[0,4,4],[1,2,3]]]) #([[[whiteMove],[whiteHit]],[[blackMove],[blackHit]]]) 
		self.legalMovePawn = [[(1,0),(0,1),(0,-1)],[(-1,0),(0,1),(0,-1)]]
		self.legalMovePawnHit = [[(1,1),(1,-1)],[(-1,1),(-1,-1)]]
		self.legalMoveKnight = [[(1,2),(1,-2),(2,1),(2,-1)],[(-1,-2),(-1,2),(-2,-1),(-2,1)]]

	def initTurnGenerator(self):
		self.names = np.array([["a1","b1","c1","d1","e1","f1","g1","h1"],
								["a2","b2","c2","d2","e2","f2","g2","h2"],
								["a3","b3","c3","d3","e3","f3","g3","h3"],
								["a4","b4","c4","d4","e4","f4","g4","h4"],
								["a5","b5","c5","d5","e5","f5","g5","h5"],
								["a6","b6","c6","d6","e6","f6","g6","h6"],
								["a7","b7","c7","d7","e7","f7","g7","h7"],
								["a8","b8","c8","d8","e8","f8","g8","h8"]])
		self.X = np.array([[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],
						[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7]])
		self.Y = np.array([[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,2,2,2,2,2,2,2],[3,3,3,3,3,3,3,3],
						[4,4,4,4,4,4,4,4],[5,5,5,5,5,5,5,5],[6,6,6,6,6,6,6,6],[7,7,7,7,7,7,7,7]])


	def __init__(self):
		# Helpers for CheckWon
		self.initCheckWon()
		# Helpers for ExecuteTurn
		self.initExecuteTurn()
		#Helpers for CheckTurn
		self.initCheckTurn()
		#Helpers fpr Tungenerator
		self.initTurnGenerator()

		self.names = np.array([["a1","b1","c1","d1","e1","f1","g1","h1"],
								["a2","b2","c2","d2","e2","f2","g2","h2"],
								["a3","b3","c3","d3","e3","f3","g3","h3"],
								["a4","b4","c4","d4","e4","f4","g4","h4"],
								["a5","b5","c5","d5","e5","f5","g5","h5"],
								["a6","b6","c6","d6","e6","f6","g6","h6"],
								["a7","b7","c7","d7","e7","f7","g7","h7"],
								["a8","b8","c8","d8","e8","f8","g8","h8"]])
		self.X = np.array([[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],
						[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7],[0,1,2,3,4,5,6,7]])
		self.Y = np.array([[0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1],[2,2,2,2,2,2,2,2],[3,3,3,3,3,3,3,3],
						[4,4,4,4,4,4,4,4],[5,5,5,5,5,5,5,5],[6,6,6,6,6,6,6,6],[7,7,7,7,7,7,7,7]])


	def printBoard(self, state):
		print(np.flip(state.board,0))


	def getStartConfig(self):
		board = np.array([[-1,1,1,1,1,1,1,-1],
							[0,1,1,1,1,1,1,0],
							[0,0,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,0],
							[0,4,4,4,4,4,4,0],
							[-1,4,4,4,4,4,4,-1]])
		player = 0
		state = s.State(board, player)
		return state
	


	def CheckTurn(self, state, turn):
		start = state.board[turn.from_y, turn.from_x]
		target = state.board[turn.to_y, turn.to_x]
		color = int(4<=start<=6)

		#check start
		if color != state.player:
			return False

		#check move
		deltaY = turn.to_y - turn.from_y
		deltaX = turn.to_x - turn.from_x
		kind =[0]
		if (deltaY,deltaX) in self.legalMovePawn[color]:
			kind = [0]
		elif (deltaY,deltaX) in self.legalMovePawnHit[color]:
			kind = [1]
		elif (deltaY,deltaX) in self.legalMoveKnight[color]:
			kind = [0,1]
		else :
			return False

		#check target
		if target not in self.legalTarget[color,kind,:]:
			return False

		return True
	
	
	def ExecuteTurn(self, state, turn):
		# remove piece at from
		start = state.board[turn.from_y, turn.from_x]
		target = state.board[turn.to_y, turn.to_x]
		color = int(4<=start<=6)

		newState = s.State(state.board, state.nextPlayer())
		newState.board[turn.from_y, turn.from_x] = self.exTransFrom[start]
		newState.board[turn.to_y, turn.to_x] = self.exTransTo[color, target]

		return newState
	
	
	def CheckWon(self, state):
		if np.any((state.board <= 3) & (state.board >= 1) & self.player0won):
			return True
		if np.any((state.board <= 6) & (state.board >= 4) & self.player1won):
			return True
		return False
	
	


	################ TURN GENERATOR ################

	# returns a list of all possible turns for color
	# color is either 0(w) or 1(b)
	def turnlist(self, state):
		return np.append(self.pawnMoves(state),self.knightMoves(state))
	
	def turnlistasArray(self, state):
		a,b,c,d = self.pawnMovesArray(state)
		A,B,C,D = self.knightMovesArray(state)
		return np.append(a,A), np.append(b,B), np.append(c,C), np.append(d,D)
	
	def pawnMovesArray(self, state):
		if state.player == 1: # black
			pawnBoard = state.board == 4
			enemyBoard = (state.board <= 3) & (state.board >= 1)
			updown = -1 # von oben nach unten (invertiert)
		elif state.player == 0: # white
			pawnBoard = state.board == 1
			enemyBoard = (state.board <= 6) & (state.board >= 4)
			updown = 1 # von unten nach oben (normal)

		#MOVES
		targetBoard = pawnBoard | (state.board == 0)

		#pawn moves right
		pawnTargetBoard = shift.shiftright(pawnBoard,1) & targetBoard
		pawnStartBoard = shift.shiftleft(pawnTargetBoard,1)

		fromX = self.X[pawnStartBoard]
		fromY = self.Y[pawnStartBoard]
		toX = self.X[pawnTargetBoard]
		toY = self.Y[pawnTargetBoard]

		#pawn moves left
		pawnTargetBoard = shift.shiftleft(pawnBoard,1) & targetBoard
		pawnStartBoard = shift.shiftright(pawnTargetBoard,1)

		fromX = np.append(fromX, self.X[pawnStartBoard])
		fromY = np.append(fromY, self.Y[pawnStartBoard])
		toX = np.append(toX, self.X[pawnTargetBoard])
		toY = np.append(toY, self.Y[pawnTargetBoard])

		#pawn moves up
		pawnTargetBoard = shift.shiftup(pawnBoard,updown) & targetBoard
		pawnStartBoard = shift.shiftdown(pawnTargetBoard,updown)

		fromX = np.append(fromX, self.X[pawnStartBoard])
		fromY = np.append(fromY, self.Y[pawnStartBoard])
		toX = np.append(toX, self.X[pawnTargetBoard])
		toY = np.append(toY, self.Y[pawnTargetBoard])

		#CAPTURES
		targetBoard = enemyBoard

		#pawn captures up right
		pawnTargetBoard = shift.shift2(pawnBoard,1,updown) & targetBoard
		pawnStartBoard = shift.shift2(pawnTargetBoard,-1,-updown)

		fromX = np.append(fromX, self.X[pawnStartBoard])
		fromY = np.append(fromY, self.Y[pawnStartBoard])
		toX = np.append(toX, self.X[pawnTargetBoard])
		toY = np.append(toY, self.Y[pawnTargetBoard])

		#pawn captures up left
		pawnTargetBoard = shift.shift2(pawnBoard, -1, updown) & targetBoard
		pawnStartBoard = shift.shift2(pawnTargetBoard, 1, -updown)

		fromX = np.append(fromX, self.X[pawnStartBoard])
		fromY = np.append(fromY, self.Y[pawnStartBoard])
		toX = np.append(toX, self.X[pawnTargetBoard])
		toY = np.append(toY, self.Y[pawnTargetBoard])

		return fromX, fromY, toX, toY


	def pawnMoves(self, state):
		if state.player == 1: # black
			pawnBoard = state.board == 4
			enemyBoard = (state.board <= 3) & (state.board >= 1)
			updown = -1 # von oben nach unten (invertiert)
		elif state.player == 0: # white
			pawnBoard = state.board == 1
			enemyBoard = (state.board <= 6) & (state.board >= 4)
			updown = 1 # von unten nach oben (normal)

		#MOVES
		targetBoard = pawnBoard | (state.board == 0)

		#pawn moves right
		pawnTargetBoard = shift.shiftright(pawnBoard,1) & targetBoard
		pawnStartBoard = shift.shiftleft(pawnTargetBoard,1)

		moves = np.core.defchararray.add(self.names[pawnStartBoard], np.core.defchararray.add('-', self.names[pawnTargetBoard]))

		#pawn moves left
		pawnTargetBoard = shift.shiftleft(pawnBoard,1) & targetBoard
		pawnStartBoard = shift.shiftright(pawnTargetBoard,1)

		moves = np.append(moves, np.core.defchararray.add(self.names[pawnStartBoard], np.core.defchararray.add('-', self.names[pawnTargetBoard])))
		
		#pawn moves up
		pawnTargetBoard = shift.shiftup(pawnBoard,updown) & targetBoard
		pawnStartBoard = shift.shiftdown(pawnTargetBoard,updown)

		moves = np.append(moves, np.core.defchararray.add(self.names[pawnStartBoard], np.core.defchararray.add('-', self.names[pawnTargetBoard]))) 

		#CAPTURES
		targetBoard = enemyBoard

		#pawn captures up right
		pawnTargetBoard = shift.shift2(pawnBoard,1,updown) & targetBoard
		pawnStartBoard = shift.shift2(pawnTargetBoard,-1,-updown)

		moves = np.append(moves, np.core.defchararray.add(self.names[pawnStartBoard], np.core.defchararray.add('-', self.names[pawnTargetBoard]))) 

		#pawn captures up left
		pawnTargetBoard = shift.shift2(pawnBoard, -1, updown) & targetBoard
		pawnStartBoard = shift.shift2(pawnTargetBoard, 1, -updown)

		moves = np.append(moves, np.core.defchararray.add(self.names[pawnStartBoard], np.core.defchararray.add('-', self.names[pawnTargetBoard]))) 

		return moves

	def knightMoves(self, state):
		if state.player == 1: # black
			pawnBoard = state.board == 4
			knightBoard = (state.board == 5) | (state.board == 6) 
			enemyBoard = (state.board <= 3) & (state.board >= 1)
			updown = -1 
		elif state.player == 0: # white
			pawnBoard = state.board == 4
			knightBoard = (state.board == 3) | (state.board == 2)
			enemyBoard = (state.board <= 6) & (state.board >= 4)
			updown = 1

		targetBoard = pawnBoard | enemyBoard | (state.board == 0)

		#knight moves right right up
		knightTargetBoard = shift.shift2(knightBoard, 2, updown) & targetBoard
		knightStartBoard = shift.shift2(knightTargetBoard, -2, -updown)

		moves = np.core.defchararray.add(self.names[knightStartBoard], np.core.defchararray.add('-', self.names[knightTargetBoard]))

		#knight moves right up up
		knightTargetBoard = shift.shift2(knightBoard, 1, 2*updown) & targetBoard
		knightStartBoard = shift.shift2(knightTargetBoard, -1, -2*updown)

		moves = np.append(moves, np.core.defchararray.add(self.names[knightStartBoard], np.core.defchararray.add('-', self.names[knightTargetBoard]))) 


		#knight moves left up up
		knightTargetBoard = shift.shift2(knightBoard, -1, 2*updown) & targetBoard
		knightStartBoard = shift.shift2(knightTargetBoard, 1, -2*updown)

		moves = np.append(moves, np.core.defchararray.add(self.names[knightStartBoard], np.core.defchararray.add('-', self.names[knightTargetBoard])))


		#knight moves left left up
		knightTargetBoard = shift.shift2(knightBoard, -2, updown) & targetBoard
		knightStartBoard = shift.shift2(knightTargetBoard, 2, -updown)

		moves = np.append(moves, np.core.defchararray.add(self.names[knightStartBoard], np.core.defchararray.add('-', self.names[knightTargetBoard])))

		return moves

	def knightMovesArray(self, state):
		if state.player == 1: # black
			pawnBoard = state.board == 4
			knightBoard = (state.board == 5) | (state.board == 6) 
			enemyBoard = (state.board <= 3) & (state.board >= 1)
			updown = -1 
		elif state.player == 0: # white
			pawnBoard = state.board == 4
			knightBoard = (state.board == 3) | (state.board == 2)
			enemyBoard = (state.board <= 6) & (state.board >= 4)
			updown = 1

		targetBoard = pawnBoard | enemyBoard | (state.board == 0)

		#knight moves right right up
		knightTargetBoard = shift.shift2(knightBoard, 2, updown) & targetBoard
		knightStartBoard = shift.shift2(knightTargetBoard, -2, -updown)

		fromX = self.X[knightStartBoard]
		fromY = self.Y[knightStartBoard]
		toX = self.X[knightTargetBoard]
		toY = self.Y[knightTargetBoard]

		#knight moves right up up
		knightTargetBoard = shift.shift2(knightBoard, 1, 2*updown) & targetBoard
		knightStartBoard = shift.shift2(knightTargetBoard, -1, -2*updown)

		fromX = np.append(fromX, self.X[knightStartBoard])
		fromY = np.append(fromY, self.Y[knightStartBoard])
		toX = np.append(toX, self.X[knightTargetBoard])
		toY = np.append(toY, self.Y[knightTargetBoard])

		#knight moves left up up
		knightTargetBoard = shift.shift2(knightBoard, -1, 2*updown) & targetBoard
		knightStartBoard = shift.shift2(knightTargetBoard, 1, -2*updown)

		fromX = np.append(fromX, self.X[knightStartBoard])
		fromY = np.append(fromY, self.Y[knightStartBoard])
		toX = np.append(toX, self.X[knightTargetBoard])
		toY = np.append(toY, self.Y[knightTargetBoard])

		#knight moves left left up
		knightTargetBoard = shift.shift2(knightBoard, -2, updown) & targetBoard
		knightStartBoard = shift.shift2(knightTargetBoard, 2, -updown)

		fromX = np.append(fromX, self.X[knightStartBoard])
		fromY = np.append(fromY, self.Y[knightStartBoard])
		toX = np.append(toX, self.X[knightTargetBoard])
		toY = np.append(toY, self.Y[knightTargetBoard])

		return fromX, fromY, toX, toY
	


	





