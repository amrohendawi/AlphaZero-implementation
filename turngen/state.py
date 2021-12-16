import numpy as np

class State:

    def __init__(self, board, player):
        self.board = board
        self.player = player

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return np.array_equal(self.board, other.board) & (self.player == other.player)
        else:
            return False

    def key(self):
        return (tuple(self.board.flatten()), self.player);

    def __hash__(self):
        return hash(self.key())

    def nextPlayer(self):
        return ((self.player+1)%2)