import math

from board import Board
import time
import random
import src as fun
import numpy as np


# GAME LINK
# http://kevinshannon.com/connect4/


def main():
    board = Board()

    print("1 (miniMax algorithm")
    print("2 (alpha beta pruning)")
    print("Choose which algorithm to use: ", end=" \t")
    option = input()
    level = 0
    print("1 (Easy)")
    print("2 (Medium)")
    print("3 (Hard)")
    print("Choose the difficulty: ", end=" \t")
    level = input()
    time.sleep(2)
    game_end = False
    while not game_end:
        (game_board, game_end) = board.get_game_grid()

        # FOR DEBUG PURPOSES
        # board.print_grid(game_board)
        # YOUR CODE GOES HERE

        # Insert here the action you want to perform based on the output of the algorithm
        # You can use the following function to select a column
        #    board.print_grid()
        new_board = np.zeros((6, 7))
        # Copy the content of game_board to new_board
        for i in range(len(game_board)):
            for j in range(len(game_board[i])):
                if game_board[i][j] == 0:
                    new_board[i][j] = 0
                elif game_board[i][j] == 1:
                    new_board[i][j] = 1
                elif game_board[i][j] == 2:
                    new_board[i][j] = 2
        print(new_board)
        depth = 0
        if level == 1:
            depth = 2
        elif level == 2:
            depth = 3
        else:
            depth = 8
        if option == 1:
            while True:
                col, bestScore = fun.alpha_beta(new_board, depth, -math.inf, math.inf, True)
                if fun.is_valid_location(new_board, col):
                    row = fun.get_next_open_row(new_board, col)
                    board.select_column(col)
                    if fun.winning_move(new_board, fun.AI_PIECE):
                        game_end = True
                    break

        else:
            col, bestScore = fun.alpha_beta(new_board, depth, -math.inf, math.inf, True)
            print(col)
            board.select_column(col)
        time.sleep(2)


if __name__ == "__main__":
    main()
