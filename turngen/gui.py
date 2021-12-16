'''
Developed by: Frederico Jordan

@author: fvj
'''
import pygame, chess
from random import choice
from traceback import format_exc
from sys import stderr
from time import strftime
from copy import deepcopy
pygame.init()

SQUARE_SIDE = 40
AI_SEARCH_DEPTH = 2

WHITE              = (255, 255, 255)
BLACK              = (10, 50, 50)
LICHESS_LIGHT      = (90, 250, 180)


WHITE_PAWN   = pygame.image.load('images/white.png')
RED_PAWN   = pygame.image.load('images/red.png')
WHITE_KNIGHT = pygame.image.load('images/two_white.png')
RED_KNIGHT = pygame.image.load('images/two_white.png')
WHITE_RED_KNIGHT = pygame.image.load('images/white_red.png')
RED_WHITE_KNIGHT = pygame.image.load('images/red_white.png')

CLOCK = pygame.time.Clock()
CLOCK_TICK = 15

SCREEN = pygame.display.set_mode((8*SQUARE_SIDE, 8*SQUARE_SIDE), pygame.RESIZABLE)
SCREEN_TITLE = 'Jump-Sturdy Game'

pygame.display.set_icon(pygame.image.load('images/jumpSturdy_icon.png'))
pygame.display.set_caption(SCREEN_TITLE)

def resize_screen(square_side_len):
    global SQUARE_SIDE
    global SCREEN
    SCREEN = pygame.display.set_mode((8*square_side_len, 8*square_side_len), pygame.RESIZABLE)
    SQUARE_SIDE = square_side_len

def print_empty_board():
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN,BLACK,(50,50,50,40))
    paint_dark_squares(BLACK)
    
def paint_dark_squares(square_color):
    for position in chess.single_gen(chess.LIGHT_SQUARES):
        paint_square(chess.bb2str(position), square_color)
    for position in chess.single_gen(chess.DARK_SQUARES):
        paint_square(chess.bb2str(position), square_color)
        
def paint_square(square, square_color):
    col = chess.FILES.index(square[0])
    row = 7-chess.RANKS.index(square[1])
    if not ((col == 7 and row == 7) or (col == 7 and row == 0) or (col == 0 and row == 7) or (col == 0 and row == 0)):
        pygame.draw.rect(SCREEN, square_color, (SQUARE_SIDE*col,SQUARE_SIDE*row,SQUARE_SIDE,SQUARE_SIDE), 3)
        pygame.draw.rect(SCREEN, LICHESS_LIGHT, (SQUARE_SIDE*col,SQUARE_SIDE*row,SQUARE_SIDE,SQUARE_SIDE), 0)
        
def get_square_rect(square):
    col = chess.FILES.index(square[0])
    row = 7-chess.RANKS.index(square[1])
    return pygame.Rect((col*SQUARE_SIDE, row*SQUARE_SIDE), (SQUARE_SIDE,SQUARE_SIDE))

def coord2str(position, color=chess.WHITE):
    if color == chess.WHITE:
        file_index = int(position[0]/SQUARE_SIDE)
        rank_index = 7 - int(position[1]/SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]
    if color == chess.BLACK:
        file_index = 7 - int(position[0]/SQUARE_SIDE)
        rank_index = int(position[1]/SQUARE_SIDE)
        return chess.FILES[file_index] + chess.RANKS[rank_index]
    
def printBoard(board, color=chess.WHITE):
    printed_board = board
    
    print_empty_board()
    
    for position in chess.colored_piece_gen(printed_board, chess.PAWN, chess.BLACK):
        SCREEN.blit(pygame.transform.scale(RED_PAWN,   (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
    for position in chess.colored_piece_gen(printed_board, chess.PAWN, chess.WHITE):
        SCREEN.blit(pygame.transform.scale(WHITE_PAWN,   (SQUARE_SIDE,SQUARE_SIDE)), get_square_rect(chess.bb2str(position)))
        
    pygame.display.flip()
    
def set_title(title):
    pygame.display.set_caption(title)
    pygame.display.flip()
    
def make_AI_move(game, color):
    set_title(SCREEN_TITLE + ' - Calculating move...')
    new_game = chess.make_move(game, chess.get_AI_move(game, AI_SEARCH_DEPTH))
    set_title(SCREEN_TITLE)
    printBoard(new_game.board, color)
    return new_game

def try_move(game, attempted_move):
    for move in chess.legal_moves(game, game.to_move):
        if move == attempted_move:
            game = chess.make_move(game, move)
    return game

def play_as(game, color):
    run = True
    ongoing = True
    
    try:
        while run:
            CLOCK.tick(CLOCK_TICK)
            printBoard(game.board, color)
            
            if chess.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
                ongoing = False
            
            if ongoing and game.to_move == chess.opposing_color(color):
                game = make_AI_move(game, color)
            
            if chess.game_ended(game):
                set_title(SCREEN_TITLE + ' - ' + chess.get_outcome(game))
                ongoing = False
             
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    leaving_square = coord2str(event.pos, color)
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    arriving_square = coord2str(event.pos, color)
                    
                    if ongoing and game.to_move == color:
                        move = (chess.str2bb(leaving_square), chess.str2bb(arriving_square))
                        game = try_move(game, move)
                        printBoard(game.board, color)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == 113:
                        run = False
                    if event.key == 104 and ongoing: # H key
                        game = make_AI_move(game, color)
                    if event.key == 117: # U key
                        game = chess.unmake_move(game)
                        game = chess.unmake_move(game)
                        set_title(SCREEN_TITLE)
                        printBoard(game.board, color)
                        ongoing = True
                    if event.key == 112 or event.key == 100: # P or D key
                        print(game.get_move_list() + '\n')
                        print('\n'.join(game.position_history))
                    if event.key == 101: # E key
                        print('eval = ' + str(chess.evaluate_game(game)/100))
                
                if event.type == pygame.VIDEORESIZE:
                    if SCREEN.get_height() != event.h:
                        resize_screen(int(event.h/8.0))
                    elif SCREEN.get_width() != event.w:
                        resize_screen(int(event.w/8.0))
                    printBoard(game.board, color)
    except:
        print(format_exc(), file=stderr)
        bug_file = open('bug_report.txt', 'a')
        bug_file.write('----- ' + strftime('%x %X') + ' -----\n')
        bug_file.write(format_exc())
        bug_file.write('\nPlaying as WHITE:\n\t' if color == chess.WHITE else '\nPlaying as BLACK:\n\t')
        bug_file.write(game.get_move_list() + '\n\t')
        bug_file.write('\n\t'.join(game.position_history))
        bug_file.write('\n-----------------------------\n\n')
        bug_file.close()

def play_as_white(game=chess.Game()):
    return play_as(game, chess.WHITE)

def play_as_black(game=chess.Game()):
    return play_as(game, chess.BLACK)

def play_random_color(game=chess.Game()):
    color = choice([chess.WHITE, chess.BLACK])
    play_as(game, color)

# chess.verbose = True
play_random_color()
