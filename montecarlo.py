from node import Node
import numpy as np
import random
import utils

def montecarlo(board):
    turn = 1
    tree = Node(board, turn)

    iters = 0
    while iters < 10000:
        next_node, path = select(tree)
        if next_node != None and path != None:
            winner = rollout(next_node.state, next_node.turn)
            curr = tree
            for ind in path:
                curr = curr.children[ind]
                curr.visits += 1
                if winner == curr.turn:
                    curr.tot_val += 1
        
        iters += 1
    return tree

def select(tree):
    head = tree
    path = []
    while True:
        if len(head.children) == 0:
            next_states = utils.get_next_board_states(head.turn, head.state)
            if len(next_states) == 0:
                return None, None
            for i in range(len(next_states)):
                head.append_child(Node(next_states[i], utils.next_turn(head.turn)))
        
        unvisited = []
        for i in range(len(head.children)):
            if head.children[i].visits == 0:
                unvisited.append(i)

        if len(unvisited) == 0:
            max_arg = utils.get_max_ucb(head)
            head = head.children[max_arg]
            path.append(max_arg)
        else:
            next_ind = random.choice(unvisited)
            path.append(next_ind)
            return head.children[next_ind], path


def rollout(board, turn):
    curr_board = utils.copy_board(board)
    while True:
        next_states = utils.get_next_board_states(turn, curr_board)
        if len(next_states) == 0:
            break
        curr_board = random.choice(next_states)
        turn = utils.next_turn(turn)

    return utils.get_winner(curr_board)