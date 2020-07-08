class Node:
    def __init__(self, board, turn):
        self.parent = None
        self.children = []
        self.visits = 0
        self.tot_val = 0
        self.state = board
        self.turn = turn
    
    def append_child(self, child):
        self.children.append(child)
    
    def set_parent(self, parent):
        self.parent = parent

    def inc_visits(self, amt):
        self.visits += amt
    
    def inc_value(self, amt):
        self.tot_val += amt
    
    def print_node(self):
        print(self.visits, self.tot_val, self.state, self.turn)
    