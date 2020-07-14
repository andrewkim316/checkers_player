from board import init_board
from montecarlo import montecarlo
import utils
import random
import sys

def main():
    # Handles command line args
    if len(sys.argv) != 3:
        print("Incorrect amount of args")
        return
    
    args = sys.argv[1:]
    try:
        int(args[0])
        float(args[1])
    except ValueError:
        print("Incorrect arg types")
        return
    

    if(int(args[0]) != 1 and float(args[1]) != 2):
        print("Turn arg must be 1 or 2")
        return

    # Initializes board
    board = init_board()
    turn = int(args[0])
    print("Initial board:")
    utils.print_board(board)

    # Loops until someone wins
    while len(utils.get_next_board_states(board, turn)) > 0:
        board = montecarlo(board, turn, float(args[1]))
        print(f"{turn} goes")
        utils.print_board(board)
        turn = utils.next_turn(turn)
    
    print(f"{utils.next_turn(turn)} wins!")

        

if __name__ == "__main__":
    main()