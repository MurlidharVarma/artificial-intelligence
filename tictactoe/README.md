# Tic-Tac-Toe
An AI to play Tic-Tac-Toe optimally using Minimax algorithm


## Screencast
[![Project 0b: Tic-Tac-Toe](https://img.youtube.com/vi/NNn6DZxU3Wk/0.jpg)](https://youtu.be/NNn6DZxU3Wk)

## Understanding
There are two main files in this project: `runner.py` and `tictactoe.py`. `tictactoe.py` contains all of the logic for playing the game, and for making optimal moves. `runner.py` contains all of the code to run the graphical interface for the game. 

In `tictactoe.py` we define three variables: X, O, and EMPTY, to represent possible moves of the board.

The function `initial_state` returns the starting state of the board. The board is represented as a list of three lists (representing the three rows of the board), where each internal list contains three values that are either X, O, or EMPTY.