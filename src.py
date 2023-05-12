import math
import random
import sys

import numpy as np
import pygame

rowCtr = 6
colCtr = 7
windowLength = 4
empty = 0
player = 0
AI = 1
playerPiece = 1
AIPiece = 2

blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)


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
    opPiece = playerPiece
    if piece == playerPiece:
        opPiece = AIPiece
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(empty) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(empty) == 2:
        score += 5
    if window.count(opPiece) == 3 and window.count(empty) == 1:
        score -= 80
    return score


def positionScore(board, piece):
    score = 0
    # center column score
    centerArray = [int(i) for i in list(board[:, colCtr // 2])]
    centerCtr = centerArray.count(piece)
    score += centerCtr * 6

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
    return winningMove(board, playerPiece) or winningMove(board, AIPiece) or len(getValidLocations(board)) == 0


def miniMax(board, depth, maxPlayer):
    validLoc = getValidLocations(board)
    isTerminal = isTerminalNode(board)
    if depth == 0 or isTerminal:
        if isTerminal:
            if winningMove(board, AIPiece):
                return (None, 100000000000000)
            elif winningMove(board, playerPiece):
                return (None, -100000000000000)
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
            newScore = miniMax(boardCopy, depth - 1, False)[1]
            if newScore > value:
                value = newScore
                bestColumn = col
        return bestColumn, value
    else:
        value = math.inf
        bestColumn = random.choice(validLoc)
        for col in validLoc:
            row = getNextOpenRow(board, col)
            boardCopy = board.copy()
            dropPiece(boardCopy, row, col, playerPiece)
            newScore = miniMax(boardCopy, depth - 1, True)[1]
            if newScore < value:
                value = newScore
                bestColumn = col
        return bestColumn, value


def getValidLocations(board):
    validLocation = []
    for c in range(colCtr):
        if isValid(board, c):
            validLocation.append(c)
    return validLocation


def pickBestMove(board, piece):
    validLocations = getValidLocations(board)
    bestScore = -10000
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
            pygame.draw.rect(screen, blue, (c * squareSize, r * squareSize + squareSize, squareSize, squareSize))
            pygame.draw.circle(screen, black,
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
                pygame.draw.circle(screen, yellow,
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
drawBoard(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

turn = random.randint(player, AI)

while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squareSize))
            posx = event.pos[0]
            if turn == player:
                pygame.draw.circle(screen, red, (posx, int(squareSize / 2)), radius)

        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, squareSize))
            # Player1 turn
            if turn == player:
                posx = event.pos[0]
                col = int(math.floor(posx / squareSize))
                if isValid(board, col):
                    row = getNextOpenRow(board, col)
                    dropPiece(board, row, col, playerPiece)
                    if winningMove(board, playerPiece):
                        label = myFont.render("Player1 wins!!!", 1, red)
                        screen.blit(label, (40, 10))
                        gameOver = True
                    turn = not turn
                    printBoard(board)
                    drawBoard(board)

        # Player2 turn
        if turn == AI and not gameOver:
            col, minMaxScore = miniMax(board, 4, True)
            if isValid(board, col):
                pygame.time.wait(500)
                row = getNextOpenRow(board, col)
                dropPiece(board, row, col, AIPiece)
                if winningMove(board, AIPiece):
                    label = myFont.render("Player2 wins!!!", 1, yellow)
                    screen.blit(label, (40, 10))
                    gameOver = True
                turn = not turn
                printBoard(board)
                drawBoard(board)

        if gameOver:
            pygame.time.wait(4000)
