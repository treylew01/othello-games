from agent import Player
from math import inf
import random

import time

from game import getValidMoves, getBoardCopy, gameOver, getScoreOfBoard, makeMove

#Pulled from https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
UTILITY = {
            (0, 0): 4, (0, 1): -3, (0, 2): 2, (0, 3): 2, (0, 4): 2, (0, 5): 2, (0, 6): -3, (0, 7): 4,
            (1, 0): -3, (1, 1): -4, (1, 2): -1, (1, 3): -1, (1, 4): -1, (1, 5): -1, (1, 6): -4, (1, 7): -3,
            (2, 0): 2, (2, 1): -1, (2, 2): 1, (2, 3): 0, (2, 4): 0, (2, 5): 1, (2, 6): -1, (2, 7): 2, 
            (3, 0): 2, (3, 1): -1, (3, 2): 0, (3, 3): 1, (3, 4): 1, (3, 5): 0, (3, 6): -1, (3, 7): 2,
            (4, 0): 2, (4, 1): -1, (4, 2): 0, (4, 3): 1, (4, 4): 1, (4, 5): 0, (4, 6): -1, (4, 7): 2,
            (5, 0): 2, (5, 1): -1, (5, 2): 1, (5, 3): 0, (5, 4): 0, (5, 5): 1, (5, 6): -1, (5, 7): 2,
            (6, 0): -3, (6, 1): -4, (6, 2): -1, (6, 3): -1, (6, 4): -1, (6, 5): -1, (6, 6): -4, (6, 7): -3,
            (7, 0): 4, (7, 1): -3, (7, 2): 2, (7, 3): 2, (7, 4): 2, (7, 5): 2, (7, 6): -3, (7, 7): 4
        }

MAX_PLAYER = 1
MIN_PLAYER = 2

class Trey(Player):
    def __init__(self, time, *args, **kwargs):
        self.time = time
        super().__init__(*args, **kwargs)

    def getComputerMove(self, board):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        start = time.time()

        moves = getValidMoves(board, self.piece)
        if len(moves) == 1:
            return moves[0]
        if len(moves) == 0:
            return None

        # First look for a kill_move, if such a move exists, capture it
        killer = self.killer_move(board)
        if killer is not None:
            return killer
        
        depth = 2
        max_pos = 1 if self.piece == 1 else 0
        best_move = None
        best_score = -inf if max_pos else inf
        while time.time() - start < self.time:
            score, move = self.minimax_alpha_beta(board, max_pos, self.utility_heuristic, depth, -inf, inf, start)
            if max_pos:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
            depth += 1
        return best_move

    def minimax(self, board, side, heuristic, depth):
        #print(depth)
        moves = getValidMoves(board, 2 - side)
        if depth == 0 or gameOver(board):
            return heuristic(board), None
        
        if len(moves) == 0:
            return heuristic(board), None
            
        best_move = None
        if side:
            best_score_yet = -9999
            for move in moves:

                new_board = getBoardCopy(board)
                makeMove(new_board, 2 - side, move[0], move[1])
                move_score, _ = self.minimax(new_board,  1 - side, heuristic, depth - 1)

                if best_score_yet < move_score:
                    best_score_yet = move_score
                    best_move = move

            return best_score_yet, best_move
        else:
            best_score_yet = 9999
            for move in moves:

                new_board = getBoardCopy(board)
                makeMove(new_board, 2 - side, move[0], move[1])
                move_score, _ = self.minimax(new_board,  1 - side, heuristic, depth - 1)

                if best_score_yet > move_score:
                    best_score_yet = move_score
                    best_move = move

            return best_score_yet, best_move
    
    def minimax_alpha_beta(self, board, side, heuristic, depth, alpha, beta, start):        
        moves = getValidMoves(board, 2 - side)
        if depth == 0 or gameOver(board):
            return heuristic(board), None

        if len(moves) == 0:
            return heuristic(board), None

        best_move = None
        if side:
            a = -inf
            for move in moves:
                if time.time() - start >= self.time:
                    if best_move == None:
                        return heuristic(board), move
                    else:
                        return a, best_move

                new_board = getBoardCopy(board)
                makeMove(new_board, 2 - side, move[0], move[1])
                move_score, _ = self.minimax_alpha_beta(new_board,  1 - side, heuristic, depth - 1, alpha, beta, start)

                if move_score > a:
                    a = move_score
                    best_move = move
                
                alpha = max(alpha, a)
                if beta <= alpha:
                    break
                    

            return a, best_move
        else:
            b = inf
            for move in moves:
                if time.time() - start >= self.time:
                    if best_move == None:
                        return heuristic(board), move
                    else:
                        return b, best_move


                new_board = getBoardCopy(board)
                makeMove(new_board, 2 - side, move[0], move[1])
                move_score, _ = self.minimax_alpha_beta(new_board,  1 - side, heuristic, depth - 1, alpha, beta, start)

                if b > move_score:
                    b = move_score
                    best_move = move
                
                beta = min(beta, b)
                if beta <= alpha:
                    break

            return b, best_move
        
    

    def greedy_heuristic(self, board):
        """
            Simply Greedy Heuristic which goes for points based on max or min
        """
        score = getScoreOfBoard(board)
        return score[0] - score[1]
    
    #ideas synthesized from https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/

    def heuristic(self, board):
        coin_parity = self.coin_parity(board)
        mobility = self.mobility(board)
        corners = self.corner_pieces(board)
        return coin_parity + mobility + corners
    
    def coin_parity(self, board):
        score = getScoreOfBoard(board)
        if score[0] == score[1]:
            return 0
        coin_parity = 100 * ((score[0] - score[1]) / (score[1] - score[0]))
        return coin_parity
    
    def mobility(self, board):
        if not gameOver(board):
            max_player_length = len(getValidMoves(board, MAX_PLAYER))
            min_player_length = len(getValidMoves(board, MIN_PLAYER))
            mobility = 100 * (max_player_length - min_player_length) / (max_player_length + min_player_length)
            return mobility
        return 0
    
    def corner_pieces(self, board):
        corners = self.corner_captured(board)
        if corners[0] + corners[1] != 0:
            corner = 100 * ((corners[0] - corners[1]) / (corners[0] + corners[1]))
            return corner
        else:
            return 0


    def corner_captured(self, board):
        corners = [[0, 0], [0, 7], [7, 0], [7, 7]]        
        
        count_max = 0
        count_min = 0
        for corner in corners:
            if board[corner[0]][corner[1]] == MAX_PLAYER:
                count_max += 1
            if board[corner[0]][corner[1]] == MIN_PLAYER:
                count_min += 1
        return count_max, count_min

    def utility_heuristic(self, board):
        max_value = 0
        min_value = 0

        for x in range(8):
            for y in range(8):
                if board[x][y] == MIN_PLAYER:
                    min_value += UTILITY[(x, y)]
                if board[x][y] == MAX_PLAYER:
                    max_value += UTILITY[(x, y)]

        utility_value = max_value - min_value
        return utility_value


    

    def killer_move(self, board):
        """ 
            Don't search the tree if a move like this exist - we want corner moves
            These moves include board[0][0], board[0][7], board[7][0], board[7][7]
        """
        killer = [[0, 0], [0, 7], [7, 0], [7, 7]]
        moves = getValidMoves(board, self.piece)

        random.shuffle(moves)

        for move in moves:
            if move in killer:
                return move
        return None


    

    

