import numpy as np

from .mcts import MCTS

class AI:
    def __init__(self, mcts, player=0):
        self.mcts = mcts
        self.player = player
        self.reset()

    def set_player(player):
        self.player = player

    def reset(self):
        self.node = self.mcts.tree.root

    def opponent_action(self, action):
        if action not in self.node:
            print('Game state not explored by MTCS.')
            self.node = {}
        else:
            self.node = self.node[action]

    def get_action(self, allowed_actions):
        node = self.node
        player = self.player

        scores = []
        for action in allowed_actions:
            if action in node:
                scores.append(node[action]['win_p{}'.format(player+1)]/node[action]['count'])
            else:
                scores.append(0)

        idx_max = np.argmax(scores)
        return allowed_actions[idx_max]
