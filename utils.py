from functools import reduce
import numpy as np

# Gets the next board states for the given turn and board
def get_next_board_states(board, turn):
    next_states = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == turn or board[i][j] == turn * 10:
                next_states.extend(get_moves(board, (i, j), turn))
    return next_states

# Gets all possible moves for one location
def get_moves(board, loc, turn):
    outcomes = []
    if (board[loc[0]][loc[1]] == turn * 10):
        new_locs = [(loc[0] + 1, loc[1] - 1), (loc[0] - 1, loc[1] - 1), (loc[0] + 1, loc[1] + 1), (loc[0] - 1, loc[1] + 1)]
    else:
        offset = get_offset(turn)
        new_locs = [(loc[0] + offset, loc[1] - 1), (loc[0] + offset, loc[1] + 1)]

    for i in range(len(new_locs)):
        if is_on_board(new_locs[i]):
            if board[new_locs[i][0]][new_locs[i][1]] == 0:
                outcomes.append(move(board, loc, new_locs[i]))
            elif can_jump(turn, board[new_locs[i][0]][new_locs[i][1]]):
                jumped, new_board, jump = jump_util(board, loc, new_locs[i], turn)
                if jumped:
                    outcomes.extend(get_jumps(move(new_board, loc, jump), jump, turn, new_locs[i]))
    return outcomes

# Gets all possible jumps for one location
def get_jumps(board, loc, turn, came_from):
    outcomes = []
    locs = [(loc[0] + 1, loc[1] - 1), (loc[0] - 1, loc[1] - 1), (loc[0] + 1, loc[1] + 1), (loc[0] - 1, loc[1] + 1)]
    new_locs = []
    
    bad_locs = [came_from]
    if not (board[loc[0]][loc[1]] == turn * 10):
        bad_locs.append((came_from[0], came_from[1] + 2 * (loc[1] - came_from[1])))
    for i in range(len(locs)):
        if locs[i] in bad_locs or not is_on_board(locs[i]) or not can_jump(turn, board[locs[i][0]][locs[i][1]]):
            continue
        new_locs.append(locs[i])

    for i in range(len(new_locs)):
        if can_jump(turn, board[new_locs[i][0]][new_locs[i][1]]):
            jumped, new_board, jump = jump_util(board, loc, new_locs[i], turn)
            if jumped:
                outcomes.extend(get_jumps(move(new_board, loc, jump), jump, turn, new_locs[i]))

    if len(outcomes) == 0:
        outcomes.append(board)

    return outcomes

# Performs a jump if possible
def jump_util(board, loc, new_loc, turn):
    loc_diff = (new_loc[0] - loc[0], new_loc[1] - loc[1])
    jump = (new_loc[0] + loc_diff[0], new_loc[1] + loc_diff[1])
    if is_on_board(jump) and board[jump[0]][jump[1]] == 0:
        board_copy = copy_board(board)
        board_copy[new_loc[0]][new_loc[1]] = 0
        return True, board_copy, jump
    else:
        return False, board, jump

# Returns the direction each player is going (1 -> down, 2 -> up)
def get_offset(turn):
    if turn == 1:
        return 1
    else:
        return -1

# Returns whether or not the player can jump a board spot
def can_jump(turn, target):
    if turn == 1:
        return target == 20 or target == 2
    else:
        return target == 10 or target == 1

# Performs a move on the board and returns a copy (old board is not changed)
def move(board, old, new):
    board_copy = copy_board(board)
    temp = board_copy[old[0]][old[1]]
    board_copy[old[0]][old[1]] = board_copy[new[0]][new[1]]
    board_copy[new[0]][new[1]] = temp

    if temp == 1 and new[0] == len(board) - 1:
        board_copy[new[0]][new[1]] = 10
    
    if temp == 2 and new[0] == 0:
        board_copy[new[0]][new[1]] = 20

    return board_copy

# Returns whether or not the coordinates are on the board
def is_on_board(coords):
    return coords[0] >= 0 and coords[0] < 8 and coords[1] >= 0 and coords[1] < 8

# Neatly prints the board
def print_board(board):
    out_str = ""
    for i in range(len(board)):
        out_str += f"{' '.join(map(lambda x: f'{x} ' if x < 10 else str(x), board[i]))}\n"
    print(out_str)

# Changes the turn
def next_turn(turn):
    if turn == 1:
        return 2
    else:
        return 1

# Gets the winner of the assumed terminal board state
def get_winner(board):
    pieces_left = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 10 or board[i][j] == 1:
                pieces_left.add(1)
            elif board[i][j] == 20 or board[i][j] == 2:
                pieces_left.add(2)
    
    if 1 in pieces_left and 2 in pieces_left:
        return 0
    elif 1 in pieces_left:
        return 1
    elif 2 in pieces_left:
        return 2
    else:
        return 0

# Copies the board
def copy_board(board):
    return list(map(list, board))

# Determines whether or not two boards are the same
def same_board(board1, board2):
    for i in range(len(board1)):
        for j in range(len(board1[i])):
            if board1[i][j] != board2[i][j]:
                return False
    return True

# Return the arg in an array that has the max UCB measurement
def get_max_ucb(tree):
    N = reduce(lambda x, y: x + y, list(map(lambda z: z.visits, tree.children)))
    ucbs = list(map(lambda x: ucb1((x.tot_val / x.visits), 2, N, x.visits) if x.visits != 0 else 0, tree.children))
    return np.argmax(np.array(ucbs))

# Returns the UCB measure of a state
def ucb1(value, constant, N, n):
    return value + constant * ((np.log(N) / n) ** 2)

# Generates a board given the inputs
def board_gen(inputs):
    board = [[0 for j in range(8)] for i in range(8)]
    for i in range(len(inputs)):
        board[inputs[i][0]][inputs[i][1]] = inputs[i][2]
    return board
