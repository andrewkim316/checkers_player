class Node:
    def __init__(self, board):
        self.parent = None
        self.children = []
        self.visits = 0
        self.win_outcomes = 0
        self.state = board
    
    def append_child(self, child):
        self.children.append(child)
    
    def set_parent(self, parent):
        self.parent = parent

    def inc_visits(self, amt):
        self.visits += amt
    
    def inc_win_outcomes(self, amt):
        self.win_outcomes += amt
    