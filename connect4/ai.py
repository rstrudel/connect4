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

    def step_tree(self, action):
        if action not in self.node:
            print('Game state not explored by MTCS.')
            self.node = {}
        else:
            self.node = self.node[action]

    def get_action(self, allowed_actions):
        node = self.node
        player = self.player

        idx_max = np.argmax(scores[player])
        action = allowed_actions[idx_max]
        self.step_tree(action)

        return action
