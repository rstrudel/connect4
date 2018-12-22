import numpy as np

class Node:
    def __init__(self, state, winning, action, parent):
        self.parent = parent
        self.state = state
        self.action = action
        self.win = 0
        self.games = 0
        self.children = []
        self.winner = winning
        self.c_exp = np.sqrt(2)

    def add_child(self, child):
        assert isinstance(child, Node)
        self.children.append(child)

    def get_ucb(self):
        if self.games == 0:
            return None
        return self.win/self.games+self.c_exp*np.sqrt(np.log(self.parent.games)/self.games)

    def select_action(self):
        if not self.children:
            return None, None, None

        winners = [child for child in self.children if child.winner]
        if len(winners) > 0:
            return winners[0], winners[0].action, ''

        scores = [child.win/child.games if child.games > 0 else 0
                 for child in self.children]

        best_child = self.children[np.argmax(scores, axis=0)]

        scores_actions = [[child.win/child.games, child.action] if child.games > 0 else 0
                 for child in self.children]
        scores_actions = sorted(scores_actions, key=lambda x:x[1])
        scores_actions = np.array(scores_actions)[:, 0]

        str_scores = ''
        for sc in scores_actions:
            str_scores += '{:.2f} '.format(sc)

        return best_child, best_child.action, str_scores

    def get_child_action(self, action):
        for child in self.children:
            if child.action == action:
                return child
        return None
