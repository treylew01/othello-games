# Reversi
import random
import sys

def drawBoard(board):

    # This function prints out the board that it was passed. Returns None.

    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)



def resetBoard(board):
    # Blanks out the board it is passed, except for the original starting posit
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'



def getNewBoard():
    # Creates a brand new, blank board data structure
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board



def isValidMove(board, tile, xstart, ystart):

    # Returns False if the player's move on space xstart, ystart is invalid

    # If it is a valid move, returns a list of spaces that would become the player's if they made a move h
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False


    board[xstart][ystart] = tile 
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

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
    board[xstart][ystart] = ' ' # restore the empty space

    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move

        return False

    return tilesToFlip

 
 
def isOnBoard(x, y):
    # Returns True if the coordinates are located on the boa
    return x >= 0 and x <= 7 and y >= 0 and y <=7

 
 
def getBoardWithValidMoves(board, tile):
    # Returns a new board with _ marking the valid moves the given player can make
    dupeBoard = getBoardCopy(board)
    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'

    return dupeBoard



def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def enterPlayerTile():
    # Lets the player type which tile they want to be
    # Returns a list with the player's tile as the first item, and the computer's tile as the second
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()
    # the first element in the list is the player's tile, the second is the computer's tile

    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']



def whoGoesFirst():
    # Randomly choose the player who goes first
    if random.randint(0, 1) == 0:
        return 'computer'

    else:
        return 'player'



def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')



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

def getBoardCopy(board):
    # Make a duplicate of the board list and return the duplicate.
    dupeBoard = getNewBoard()
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard



def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)
