# minmax-ramses-player
Min-max based Ramses game player 

Rameses is a two-player game that requires a board having an n X n grid and n2 pebbles. Initially
the board starts empty and all pebbles are in a pile beside the board. Player 1 picks up a pebble and
places it in any square of the grid. Player 2 then picks up a pebble from the pile, and places it in any
open square (i.e. any square except the one selected by Player 1). Play continues back and forth, with
each player picking up a pebble from the pile and placing it in any open square. A player loses the
game as soon as they place a pebble that completes a row, a column, or one of the two diagonals of
the board, and then the other player wins.

The program is a ramses player. It accepts a command line argument that gives the current state of the board as a string of x's and .'s, where x
indicates a pebble and . indicates an empty square, respectively, in row-major order. The program needs to be called with three command line parameters: (1) the value of n,
(2) the state of the board, encoded as above, and (3) a time limit in seconds. The program decides a recommended move given the current board state, and display the new state of the board
after making that move, within the number of seconds specified.