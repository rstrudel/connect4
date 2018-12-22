import numpy as np
from anytree import Node


class Tree:
    def __init__(self):
        self.root = {'win': 0, 'count': 0}

    def fill(self, actions, win):
        node = self.root[actions[0]]
        for i, action in enumerate(actions[1:]):
            node_win = int(win == (i+1) % 2)
            node['win'] += node_win
            node['count'] += 1
            node_child = None
            if action in node:
                node_child = node[action]
            else:
                node[action] = {'win': 0, 'count': 0}
                node_child = node[action]
            node = node_child

class MCTS:
    def __init__(self, game):
        self.tree = Tree()
        self.root = self.tree.root
        self.game = game
        self.c_exp = 1

    def action_explore(self, node, actions):
        c_exp = self.c_exp

        unexplored_actions = []
        score_max = 0
        idx_max = 0
        for i, action in enumerate(actions):
            if action in node:
                score = node[action]['win']/node[action]['count']+\
                        c_exp*np.sqrt(np.log(node['count'])/node[action]['count'])
                if score > score_max:
                    score = score_max
                    idx_max = i
            else:
                unexplored_actions.append(action)

        if unexplored_actions:
            action = unexplored_actions[
                np.random.randint(len(unexplored_actions))]
        else:
            action = actions[idx_max]

        return action

    def sim(self):
        game = self.game
        tree = self.tree
        node = self.root
        game.reset()

        actions = []
        allowed_actions = game.allowed_actions()
        is_won = 0
        while is_won == 0 and allowed_actions:
            action = self.action_explore(node, allowed_actions)
            actions.append(action)
            if 'action' in node:
                node = node[action]
            else:
                node = {}
            game.play(action)
            allowed_actions = game.allowed_actions()
            is_won = game.is_won()
        tree.fill(actions, is_won)
