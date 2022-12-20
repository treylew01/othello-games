from agent import Player

from game import getValidMoves, isValidMove, getBoardCopy, gameOver, getScoreOfBoard, makeMove

MAX_PLAYER = 1
MIN_PLAYER = 2
DEPTH = 1

class Trey(Player):

    def getComputerMove(self, board):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        # move and return that move as a [x, y] list.
        possibleMoves = getValidMoves(board, self.piece)
        if len(possibleMoves) == 0:
            return None
        # randomize the order of the possible moves
        current_score = -9999
        winning_move = None

        if len(possibleMoves) > 1:
            for move in possibleMoves:
                passed_board = getBoardCopy(board)
                makeMove(passed_board, self.piece, move[0], move[1])

                score = self.minimax(passed_board, DEPTH - 1, -9999, 9999)
                if score > current_score:
                    winning_move = move
                    current_score = score
        else:
            winning_move = possibleMoves[0]
        return winning_move

    def minimax(self, board_state, depth, min, max):
        total_moves = getValidMoves(board_state, self.piece)

        total_moves_length = len(total_moves)
        eval = self.evaluate(board_state)


        if total_moves_length == 0 or depth == 0 or gameOver(board_state):
            return eval
        if self.piece == MIN_PLAYER:
            best_move_yet = min
            for move in total_moves:
                passed_board = getBoardCopy(board_state)
                makeMove(board_state, MIN_PLAYER, move[0], move[1])
                current_move = self.minimax(passed_board, depth - 1, best_move_yet, max)
                if current_move > best_move_yet:
                    best_move_yet = current_move
                if best_move_yet > max:
                    return max
            return best_move_yet
        else:
            best_move_yet = max
            for move in total_moves:
                passed_board = getBoardCopy(board_state)
                makeMove(board_state, MAX_PLAYER, move[0], move[1])
                current_move = self.minimax(passed_board, depth - 1, min, best_move_yet)
                if current_move < best_move_yet:
                    best_move_yet = current_move
                if best_move_yet < min:
                    return min
            return best_move_yet
    
    def evaluate(self, board):
        players = getScoreOfBoard(board)
        score = players[0] - players[1]
        return score
