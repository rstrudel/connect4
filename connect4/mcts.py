import numpy as np


class Tree:
    def __init__(self):
        self.root = {'win_p1': 0, 'win_p2': 0, 'draw': 0, 'count': 0}

    def fill(self, actions, win):
        node = self.root
        win2key = {1: 'win_p1', -1: 'win_p2', 0: 'draw'}
        key_game = win2key[win]

        for action in actions:
            node[key_game] += 1
            node['count'] += 1
            node_child = None
            if action in node:
                node_child = node[action]
            else:
                node[action] = {'win_p1': 0, 'win_p2': 0, 'draw': 0, 'count': 0}
                node_child = node[action]
            node = node_child

class MCTS:
    def __init__(self, game):
        self.tree = Tree()
        self.root = self.tree.root
        self.game = game
        self.c_exp = 1

    def action_explore(self, node, actions, player):
        c_exp = self.c_exp

        unexplored_actions = []
        scores = []
        for action in actions:
            if action in node:
                score = node[action]['win_p{}'.format(player+1)]/node[action]['count']+\
                        c_exp*np.sqrt(np.log(node['count'])/node[action]['count'])
                scores.append(score)
            else:
                unexplored_actions.append(action)
                scores.append(0)

        if unexplored_actions:
            rand_idx = np.random.randint(len(unexplored_actions))
            action = unexplored_actions[rand_idx]
        else:
            idx_max = np.argmax(scores)
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
        count = 0
        while is_won == 0 and allowed_actions:
            action = self.action_explore(node, allowed_actions, count%2)
            actions.append(action)
            if 'action' in node:
                node = node[action]
            else:
                node = {}
            game.play(action)
            allowed_actions = game.allowed_actions()
            is_won = game.is_won()
            count += 1
        tree.fill(actions, is_won)
