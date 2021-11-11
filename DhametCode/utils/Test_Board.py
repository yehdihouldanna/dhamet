#------------------------------------------------
# Copyrigh (c) SMART Solutions SM SA® 2021.
# All rights reserved.
# Code made by : Yehdhih ANNA (TheLuckyMagician).
#------------------------------------------------

from Board import State
import unittest
import numpy as np

class TestBoard(unittest.TestCase):
    def test_state(self):
        game = State(9)
        assert game.n == 9
        assert game.board.shape == (9,9)
        moved = game.move((3,3),(4,4))
        assert moved
        A= np.array([
            [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  0,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1,]])
        assert A.shape==game.board.shape
        np.testing.assert_array_almost_equal(game.board,A)
        possible_moves,scores = game.available_moves(5,5)
        self.assertCountEqual(scores,[1])
        self.assertListEqual(scores,[1])
        self.assertCountEqual(possible_moves,[(3, 3)])
        self.assertListEqual(possible_moves,[(3,3)])

        game.set_player("White")
        moved = game.move((5,5),(3,3)) # trying to move that is not the Player's (non valid)
        assert not moved

        A = np.array(
            [[ 1,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  1,  0,  0,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  0,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1, -1, -1, -1, -1],
            [-1, -1, -1,  0, -1,  0, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1]]
        )
        game.set_board(A)
        game.set_player("Black")
        possible_moves,scores=game.available_moves(4,5)
        self.assertCountEqual(scores,[])
        self.assertListEqual(scores,[])
        self.assertCountEqual(possible_moves,[])
        self.assertListEqual(possible_moves,[])

        moved = game.move((4,5),(2,3))  # trying to move diagonaly from a '+' node (non valid)
        assert not moved

        A = np.array(
            [[ 1,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 0,  0,  0,  0,  1,  0,  1,  1,  1],
            [ 0,  0,  0, -1,  0,  0,  1,  1,  1],
            [ 0,  0, -1,  0,  0,  0, -1, -1, -1],
            [ 0,  0,  0,  0, -1, -1, -1, -1, -1],
            [ 0,  0,  0, -1, -1,  0, -1, -1, -1],
            [ 0, -1, -1, -1, -1, -1, -1, -1, -1],
            [ 3, -1, -1, -1, -1, -1, -1, -1, -1]])
        game.set_board(A)
        possible_moves_80= [(7, 0), (6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (6, 2), (5, 3), (4, 4), (3, 5)]
        scores_80 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        possible_moves,scores= game.available_moves(8,0)
        self.assertCountEqual(scores_80,scores)
        self.assertListEqual(sorted(scores_80),sorted(scores))
        self.assertCountEqual(possible_moves_80,possible_moves)
        self.assertListEqual(sorted(possible_moves_80),sorted(possible_moves))
        print("Test State OK!")
        
if __name__=="__main__":
    test = TestBoard()
    test.test_state()


