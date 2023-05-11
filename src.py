import numpy as np

rowCtr = 6
colCtr = 7


def createBoard():
    board = np.zeros((rowCtr, colCtr))
    return board


def dropPiece(board, row, col, piece):
    board[row][col] = piece


def isValid(board, col):
    return board[rowCtr - 1][col] == 0


def getNextOpenRow(board, col):
    for r in range(rowCtr):
        if board[r][col] == 0:
            return r


def move(board, col, piece):
    if isValid(board, col):
        row = getNextOpenRow(board, col)
        dropPiece(board, row, col, piece)


def winningMove(board, piece):
    # Horizontal check
    for c in range(colCtr - 3):
        for r in range(rowCtr):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and \
                    board[r][c + 3] == piece:
                return True
    # vertical check
    for c in range(colCtr):
        for r in range(rowCtr - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and \
                    board[r + 3][c] == piece:
                return True
    # diagonal check (positive,positive)
    for r in range(rowCtr - 3):
        for c in range(colCtr - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                    board[r + 3][c + 3] == piece:
                return True
    # diagonal check (positive, negative)
    for r in range(rowCtr - 3):
        for c in range(3, colCtr):
            if board[r][c] == piece and board[r + 1][c - 1] == piece and board[r + 2][c - 2] == piece and \
                    board[r + 3][c - 3] == piece:
                return True


def printBoard(board):
    print(np.flip(board, 0))


board = createBoard()
gameOver = False
turn = 0

while not gameOver:
    # Player1 turn
    if turn == 0:
        col = int(input("Player1 make your move (0-6):"))
        move(board, col, 1)
        if winningMove(board, 1):
            print("Player1 wins!!!")
            gameOver = True


    # Player2 turn
    else:
        col = int(input("Player2 make your move (0-6):"))
        move(board, col, 2)
        if winningMove(board, 2):
            print("Player2 wins!!!")
            gameOver = True

    printBoard(board)

    turn = not turn
