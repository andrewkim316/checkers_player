from functools import reduce
import numpy as np

def get_next_board_states(turn, board):
    next_states = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == turn:
                next_states.extend(get_normal_moves(board, (i, j), turn))
            elif board[i][j] == turn * 10:
                next_states.extend(get_king_moves(board, (i, j), turn))

    return next_states

def get_king_moves(board, loc, turn):
    outcomes = []
    new_locs = [(loc[0] + 1, loc[1] - 1), (loc[0] - 1, loc[1] - 1), (loc[0] + 1, loc[1] + 1), (loc[0] - 1, loc[1] + 1)]
    
    for i in range(len(new_locs)):
        if is_on_board(new_locs[i]):
            if board[new_locs[i][0]][new_locs[i][1]] == 0:
                outcomes.append(move(board, loc, new_locs[i]))
            elif can_jump(turn, board[new_locs[i][0]][new_locs[i][1]]):
                jump = (new_locs[i][0] + (new_locs[i][0] - loc[0]), new_locs[i][1] + (new_locs[i][1] - loc[1]))
                if is_on_board(jump) and board[jump[0]][jump[1]] == 0:
                    board_copy = copy_board(board)
                    board_copy[new_locs[i][0]][new_locs[i][1]] = 0
                    outcomes.extend(get_king_jumps(move(board_copy, loc, jump), jump, turn, loc))
    
    return outcomes
                

def get_normal_moves(board, loc, turn):
    offset = get_offset(turn)
    outcomes = []
    new_locs = [(loc[0] + offset, loc[1] - 1), (loc[0] + offset, loc[1] + 1)]

    for i in range(len(new_locs)):
        if is_on_board(new_locs[i]):
            if board[new_locs[i][0]][new_locs[i][1]] == 0:
                outcomes.append(move(board, loc, new_locs[i]))
            elif can_jump(turn, board[new_locs[i][0]][new_locs[i][1]]):
                jump = (new_locs[i][0] + (new_locs[i][0] - loc[0]), new_locs[i][1] + (new_locs[i][1] - loc[1]))
                if is_on_board(jump) and board[jump[0]][jump[1]] == 0:
                    board_copy = copy_board(board)
                    board_copy[new_locs[i][0]][new_locs[i][1]] = 0
                    outcomes.extend(get_jumps(move(board_copy, loc, jump), jump, turn))
    
    return outcomes

def get_king_jumps(board, loc, turn, came_from):
    outcomes = []
    new_locs = [(loc[0] + 1, loc[1] - 1), (loc[0] - 1, loc[1] - 1), (loc[0] + 1, loc[1] + 1), (loc[0] - 1, loc[1] + 1)]
    for i in range(len(new_locs)):
        if new_locs[i][0] == came_from[0] and new_locs[i][1] == came_from[1]:
            new_locs.pop(i)
            break

    to_check = []
    for i in range(len(new_locs)):
        to_check.append(not is_on_board(new_locs[i]) or not can_jump(turn, board[new_locs[i][0]][new_locs[i][1]]))

    for i in range(len(to_check)):
        if not to_check[i]:
            jump = (new_locs[i][0] + (new_locs[i][0] - loc[0]), new_locs[i][1] + (new_locs[i][1] - loc[1]))
            if is_on_board(jump) and board[jump[0]][jump[1]] == 0:
                board_copy = copy_board(board)
                board_copy[new_locs[i][0]][new_locs[i][1]] = 0
                outcomes.extend(get_king_jumps(move(board_copy, loc, jump), jump, turn, loc))

    if len(outcomes) == 0:
        outcomes.append(board)

    return outcomes

def get_jumps(board, loc, turn):
    offset = get_offset(turn)
    outcomes = []
    new_locs = [(loc[0] + offset, loc[1] - 1), (loc[0] + offset, loc[1] + 1)]

    to_check = []
    for i in range(len(new_locs)):
        to_check.append(not is_on_board(new_locs[i]) or not can_jump(turn, board[new_locs[i][0]][new_locs[i][1]]))

    for i in range(len(to_check)):
        if not to_check[i]:
            jump = (new_locs[i][0] + (new_locs[i][0] - loc[0]), new_locs[i][1] + (new_locs[i][1] - loc[1]))
            if is_on_board(jump) and board[jump[0]][jump[1]] == 0:
                board_copy = copy_board(board)
                board_copy[new_locs[i][0]][new_locs[i][1]] = 0
                outcomes.extend(get_jumps(move(board_copy, loc, jump), jump, turn))

    if len(outcomes) == 0:
        outcomes.append(board)
    
    return outcomes


def get_offset(turn):
    if turn == 1:
        return 1
    else:
        return -1

def can_jump(turn, target):
    if turn == 1:
        return target == 20 or target == 2
    else:
        return target == 10 or target == 1


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


def is_on_board(coords):
    return coords[0] >= 0 and coords[0] < 8 and coords[1] >= 0 and coords[1] < 8


def print_board(board):
    out_str = ""
    for i in range(len(board)):
        out_str += f"{' '.join(map(lambda x: f'{x} ' if x < 10 else str(x), board[i]))}\n"
    
    print(out_str)

def next_turn(turn):
    if turn == 1:
        return 2
    else:
        return 1

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

def copy_board(board):
    return list(map(list, board))

def same_board(board1, board2):
    for i in range(len(board1)):
        for j in range(len(board1[i])):
            if board1[i][j] != board2[i][j]:
                return False

    return True

def get_max_ucb(tree):
    N = reduce(lambda x, y: x + y, list(map(lambda z: z.visits, tree.children)))
    ucbs = list(map(lambda x: ucb1((x.tot_val / x.visits), 2, N, x.visits) if x.visits != 0 else 0, tree.children))
    return np.argmax(np.array(ucbs))

def ucb1(value, constant, N, n):
    return value + constant * ((np.log(N) / n) ** 2)