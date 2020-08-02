"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],  
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board) == True:
        return None
    else:
        x_moves = 0
        o_moves = 0

        for row in board:
            for col in row:
                if col == X:
                    x_moves += 1
                elif col == O:
                    o_moves += 1

        if x_moves > o_moves:
            return O
        elif o_moves >= x_moves:
            return X
        elif o_moves == 0 and x_moves == 0:
            return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    size = len(board)
    for i in range(0, size):
        for j in range(0, size):
            if board[i][j] == EMPTY:
                action_set.add((i, j))
    return action_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check if action is invalid, else raise exception
    if action == None:
        raise NameError("Invalid action") 

    i = action[0]
    j = action[1]

    # check if position in board is empty, else raise exception
    if board[i][j] != EMPTY:
        raise NameError("Invalid action")    

    # get current player
    curr_player = player(board)

    # assign current player to the cloned board
    result_board = cloneBoard(board)
    result_board[i][j] = curr_player

    return result_board

def cloneBoard(board):
    """
    Returns a deep clone of a passed in board
    """
    clone = []
    for row in board:
        clone.append(row.copy())
    
    return clone

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_if_winner(X,board):
        return X
    elif check_if_winner(O,board):
        return O
    else:
        return None

def check_if_winner(player, board):
    is_winner = False
    size = len(board)

    # to keep track of diagnol occurrance of player
    diag_1_count = 0
    diag_2_count = 0

    # vertical check - outer loop
    for k in range(0,size):
        vertical_count = 0

        # vertical check - inner loop
        for i in range(0,size):
            horizontal_count = 0

            # check player occurance horizontally
            for j in range(0,size):
                if board[i][j] == player:
                    horizontal_count += 1
            
            # if horizontal count is equal to size, then player is winner
            if horizontal_count == size:
                is_winner = True
                break

            if board[i][k] == player:
                vertical_count += 1
        
        # if horizontally winner is found then break, else check vertical
        if is_winner:
            break
        elif vertical_count == size:
            is_winner = True
            break
        
        # checking diagonally
        if board[k][k] == player:
            diag_1_count += 1

        if board[k][size-1-k] == player:
            diag_2_count += 1

    if diag_1_count == size or diag_2_count == size:
        is_winner = True

    return is_winner    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    has_empty_cell = False
    for row in board:
        for col in row:
            if col == EMPTY:
                has_empty_cell = True
                break
        
        if has_empty_cell:
            break

    # if there are no empty cells or there is a winner, then return true
    if has_empty_cell == False or winner(board) != None:
        return True
    else:
        return False
        

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    score = 0
    player_won = winner(board)

    if player_won == X:
        score = 1
    elif player_won == O:
        score = -1
    
    return score

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # max value method with alpha-beta pruning
    def max_value(board, alpha, beta):

        # if terminal state then return utility of the board
        if terminal(board):
            return utility(board)

        # initializing best max to negative Infinity
        best_max = - math.inf
        action_set = actions(board)

        # iterate to all possible actions
        for action in action_set:

            # apply action to the given board state
            action_result = result(board, action)

            # evaluate score of what a min player would do
            score = min_value(action_result, alpha, beta)

            # Get the max value against all possible action score
            if score > best_max:
                best_max = score
            
            # if score is greater than beta then prune
            if beta != None and score >= beta:
                return score
            
            # update value of alpha if score is greater
            if alpha == None or score > alpha:
                alpha = score
            
        return best_max

    # min value method with alpha-beta pruning
    def min_value(board, alpha, beta):

        # if terminal state then return utility of the board
        if terminal(board):
            return utility(board)

        # initializing best min to positive Infinity
        best_min = math.inf
        action_set = actions(board)

        # iterate to all possible actions
        for action in action_set:

            # apply action to the given board state
            action_result = result(board, action)

            # evaluate score of what a max player would do
            score = max_value(action_result, alpha, beta)

            # Get the min value against all possible action score
            if score < best_min:
                best_min = score
            
            # if score is greater than beta then prune
            if alpha != None and score <= alpha:
                return score
            
            # update value of alpha if score is greater
            if beta == None or score < beta:
                beta = score

        return best_min    
    
    # get the current player
    current_player = player(board)

    # initalize
    best_action = None
    alpha = None
    beta = None

    # if current player is Max player X
    if current_player == X:
        # initialize best score to negative infinity
        best_score = - math.inf

        # iterate thru all possible actions, and choose best action
        for action in actions(board):
            result_board = result(board, action)
            score = min_value(result_board, alpha, beta)
            
            # if the score found is greater than best_score so far, 
            # then record the action as best action
            if score >= best_score:
                best_score = score
                best_action = action

    # if current player is Min player O
    elif current_player == O:
        # initialize best score to postive infinity
        best_score = math.inf

        # iterate thru all possible actions, and choose best action
        for action in actions(board):
            result_board = result(board, action)
            score = max_value(result_board, alpha, beta)

            # if the score found is less than best_score so far, 
            # then record the action as best action
            if score <= best_score:
                best_score = score
                best_action = action
    
    # return best action
    return best_action