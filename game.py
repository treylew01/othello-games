# Reversi
import random
import sys

def resetBoard(board):
    # Blanks out the board it is passed, except for the original starting posit
    for x in range(8):
        for y in range(8):
            board[x][y] = 0

    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1


def isValidMove(board, tile, xstart, ystart):

    # Returns False if the player's move on space xstart, ystart is invalid
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move h
    if board[xstart][ystart] != 0 or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile
    if tile == 1:
        otherTile = 2
    else:
        otherTile = 1

    tilesToFlip = []

    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our pi
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip Go in the reverse direction until we reach the original space, noting all the tiles along the                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    board[xstart][ystart] = 0 # restore the empty space

    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move
        return False

    return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the boa
    return x >= 0 and x <= 7 and y >= 0 and y <=7


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def whoGoesFirst():
    # Randomly choose the player who goes first
    if random.randint(0, 1) == 0:
        return 'computer'

    else:
        return 'player'


def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move, True if it is valid
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)
