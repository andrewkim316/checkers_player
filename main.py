from board import board_gen, test_board
from utils import get_next_board_states, print_board, next_turn
import random

def main():
    curr_board = board_gen()

    iters = 0
    turn = 1
    while True:
        next_states = get_next_board_states(turn, curr_board)
        if len(next_states) == 0:
            break
        curr_board = random.choice(next_states)
        turn = next_turn(turn)
        iters += 1
    print_board(curr_board)
    print(iters / 2)

        

if __name__ == "__main__":
    main()