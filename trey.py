from agent import Player
from math import inf
import random

import time

from game import getValidMoves, getBoardCopy, gameOver, getScoreOfBoard, makeMove
#ideas synthesized from https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/
MAX_PLAYER = 1
MIN_PLAYER = 2

class Trey(Player):
    def __init__(self, time, *args, **kwargs):
        self.time = time
        super().__init__(*args, **kwargs)

    def getComputerMove(self, board):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        start = time.time()

        # First look for a kill_move, if such a move exists, capture it
        #killer = self.killer_move(board)
        #if killer is not None:
        #    return killer

        depth = 2
        max_pos = 1 if self.piece == 1 else 0
        best_move = None
        best_score = -inf
        while time.time() - start < self.time:
            score, move = self.minimax_alpha_beta(board, max_pos, self.heuristic, depth, -inf, inf, start)
            if score > best_score:
                best_score = score
                best_move = move
            depth += 1
        return best_move

    def minimax(self, board, side, heuristic, depth):
        #print(depth)
        moves = getValidMoves(board, 2 - side)
        if depth == 0 or gameOver(board):
            return heuristic(board), None
        
        #if len(moves) == 0:
        #    return heuristic(board), None
            
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
                    break

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
                    break

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
        score = getScoreOfBoard(board)
        return score[0] - score[1]
    
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


    

    

