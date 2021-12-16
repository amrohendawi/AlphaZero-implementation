import unittest
import numpy as np
import turngen


class TestTurn(unittest.TestCase):

    def test_moves(self):

        # Base Case - White
        game = turngen.TurnGen()
        testBoard = np.array([-1, 1, 1, 1, 1, 1, 1, -1,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 4, 4, 4, 4, 4, 4, 0,
                              -1, 4, 4, 4, 4, 4, 4, -1]).reshape(8, 8)
        testMoves = ['b1-c1', 'c1-d1', 'd1-e1', 'e1-f1', 'f1-g1', 'b2-c2', 'c2-d2', 'd2-e2', 'e2-f2', 'f2-g2', 'g2-h2', 'c1-b1', 'd1-c1',
                     'e1-d1', 'f1-e1', 'g1-f1', 'b2-a2', 'c2-b2', 'd2-c2', 'e2-d2', 'f2-e2', 'g2-f2', 'b1-b2', 'c1-c2', 'd1-d2', 'e1-e2', 
                     'f1-f2', 'g1-g2', 'b2-b3', 'c2-c3', 'd2-d3', 'e2-e3', 'f2-f3', 'g2-g3']

        game.setBoard(testBoard)
        np.testing.assert_equal(sorted(game.pawnMoves(0)), sorted(testMoves))

        # Case with one knight - White
        testBoard = np.array([-1, 1, 0, 1, 1, 1, 1, -1,
                              0, 1, 2, 1, 1, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 4, 4, 4, 4, 4, 4, 0,
                              -1, 4, 4, 4, 4, 4, 4, -1]).reshape(8, 8)
        game.setBoard(testBoard)
        testMovesPawn = ['b1-c1', 'd1-e1', 'e1-f1', 'f1-g1', 'd2-e2', 'e2-f2', 'f2-g2', 'g2-h2', 'd1-c1',
                     'e1-d1', 'f1-e1', 'g1-f1', 'b2-a2', 'e2-d2', 'f2-e2', 'g2-f2',  'b1-b2', 'd1-d2', 
                     'e1-e2', 'f1-f2', 'g1-g2','b2-b3', 'd2-d3', 'e2-e3', 'f2-f3', 'g2-g3']
        testMovesKnight = ['c2-a3', 'c2-e3', 'c2-b4', 'c2-d4']

        np.testing.assert_equal(sorted(game.pawnMoves(0)), sorted(testMovesPawn))
        np.testing.assert_equal(sorted(game.knightMoves(0)), sorted(testMovesKnight))


        # Case with possible captures - White
        testBoard = np.array([-1, 1, 0, 1, 1, 1, 1, -1,
                              0, 1, 2, 1, 1, 1, 1, 0,
                              0, 0, 0, 0, 0, 4, 0, 0,
                              0, 0, 0, 5, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 4, 4, 0, 4, 0, 4, 0,
                              -1, 4, 4, 0, 4, 4, 4, -1]).reshape(8, 8)
        game.setBoard(testBoard)
        testPawnCaptures = ['e2-f3', 'e4-f3']
        testKnightCaptures = ['c2-d4']
        
        self.assertTrue((set(testPawnCaptures)).issubset(set(game.pawnMoves(0))))
        self.assertTrue((set(testKnightCaptures)).issubset(set(game.knightMoves(0))))
        
        #Base case - Black
        testBoard = np.array([-1, 1, 1, 1, 1, 1, 1, -1,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 4, 4, 4, 4, 4, 4, 0,
                              -1, 4, 4, 4, 4, 4, 4, -1]).reshape(8, 8)
        game.setBoard(testBoard)
        testMoves = [
            'b8-b7', 'c8-c7', 'd8-d7', 'e8-e7', 'f8-f7', 'g8-g7',
            'b7-b6', 'c7-c6', 'd7-d6', 'e7-e6', 'f7-f6', 'g7-g6',
            'b8-c8', 'c8-d8', 'd8-e8', 'e8-f8', 'f8-g8', 'g8-f8', 'f8-e8', 'e8-d8', 'd8-c8', 'c8-b8',
            'b7-c7', 'c7-d7', 'd7-e7', 'e7-f7', 'f7-g7', 'g7-f7', 'f7-e7', 'e7-d7', 'd7-c7', 'c7-b7', 'b7-a7', 'g7-h7']

        np.testing.assert_equal(sorted(game.pawnMoves(1)), sorted(testMoves))


        # Case with one knight - Black
        testBoard = np.array([-1, 1, 1, 1, 1, 1, 1, -1,
                              0, 1, 1, 1, 1, 1, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 4, 5, 4, 4, 4, 4, 0,
                              -1, 4, 0, 4, 4, 4, 4, -1]).reshape(8, 8)
        game.setBoard(testBoard)
        testMovesPawn = ['b8-b7', 'd8-d7', 'e8-e7', 'f8-f7', 'g8-g7',
                            'b7-b6', 'd7-d6', 'e7-e6', 'f7-f6', 'g7-g6',
                           'b8-c8', 'd8-e8', 'e8-f8', 'f8-g8',
                           'c7-d7', 'd7-e7', 'f7-g7', 'g7-h7',
                           'g8-f8', 'f8-e8', 'e8-d8', 'd8-c8',
                           'g7-f7', 'f7-e7', 'e7-d7', 'b7-a7']
        testMovesKnight = ['c7-a6', 'c7-e6', 'c7-b5', 'c7-d5']

        np.testing.assert_equal(sorted(game.pawnMoves(0)), sorted(testMovesPawn))
        np.testing.assert_eqaul(sorted(game.knightMoves(0)), sorted(testMovesKnight))

        # Case with possible captures - Black
        testBoard = np.array([-1, 0, 1, 1, 1, 1, 1, -1,
                              0, 0, 1, 1, 1, 0, 1, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0,
                              0, 2, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 1, 0, 0,
                              0, 4, 5, 4, 4, 4, 4, 0,
                              -1, 4, 0, 4, 4, 4, 4, -1]).reshape(8, 8)
        game.setBoard(testBoard)
        testKnightCaptures=['c7-b5']
        testPawnCaptures = ['e7-f6', 'g7-f6']

        self.assertTrue((set(testPawnCaptures)).issubset(set(game.pawnMoves(1))))
        self.assertTrue((set(testKnightCaptures)).issubset(set(game.knightMoves(1))))
        
if __name__ == '__main__':
    unittest.main()
