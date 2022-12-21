from agent import Player, NEGATIVEINF
from game import getValidMoves, getScoreOfBoard, gameOver, getBoardCopy, makeMove
import time

INF = float('inf')

class Fernando(Player):
    def __init__(self, time, *args, **kwargs):
        self.time = time
        super().__init__(*args, **kwargs)

    def getComputerMove(self, board):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        start = time.time()
        # move and return that move as a [x, y] list.
        depth = 2
        max_pos = 1 if self.piece == 1 else 0
        num_moves = getValidMoves(board, 2 - max_pos)
        if len(num_moves) == 0:
            return None
        if len(num_moves) == 1:
            return num_moves[0]
        best_move = None
        best_score = NEGATIVEINF if max_pos else INF
        while time.time() - start < self.time:
            score, move = self.alphaBeta(board, max_pos, NEGATIVEINF, INF, self.heuristic, depth, start)
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

    def alphaBeta(self, board, max_pos, alpha, beta, heuristic, depth, start):
        if depth == 0:
            return heuristic(board), None
        if gameOver(board):
            return heuristic(board), None
        best_move = None
        if max_pos:
            a = NEGATIVEINF
            for move in getValidMoves(board, 2 - max_pos):
                if alpha >= beta:
                    break
                new_board = getBoardCopy(board)
                makeMove(new_board, 2 - max_pos, move[0], move[1])
                if time.time() - start >= self.time:
                    if best_move != None:
                        return a, best_move
                    else:
                        return heuristic(new_board), move
                search = self.alphaBeta(new_board,  1 - max_pos, alpha, beta, heuristic, depth - 1, start)[0]
                if a < search:
                    a = search
                    best_move = move
                alpha = max(alpha, a)
            return a, best_move
        else:
            b = INF
            for move in getValidMoves(board, 2 - max_pos):
                if alpha >= beta:
                    break
                new_board = getBoardCopy(board)
                makeMove(new_board, 2 - max_pos, move[0], move[1])
                if time.time() - start >= self.time:
                    if best_move != None:
                        return b, best_move
                    else:
                        return heuristic(new_board), move
                search = self.alphaBeta(new_board,  1 - max_pos, alpha, beta, heuristic, depth - 1, start)[0]
                if b > search:
                    b = search
                    best_move = move
                beta = min(beta, b)
            return b, best_move


    def heuristic(self, board):
        score = getScoreOfBoard(board)
        return score[0] - score[1]


    def value(self, board):
        score = getScoreOfBoard(board)
        if score[0] > score[1]:
            return 100
        if score[0] == score[1]:
            return 0
        return -100