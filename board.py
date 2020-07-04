import numpy as np

def board_gen():
    flag = True
    board = np.zeros((8, 8))
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            offset = j
            if flag:
                offset += 1
            
            if offset % 2 == 0 and i < 3:
                board[i, j] = 1
            elif offset % 2 == 0 and i >= 5:
                board[i, j] = 2
    return board