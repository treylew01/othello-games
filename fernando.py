from agent import Player, NEGATIVEINF
from game import getValidMoves, getScoreOfBoard, gameOver, getBoardCopy, makeMove, isOnBoard
import time

INF = float('inf')
EARLY_GAME = 1
MID_GAME = 2
LATE_GAME = 3

corners = [[0, 0], [7,0], [7,0], [7,7]]

class Fernando(Player):
    def __init__(self, time, *args, **kwargs):
        self.time = time
        self.phase = EARLY_GAME
        self.count = 6
        super().__init__(*args, **kwargs)

    def getComputerMove(self, board):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        self.count += 2
        if self.count > 40:
            self.phase = LATE_GAME
        elif self.count > 20:
            self.phase = MID_GAME

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
            return self.value(board), None
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


    def score(self, board):
        score = getScoreOfBoard(board)
        return score[0] - score[1]

    def heuristic(self, board):
        value = 1000 * self.cornerScore(board) - 50 * self.adjacentCornerScore(board)
        if self.phase == EARLY_GAME:
            return value + 100 * self.mobilityScore(board) - 100 * self.frontierScore(board)
        elif self.phase == MID_GAME:
            return value + 100 * self.mobilityScore(board) + 100 * self.score(board) +  - 100 * self.frontierScore(board)
        else:
            return value + 100 * self.mobilityScore(board) + 200 * self.score(board)

    def mobilityScore(self, board):
        player1 = len(getValidMoves(board, 1))
        player2 = len(getValidMoves(board, 2))
        #potential_mobility = 0
        if player1 + player2 == 0:
            return 0
        return (player1 - player2) / (player1 + player2)

    def cornerScore(self, board):
        player1 = 0.0
        player2 = 0.0
        for corner in corners:
            capture = board[corner[0]][corner[1]]
            if capture != 0:
                if capture == 1:
                    player1 += 1
                else:
                    player2 += 1

        if player1 + player2 == 0:
            return 0
        return (player1 - player2)/(player1 + player2)

    def frontierScore(self, board):
        player1 = 0.0
        player2 = 0.0
        for x in range(1,7):
            for y in range(1,7):
                if board[x][y] != 0:
                    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                        if board[x+xdirection][y+ydirection] == 0:
                            if board[x][y] == 1:
                                player1 += 1
                            else:
                                player2 += 1

        if player1 + player2 == 0:
            return 0
        return (player1 - player2)/(player1 + player2)

    def adjacentCornerScore(self, board):
        player1 = 0.0
        player2 = 0.0
        for corner in corners:
            capture = board[corner[0]][corner[1]]
            if capture == 0:
                for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
                    x = corner[0] + xdirection
                    y = corner[1] + ydirection
                    if isOnBoard(x, y):
                        if board[x][y] != 0:
                            if board[x][y] == 1:
                                player1 += 1
                            else:
                                player2 += 1

        if player1 + player2 == 0:
            return 0
        return (player1 - player2)/(player1 + player2)

    def value(self, board):
        score = getScoreOfBoard(board)
        if score[0] > score[1]:
            return 10000
        if score[0] == score[1]:
            return 0
        return -10000