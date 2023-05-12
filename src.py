import math
import sys

import numpy as np
import pygame

rowCtr = 6
colCtr = 7

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
turn = 0

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

while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0, 0, width, squareSize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, red, (posx, int(squareSize / 2)), radius)
            else:
                pygame.draw.circle(screen, yellow, (posx, int(squareSize / 2)), radius)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0, 0, width, squareSize))
            # Player1 turn
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / squareSize))
                move(board, col, 1)
                if winningMove(board, 1):
                    label = myFont.render("Player1 wins!!!", 1, red)
                    screen.blit(label, (40, 10))
                    gameOver = True

            # Player2 turn
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / squareSize))
                move(board, col, 2)
                if winningMove(board, 2):
                    label = myFont.render("Player2 wins!!!", 1, yellow)
                    screen.blit(label, (40, 10))
                    gameOver = True

            printBoard(board)
            drawBoard(board)
            turn = not turn
            if gameOver:
                pygame.time.wait(4000)
