from game import getValidMoves, isValidMove
import random
import math

NEGATIVEINF = float('-inf')

class Player:
    def __init__(self, piece):
        self.piece = piece

    def getComputerMove(board, piece):
        pass

class Random(Player):
    def getComputerMove(self, board):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        # move and return that move as a [x, y] list.
        possibleMoves = getValidMoves(board, self.piece)
        print
        if len(possibleMoves) == 0:
            return None
        # randomize the order of the possible moves
        move = random.choice(possibleMoves)

        return move

class Greedy(Player):
    def getComputerMove(self, board):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        # move and return that move as a [x, y] list.
        possibleMoves = getValidMoves(board, self.piece)
        print(possibleMoves)
        # randomize the order of the possible moves
        moves = random.shuffle(possibleMoves)
        print(moves)

        max = NEGATIVEINF
        best_move = None
        for move in moves:
            print("hello World")
            tilesToFlip = len(isValidMove(board, self.piece, move[0], move[1], True))
            print(tilesToFlip)
            if tilesToFlip > max:
                max = tilesToFlip
                best_move = move

        return best_move

class Fernando(Player):
    def getComputerMove(board, piece):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        # move and return that move as a [x, y] list.
        possibleMoves = getValidMoves(board, piece)
        # randomize the order of the possible moves
        move = random.choice(possibleMoves)

        return move

class Trey(Player):
    def getComputerMove(board, piece):
        """ Board is the current Board, piece is the player, i.e 1's and 2's """
        # move and return that move as a [x, y] list.
        possibleMoves = getValidMoves(board, piece)
        # randomize the order of the possible moves
        move = random.choice(possibleMoves)

        return move