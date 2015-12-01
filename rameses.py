# !/usr/bin/python

__author__ = 'sagar'

'''
A brief report on the program:

Run Command: python rameses.py <board-size> <board-current-state> <maximum-time-to-return-decision>
Input parameters:
<board-size> -> Number of rows or number of columns in input board. e.g. N for NxN board
<board-current-state> -> current state of board represented by '.' and 'x'. '.' for empty cell, 'x' for occupied cell.
<maximum-time-to-return-decision> -> time to provide next move

Expected sample output:
Command: python rameses.py 3 ......xx. 2
Output:
INFO:root: Board: [['0', '0', '0'], ['0', '0', '0'], ['1', '1', '0']] time cutoff: 1800.0 N: 3 player: 1
INFO:root: Next move is column : 1 Row: 1 time 0.0054 seconds
x.....xx.

Algorithm: optiMinMax variant of MinMax with two time based cutoffs, soft cutoff, hard cutoff
Soft cutoff: 90% time is allocated for expansion of tree and 10% to rollback the tree calculating the final move.
Hard Cutoff: if rollback is not completed till 50 millisecond before the maximum time allowed, the best move from
    currently rolled back tree is returned

What Opti stands for in optiMinMax? and why there is comment #NeverLooseHopes in algorithm below?
Opti stands for Optimistic. MinMax don't differentiate between loosing states, so if it's loosing in all possible moves
it will just give up the fight and yield first loosing move. By adding depth to -ve infinity this algorithm will delay
the victory of opponent to the last possible move hoping that opponent will make non optimal move.

Algorithm :

cutoff <- maxTimeForDecision*0.9

Algo MinMax(boardConfiguration, player, alphaValue, betaValue, currentDepth)

    cutoff -= time for last iteration

    if game is over:
        if max player
            return +ve infinity
        else
            return -ve infinity + depth #NeverLooseHopes

    if cutoff <= 0
        #start rollup
        if hardCutoff:
            return currentBestMove
        return  evaluateBoard(boardConfiguration), move

    emptyTiles = getAvailableEmptyTiles(boardConfiguration)

    if Max player:

        for each tile in emptyTiles
            newBoard = makeMove[tile]
            score = MinMax(newBoard, player.min, alphaValue, betaValue, currentDepth+1)
            if(score > alphaValue)
                alphaValue = score
                move = tile
                currentBest = tile

            if alphaValue >= betaValue
                skip remaining nodes, tree is pruned

    if Min player:

        for each tile in emptyTiles
            newBoard = makeMove[tile]
            score = MinMax(newBoard, player.max, alphaValue, betaValue, currentDepth+1)
            if(score < betaValue)
                betaValue = score
                move = tile

            if alphaValue >= betaValue
                skip remaining nodes, tree is pruned

    if Max player
        return alphaValue, move
    else
        return betaValue, move

Initial call:
MinMax(initialBoardConfiguration, player.max, max -ve value, max +ve value, 0)


Program Analysis:


Configuration: 4x4
x . . x
. . x .
x . . .
. x . .

New Configuration: x..x.xx.x....x..
Next Move: column : 2 Row: 2
Time required: 0.4331 seconds

Configuration: 7x7
x x . . x . x
. x . x x x x
. x x x . x .
x x . x x . x
x x x . x . x
x . x x x x x
x x . x x x .

New Configuration: xxx.x.x.x.xxxx.xxx.x.xx.xx.xxxx.x.xx.xxxxxxx.xxx.
Next Move: column : 3 Row: 1
Time required: 1.8935 seconds

'''

import sys, os
import logging
import time
from copy import deepcopy
import math

# set debug level
logging.basicConfig(level=logging.INFO)  # warning: changing log level affects time for evaluation! 


class Solution:
    MAX = '1'  # MAX player's notation
    MIN = '0'  # Min player's notation

    def __init__(self, N, config, cutoff, player):

        self.player = player  # current player
        self.boardSize = int(N)  # number of columns or row
        self.cutoff = float(cutoff) * 0.9  # time to take decision is 90% of total allocated time.\
        #  10% time is required to rollup the results.
        self.startTime = 0  # start time of each iterative call to minMax algorithm
        self.board = []  # intial NxN board state represented in 0s and 1s
        self.initialConfig = config  # intial config passed to program in 'x' and '.'
        self.currentBest = 0  # current best move
        self.programStartTime = time.time()  # start time of program
        self.timeForDecision = float(cutoff) - 50  # The time till the rollup should be completed \
        # and decision should be printed.

        config = config.replace('x', '1')  # transform config in 'x' with '1's
        config = config.replace('.', '0')  # transform config in '.' with '0's

        # if empty board
        config = config.strip()

        if not config:
            logging.error(" Empty configuration")
            return -1

        # now convert the config to a matrix of size NxN
        row = []
        j = 0
        for i in range(0, self.boardSize * self.boardSize):
            row.append(config[i])
            j += 1
            if self.boardSize == j:
                self.board.append(row)
                j = 0
                row = []

        # if game is already over
        if self.isGameOver(self.board):
            logging.error("The game is over")
            return

        self.printConfig()

    def printConfig(self):
        logging.info(' Board: ' + str(self.board) + ' time cutoff: ' + str(self.cutoff) + ' N: ' + str(
            self.boardSize) + ' player: ' + self.player)

    # returns all empty tiles in current board state
    def getEmptyTiles(self, board):
        empty = []
        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                if board[i][j] == '0':
                    empty.append(i * self.boardSize + j)
        return empty

    # get number of empty cells present in the column of given position
    def getColumnEmptyCells(self, pos, boardConfig):
        board = deepcopy(boardConfig)
        board = zip(*board)
        row = ''.join(board[int(math.floor(pos % self.boardSize))])
        return row.count('0')

    # get number of empty cells present in the row of given position
    def getRowEmptyCells(self, pos, boardConfig):
        board = deepcopy(boardConfig)
        row = ''.join(board[int(math.floor(pos / self.boardSize))])
        return row.count('0')

    # get number of empty cells present in the left diagonal of given position
    def getLeftDiagonalEmptyCells(self, pos, boardConfig):
        board = deepcopy(boardConfig)

        x = int(math.floor(pos / self.boardSize))
        y = int(math.floor(pos % self.boardSize))
        mainDiagonal = ''

        if x == y:
            for i in range(0, self.boardSize):
                mainDiagonal += board[i][i]
            return mainDiagonal.count('0')
        else:
            return -1

    # get number of empty cells present in the right diagonal of given position
    def getRightDiagonalEmptyCells(self, pos, boardConfig):
        board = deepcopy(boardConfig)

        x = int(math.floor(pos / self.boardSize))
        y = int(math.floor(pos % self.boardSize))
        mainDiagonal = ''

        if y == self.boardSize - x - 1:
            for i in range(0, self.boardSize):
                mainDiagonal += board[i][self.boardSize - i - 1]
            return mainDiagonal.count('0')
        else:
            return -1

    # if game any of the row, column or diagonal is completed
    def isGameOver(self, boardConfig):

        board = deepcopy(boardConfig)

        for i in range(0, self.boardSize):  # Rows
            row = ''.join(board[i])
            if row.count('0') == 0:
                logging.debug(" Row is occupied")
                return True

        temp = zip(*board)
        for i in range(0, self.boardSize):  # Columns
            row = ''.join(temp[i])
            if row.count('0') == 0:
                logging.debug(" Column is occupied")
                return True

        mainDiagonal = ''
        for i in range(0, self.boardSize):
            mainDiagonal += board[i][i]

        diagonal = ''
        for i in range(0, self.boardSize):
            diagonal += board[i][self.boardSize - i - 1]

        if mainDiagonal.count('0') == 0 or diagonal.count('0') == 0:
            logging.debug(" Diagonal is occupied")
            return True

        return False

    # static evaluation function for the board for time based cutoff.
    # for each empty tile in any row, column or diagonal:
    # For Max: +30 if its last tile, -20 if two tiles remaining, +5 if odd number of tiles remaining
    # For Min: -30 if its last tile, +20 if two tiles remaining, +5 if even number of tiles remaining
    def evaluateBoard(self, board, player):
        # minimal heuristic for now

        val = 1  # multiplier to toggle score values based on player

        if player == Solution.MIN:
            val = -1

        # get empty slides
        emptySlides = self.getEmptyTiles(board)
        score = 0

        for slide in emptySlides:
            colRemaining = self.getColumnEmptyCells(slide, board)
            rowRemaining = self.getRowEmptyCells(slide, board)
            rdiagRemaining = self.getRightDiagonalEmptyCells(slide, board)
            ldiagRemaining = self.getLeftDiagonalEmptyCells(slide, board)

            # For Max: +30 if its last tile
            if colRemaining == 1:
                score += 30 * val
            if rowRemaining == 1:
                score += 30 * val
            if rdiagRemaining == 1:
                score += 30
            if ldiagRemaining == 1:
                score += 30

            # For Max: -20 if two tiles remaining
            if colRemaining == 2:
                score -= 20 * val
            if rowRemaining == 2:
                score -= 20 * val
            if rdiagRemaining == 2:
                score -= 20
            if ldiagRemaining == 2:
                score -= 20

            # For Max: +5 if odd number of tiles remaining
            if colRemaining % 2 == 0:
                score -= 5 * val
            else:
                score += 5 * val
            if rowRemaining % 2 == 0:
                score -= 5 * val
            else:
                score += 5 * val

            if rdiagRemaining != -1:
                if rdiagRemaining % 2 == 0:
                    score -= 5
                else:
                    score += 5 * val

            if ldiagRemaining != -1:
                if ldiagRemaining % 2 == 0:
                    score -= 5
                else:
                    score += 5 * val

        return score

    # recursive minMax algorithm
    # int(self.boardSize) * int(self.boardSize) * 300 :- +ve infinity
    def minMax(self, board, player, alpha, beta, depth):

        if self.startTime != 0:  # if not the first iteration
            self.cutoff -= round((time.time() - self.startTime) * 1000, 3)  # subtract time for last iteration
        self.startTime = round(time.time(), 3)  # set start time for current iteration

        gameover = self.isGameOver(board)
        move = -1
        score = 0
        # if terminal state is reached
        if gameover:
            logging.debug(" Gameover reached at level " + str(depth))
            if gameover and player == Solution.MAX:  # if win for Max
                score = int(self.boardSize) * int(self.boardSize) * 300  # return +ve infinity.
            elif gameover and player == Solution.MIN:  # if win for Min
                score = -int(self.boardSize) * int(
                    self.boardSize) * 300 + depth  # return -ve infinity + depth #NeverLooseHopes \
                # even if its loosing it will delay the victory of opponent to last possible move

            return score, move

        if self.cutoff <= 0:  # cutoff occurred, start to rollup the scores

            timeLapsed = (time.time() - self.programStartTime) * 1000  # time lapsed since beginning of program

            if timeLapsed >= self.timeForDecision:  # if rollup did't complete in 10% allocated time.
                self.printSolution(-1)  # return current alpha value
                sys.exit(0)  # stop the program

            logging.debug(" Threshold reached at level " + str(depth))
            score = self.evaluateBoard(board, player)  # evaluate current board state and return score, move
            return score, move

        emptyTiles = self.getEmptyTiles(board)

        if player == Solution.MAX:

            for i in emptyTiles:
                child = deepcopy(board)
                x = int(math.floor(i / self.boardSize))
                y = int(math.floor(i % self.boardSize))
                child[x][y] = '1'

                score = self.minMax(child, Solution.MIN, alpha, beta, depth + 1)[0]

                logging.debug(" Player: " + ' Max ' + "alpha score: " + str(alpha) + " best move " + str(
                    move) + " current score: " + str(score) + " current move " + str(i) + ' board ' + str(
                    child) + " depth: " + str(depth))

                if score > alpha:
                    alpha = score
                    move = i
                    self.currentBest = i

                if alpha >= beta:  # pruning
                    break

        if player == Solution.MIN:
            for i in emptyTiles:
                child = deepcopy(board)
                x = int(math.floor(i / self.boardSize))
                y = int(math.floor(i % self.boardSize))
                child[x][y] = '1'
                score = self.minMax(child, Solution.MAX, alpha, beta, depth + 1)[0]

                logging.debug(" Beta score: " + str(beta) + " best move " + str(
                    move) + " current score: " + str(score) + " current move " + str(i) + ' board ' + str(
                    child) + " depth: " + str(depth))

                if score < beta:
                    beta = score
                    move = i

                if alpha >= beta:  # pruning
                    break

        if player == Solution.MAX:
            return alpha, move
        else:
            return beta, move

    def solve(self):
        board = self.board
        player = self.player
        return self.minMax(board, player, -sys.maxint, sys.maxint, 0)

    def printSolution(self, pos):

        if pos == -1:
            pos = self.currentBest

        boardSize = self.boardSize
        x = int(math.floor(pos % int(boardSize)))
        y = int(math.floor(pos / int(boardSize)))
        logging.info(
            " Next move is column : " + str(x + 1) + ' Row: ' + str(y + 1) + ' time ' + str(
                round(time.time() - self.programStartTime, 4)) + ' seconds')
        board = list(self.initialConfig)
        board[pos] = 'x'
        config = ''.join(board)
        print config


def main():
    boardSize = sys.argv[1]  # N : size of NxN board
    config = sys.argv[2]  # current board config represented by 'x' and '.'
    cutoff = sys.argv[3]  # time limit to take the decision
    cutoff = float(cutoff) * 1000.0  # convert to milliseconds value
    solution = Solution(boardSize, config, cutoff, Solution.MAX)
    score, pos = solution.solve()
    solution.printSolution(pos)
    return


if __name__ == '__main__':
    main()
