import montecarlo as mc
import state as s
import numpy as np
import alphazero.NeuralNet as nn


def main():
    monteCarlo = mc.MCTS(2)
    nnet = nn.NeuralNet()
    board = np.array([ -1, 1, 1, 1, 1, 1, 1,-1,
                        0, 1, 1, 1, 1, 1, 1, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0,
                        0, 4, 4, 4, 4, 4, 4, 0,
                        -1, 4, 4, 4, 4, 4, 4,-1]).reshape(8, 8)
    player = 0
    state = s.State(board, player)

    turn = monteCarlo.search(state, nnet)
    print(turn)
        

if __name__ == "__main__":
    main()