from game import getValidMoves 
import random

def getComputerMoveRandom(board, piece):
    """ Board is the current Board, piece is the player, i.e 1's and 2's """
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, piece)
    # randomize the order of the possible moves
    move = random.shuffle(possibleMoves)

    return move
