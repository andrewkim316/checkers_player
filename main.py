from board import board_gen, test_board
from montecarlo import montecarlo
import utils
import random

def main():
    board = board_gen()
    tree = montecarlo(board)
    head = tree
    while len(head.children) > 0:
        # for i in range(len(head.children)):
        #     utils.print_board(head.children[i].state)
        print(list(map(lambda x: x.visits, head.children)))
        max_arg = utils.get_max_ucb(head)
        head = head.children[max_arg]
        utils.print_board(head.state)

        

if __name__ == "__main__":
    main()