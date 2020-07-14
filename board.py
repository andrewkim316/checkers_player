# Returns the beginning board state
def init_board():
    flag = True
    board = [[0 for j in range(8)] for i in range(8)]
    for i in range(len(board)):
        for j in range(len(board[i])):
            offset = j
            if flag:
                offset += 1
            
            if offset % 2 == 0 and i < 3:
                board[i][j] = 1
            elif offset % 2 == 0 and i >= 5:
                board[i][j] = 2
        flag = not flag
    return board
