import game as g 
import state as s
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap 
import pygame,sys,random
from pygame.locals import *

##################### pygame GUI ################
########### initial parameters for printing the board
pygame.init()
win_score=0
lose_score=0
draw_score=0

tab_pos=[[],[],[],[],[],[],[],[]]

screen = pygame.display.set_mode((640, 480),RESIZABLE) #add RESIZABLE ou FULLSCREEN
pygame.display.set_icon(pygame.image.load("images/icon.png"))
pygame.display.set_caption("Jump Sturdy")
board_img = pygame.image.load("images/board_img.png").convert()

## still under construction: colors for showing which positions are allowed for a piece to move
green_light = pygame.image.load("images/green_light.png").convert()
red_light = pygame.image.load("images/red_light.png").convert()
green_light.set_colorkey((255,255,255))
red_light.set_colorkey((255,255,255))

# pieces
scaled_sheet=pygame.transform.scale(pygame.image.load("images/main_pieces.png").convert_alpha(),(200,50)).convert_alpha()
scaled_sheet2=pygame.transform.scale(pygame.image.load("images/main_pieces.png").convert_alpha(),(200,50)).convert_alpha()
red=scaled_sheet.subsurface(50,0,50,50).convert_alpha()
white=scaled_sheet.subsurface(0,0,50,50).convert_alpha()
two_white=scaled_sheet.subsurface(150,0,50,50).convert_alpha()
two_red=scaled_sheet.subsurface(100,0,50,50).convert_alpha()
red_white=scaled_sheet2.subsurface(150,0,50,50).convert_alpha()
white_red=scaled_sheet2.subsurface(100,0,50,50).convert_alpha()

board_pos=(100,10)

##################### pygame GUI ################

class Manager:
	# Werte der Felder:
	# 0 -> Leer
	# 1 -> Bauer Farbe 0 (white)
	# 2 -> Springer ww
	# 3 -> Springer bw
	# 4 -> Bauer Farbe 1 (white)
	# 5 -> Springer bb
	# 6 -> Springer wb
	# -1 -> Verbotenes/nicht definiertes Feld
	def Reset(self):
		self.nextPlayer = 0
		self.gameNotWon = True
		self.winner = -1
		self.board = np.array([[-1, 1, 1, 1, 1, 1, 1, -1],
                               [0, 1, 1, 1, 1, 1, 1, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 4, 4, 4, 4, 4, 4, 0],
                               [-1, 4, 4, 4, 4, 4, 4, -1]])

	def initCheckWon(self):
		self.player0won = np.zeros((8, 8), dtype=bool)
		self.player0won[7, :] = 1
		self.player1won = np.zeros((8, 8), dtype=bool)
		self.player1won[0, :] = 1

	def initExecuteTurn(self):
		self.exTransFrom = np.array([0, 0, 1, 4, 0, 4, 1, -1])
		self.exTransTo = np.array([[1, 2, 0, 0, 1, 3, 2, -1], [4, 4, 6, 5, 5, 0, 0, -1]])

	def initCheckTurn(self):
		self.legalTarget = np.array(
        		[[[0, 1, 1], [4, 5, 6]], [[0, 4, 4], [1, 2, 3]]])  # ([[[whiteMove],[whiteHit]],[[blackMove],[blackHit]]])
		self.legalMovePawn = [[(1, 0), (0, 1), (0, -1)], [(-1, 0), (0, 1), (0, -1)]]
		self.legalMovePawnHit = [[(1, 1), (1, -1)], [(-1, 1), (-1, -1)]]
		self.legalMoveKnight = [[(1, 2), (1, -2), (2, 1), (2, -1)], [(-1, -2), (-1, 2), (-2, -1), (-2, 1)]]
	
	def initPlot(self):
		# this will set board coords for printing reasons
		x=board_pos[0]+20;y=board_pos[1]+20
		for i in range(8):
			for j in range(8):
				tab_pos[i].append([x,y])
				x+=50
			y+=50
			x=board_pos[0]+20
		##### 
	def __init__(self, ai1, ai2, debug = False, initialstate = None, delay = 1.0):
		self.game = g.Game()
		self.state = self.game.getStartConfig()
		if initialstate:
			self.state = initialstate
		self.finished = self.game.CheckWon(self.state)
		self.winner = -1
		if self.finished:
			self.winner = self.state.nextPlayer()
		self.ai = []
		self.ai.append(ai1)
		self.ai.append(ai2)
		self.Reset()
		self.debug = debug
		self.delay = delay
		if(self.debug):
			self.initPlot()

	def Win(self, reason):
#		if self.debug:
		self.winner = self.state.nextPlayer()
		self.finished = True
		print("Player" + str(self.winner) + " has won because: " + reason)

	def run_bot_vs_bot(self):
		if self.debug:
			self.showBoard()
		while not self.finished:
			start = time.time()
			turn = self.ai[self.state.player].calculateTurn(self.state.board)
			print("turn is ")
			print(turn)
			end = time.time()
			print("AI" + str(self.state.nextPlayer()) + " does " + str(turn) +" and took {:.4f}".format(end-start) + " Seconds to calculate that")
			if turn.give_up:
				self.Win("gave up... base ai?")
				break
			if end-start > 1: # took to long, so forfeit
				self.Win("time ran out for opposing player")
				break
			if self.game.CheckTurn(self.state, turn):
				self.state = self.game.ExecuteTurn(self.state, turn)
			else:  # Illegal Turn = forfeit
				self.Win("illegal move from opposing player")
				break
			if self.game.CheckWon(self.state):
				self.Win("superior skill")
			if self.debug:
				self.showBoard()
		print("we have a winner: ", self.winner)
#		print(" Final Board: ")
		self.printBoard()

	def run_human_vs_bot(self):
		if self.debug:
			self.showBoard()
		while not self.finished:
			player_type = self.ai[self.nextPlayer]
	        # Human_case
			if isinstance(player_type, HumanPlayer):
				print("Human")
				# command line input
				if player_type.input_mode == 0:
					start = time.time()
					turn = player_type.command_line_input()
					print("turn is ")
					print(turn)
					end = time.time()
					if turn.give_up:
						self.Win("gave up... base ai?")
					if self.game.CheckTurn(self.state, turn):
						self.state = self.game.ExecuteTurn(self.state, turn)
						self.nextPlayer = (self.nextPlayer + 1) % 2
					else:  # Illegal Turn = forfeit
						self.Win("illegal move from opposing player")
						break
					if self.game.CheckWon(self.state):
						self.Win("human wins")
					if self.debug:
						self.showBoard()
	        # Bot_case
			else:
				start = time.time()
				turn = self.ai[self.nextPlayer].calculateTurn(self.board)
				end = time.time()
				print("AI" + str(self.nextPlayer + 1) + " does " + str(turn) + " and took " + str(
	                end - start) + " Seconds to calculate that")
				if turn.give_up:
					self.Win("gave up... base ai?")
				if end - start > 1:  # took to long, so forfeit
					self.Win("time ran out for opposing player")
					break
				if self.game.CheckTurn(self.state, turn):
					self.state = self.game.ExecuteTurn(self.state, turn)
					self.nextPlayer = (self.nextPlayer + 1) % 2
				else:  # Illegal Turn = forfeit
					self.Win("illegal move from opposing player")
					break
				if self.game.CheckWon(self.state):
					self.Win("bot wins")
				if self.debug:
					self.showBoard()



	def printBoard(self):
		print(np.flip(self.state.board,0))
	
	def showBoard(self):
		screen.fill((204,204,204))
		screen.blit(board_img,board_pos)
		for i in range(8):
			for j in range(8):
				pos=tab_pos[i][j]
				if self.state.board[i,j]==1:screen.blit(white,pos)
				elif self.state.board[i,j]==2:screen.blit(two_white,pos)
				elif self.state.board[i,j]==3:screen.blit(red_white,pos)
				elif self.state.board[i,j]==4 :screen.blit(red,pos)
				elif self.state.board[i,j]==5:screen.blit(two_red,pos)
				elif self.state.board[i,j]==6:screen.blit(white_red,pos)
				
		font=pygame.font.SysFont('Arial', 30)

		text=font.render(("lose:"), True, (162,1,35));screen.blit(text,(550,60))
		text=font.render((str(lose_score)), True, (162,1,35));screen.blit(text,(550,90))  
		text=font.render(("win:"), True, (32,75,106));screen.blit(text,(550,0))
		text=font.render((str(win_score)), True, (32,75,106));screen.blit(text,(550,30))
		text=font.render(("draw:"), True, (145,130,0));screen.blit(text,(550,120))
		text=font.render((str(draw_score)), True, (145,130,0));screen.blit(text,(550,150))
		text=font.render(("8"), True, (0,0,0));screen.blit(text,(70,50))
		text=font.render(("7"), True, (0,0,0));screen.blit(text,(70,100))
		text=font.render(("6"), True, (0,0,0));screen.blit(text,(70,150))
		text=font.render(("5"), True, (0,0,0));screen.blit(text,(70,200))
		text=font.render(("4"), True, (0,0,0));screen.blit(text,(70,250))
		text=font.render(("3"), True, (0,0,0));screen.blit(text,(70,300))
		text=font.render(("2"), True, (0,0,0));screen.blit(text,(70,350))
		text=font.render(("1"), True, (0,0,0));screen.blit(text,(70,400))
		text=font.render(("A     B     C     D     E     F     G     H"), True, (0,0,0));screen.blit(text,(130,450))
		pygame.display.update()
		pygame.display.flip()
		time.sleep(self.delay/4)
	

from ai_dummy import ai_dummy
from human_player import HumanPlayer

if __name__== "__main__":
	gamemode = -1
	print("OPTIONS: \n 0) (Human vs Bot) \n 1) (Bot vs Bot) \n")

	while gamemode not in [0, 1]:
		try:
			gamemode = int(input("select 0/1."))
		except:
			print("That's not a valid option!")

	if int(gamemode) == 0:
        # select color for human here or add input option at start
		human = HumanPlayer(0)
		ai1 = ai_dummy(0 if human.player == 1 else 1)
		game = Manager(human, ai1, True)
		game.run_human_vs_bot()

	elif int(gamemode) == 1:
		ai1 = ai_dummy(0)
		ai2 = ai_dummy(1)
		gameManager = Manager(ai1, ai2, True)
		gameManager.run_bot_vs_bot()
		input("Press Enter to continue...")
