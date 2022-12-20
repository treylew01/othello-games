from agent import Player
from math import inf

from game import getValidMoves, getBoardCopy, gameOver, getScoreOfBoard, makeMove

MAX_PLAYER = 1
MIN_PLAYER = 2

class Trey(Player):
    def getComputerMove(self, board):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """

        depth = 4
        max_pos = 1 if self.piece == 1 else 0
        best_score, best_move = self.minimax_alpha_beta(board, max_pos, self.heuristic, depth, -inf, inf)
        return best_move

    def minimax(self, board, side, heuristic, depth):
        #print(depth)
        if depth == 0 or gameOver(board):
            return heuristic(board), None
        
        moves = getValidMoves(board, 2 - side)
            
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
    
    def minimax_alpha_beta(self, board, side, heuristic, depth, alpha, beta):        
        moves = getValidMoves(board, 2 - side)
        if depth == 0 or gameOver(board):
            return heuristic(board), None
        
        best_move = None
        if side:
            a = -inf
            for move in moves:

                new_board = getBoardCopy(board)
                makeMove(new_board, 2 - side, move[0], move[1])
                move_score, _ = self.minimax_alpha_beta(new_board,  1 - side, heuristic, depth - 1, alpha, beta)

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

                new_board = getBoardCopy(board)
                makeMove(new_board, 2 - side, move[0], move[1])
                move_score, _ = self.minimax_alpha_beta(new_board,  1 - side, heuristic, depth - 1, alpha, beta)

                if b > move_score:
                    b = move_score
                    best_move = move
                
                beta = min(beta, b)
                if beta <= alpha:
                    break

            return b, best_move
        
    
    def heuristic(self, board):
        score = getScoreOfBoard(board)
        return score[0] - score[1]

