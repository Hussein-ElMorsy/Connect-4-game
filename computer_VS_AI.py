import math
import random
import sys

import numpy as np
import pygame

rowCtr = 6
colCtr = 7
windowLength = 4
empty = 0
computer = 0
AI = 1
computerPiece = 1
AIPiece = 2

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

pygame.init()
winSound = pygame.mixer.Sound('soundEffects\win.mp3')


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


def evaluateWindow(window, piece):
    score = 0
    opPiece = computerPiece
    if piece == computerPiece:
        opPiece = AIPiece
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(empty) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(empty) == 2:
        score += 2
    if window.count(opPiece) == 3 and window.count(empty) == 1:
        score -= 4
    return score


def positionScore(board, piece):
    score = 0
    # center column score
    centerArray = [int(i) for i in list(board[:, colCtr // 2])]
    centerCtr = centerArray.count(piece)
    score += centerCtr * 3

    # Horizonal score
    for r in range(rowCtr):
        rowArray = [int(i) for i in list(board[r, :])]
        for c in range(colCtr - 3):
            window = rowArray[c:c + windowLength]
            score += evaluateWindow(window, piece)
    # Vertical Score
    for c in range(colCtr):
        colArray = [int(i) for i in list(board[:, c])]
        for r in range(rowCtr - 3):
            window = colArray[r:r + windowLength]
            score += evaluateWindow(window, piece)
    # Positive sloped diagonal score
    for r in range(rowCtr - 3):
        for c in range(colCtr - 3):
            window = [board[r + i][c + i] for i in range(windowLength)]
            score += evaluateWindow(window, piece)
    # Negative sloped diagonal score
    for r in range(rowCtr - 3):
        for c in range(colCtr - 3):
            window = [board[r + 3 - i][c + i] for i in range(windowLength)]
            score += evaluateWindow(window, piece)

    return score


def isTerminalNode(board):
    return winningMove(board, computerPiece) or winningMove(board, AIPiece) or len(getValidLocations(board)) == 0


def miniMax(board, depth, alpha, beta, maxPlayer):
    validLoc = getValidLocations(board)
    isTerminal = isTerminalNode(board)
    if depth == 0 or isTerminal:
        if isTerminal:
            if winningMove(board, AIPiece):
                return (None, math.inf)
            elif winningMove(board, computerPiece):
                return (None, -math.inf)
            else:  # game over no more moves
                return (None, 0)
        else:  # depth is zero
            return (None, positionScore(board, AIPiece))
    if maxPlayer:
        value = -math.inf
        bestColumn = random.choice(validLoc)
        for col in validLoc:
            row = getNextOpenRow(board, col)
            boardCopy = board.copy()
            dropPiece(boardCopy, row, col, AIPiece)
            newScore = miniMax(boardCopy, depth - 1, alpha, beta, False)[1]
            if newScore > value:
                value = newScore
                bestColumn = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return bestColumn, value
    else:
        value = math.inf
        bestColumn = random.choice(validLoc)
        for col in validLoc:
            row = getNextOpenRow(board, col)
            boardCopy = board.copy()
            dropPiece(boardCopy, row, col, computerPiece)
            newScore = miniMax(boardCopy, depth - 1, alpha, beta, True)[1]
            if newScore < value:
                value = newScore
                bestColumn = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return bestColumn, value


def getValidLocations(board):
    validLocation = []
    for c in range(colCtr):
        if isValid(board, c):
            validLocation.append(c)
    return validLocation


def pickBestMove(board, piece):
    validLocations = getValidLocations(board)
    bestScore = -math.inf
    bestCol = random.choice(validLocations)
    for col in validLocations:
        row = getNextOpenRow(board, col)
        tempBoard = board.copy()
        dropPiece(tempBoard, row, col, piece)
        score = positionScore(tempBoard, piece)
        if score > bestScore:
            bestScore = score
            bestCol = col
    return bestCol


def printBoard(board):
    print(np.flip(board, 0))


def drawBoard(board):
    for c in range(colCtr):
        for r in range(rowCtr):
            pygame.draw.rect(screen, black, (c * squareSize, r * squareSize + squareSize, squareSize, squareSize))
            pygame.draw.circle(screen, white,
                               (
                                   int(c * squareSize + squareSize / 2),
                                   int(r * squareSize + squareSize + squareSize / 2)),
                               radius)
    for c in range(colCtr):
        for r in range(rowCtr):
            if board[r][c] == 1:
                pygame.draw.circle(screen, red,
                                   (
                                       int(c * squareSize + squareSize / 2),
                                       height - int(r * squareSize + squareSize / 2)),
                                   radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, green,
                                   (
                                       int(c * squareSize + squareSize / 2),
                                       height - int(r * squareSize + squareSize / 2)),
                                   radius)

    pygame.display.update()


board = createBoard()
gameOver = False

pygame.init()

squareSize = 100
width = colCtr * squareSize
height = (1 + rowCtr) * squareSize

size = (width, height)

radius = int(squareSize / 2 - 5)

screen = pygame.display.set_mode(size)
# Set the window title
pygame.display.set_caption("Connect Four")
drawBoard(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

turn = random.randint(computer, AI)

while not gameOver:

    # Player1 turn
    if turn == computer:
        pygame.time.wait(1500)
        col = random.randint(0, 6)
        if isValid(board, col):
            row = getNextOpenRow(board, col)
            dropPiece(board, row, col, computerPiece)
            if winningMove(board, computerPiece):
                label = myFont.render("Player 1 wins!!!", 1, red)
                screen.blit(label, (40, 10))
                gameOver = True
            turn = not turn
            printBoard(board)
            drawBoard(board)

    # Player2 turn
    if turn == AI and not gameOver:
        pygame.time.wait(200)
        col, minMaxScore = miniMax(board, 6, -math.inf, math.inf, True)
        if isValid(board, col):
            row = getNextOpenRow(board, col)
            dropPiece(board, row, col, AIPiece)
            if winningMove(board, AIPiece):
                label = myFont.render("Player 2 wins!!!", 1, green)
                screen.blit(label, (40, 10))
                gameOver = True
            turn = not turn
            printBoard(board)
            drawBoard(board)

    if gameOver:
        winSound.set_volume(0.5)  # sets the volume to 50%
        winSound.play()
        pygame.time.wait(5000)
