import os
from tqdm import tqdm
import time
from joblib import Parallel, delayed
import numpy as np

from .connect4 import Connect4
from .mcts import MCTS
from .node import Node

np.random.seed(0)


def explore(mcts, max_time, node=None, state=None):
    count = 0
    t0 = time.time()
    while time.time()-t0 < max_time:
        if state is not None:
            mcts.sim(node, state.copy())
        else:
            mcts.sim()
        count += 1
    # print('Played {} games'.format(count))


# initialize game and mcts
game_cls = Connect4
mcts = MCTS(game_cls)
explore(mcts, 2)

game = game_cls()
game.reset()

node = mcts.root
valid_actions = game.valid_actions(game.board)
player = 1
while game.is_won() == 0 and len(valid_actions) > 0:
    # human player move
    print('Board:\n', game.to_str())
    action = None
    while action not in valid_actions:
        action = int(input('action: '))
    game.play(action)
    node_action = node.get_child_action(action)
    if node_action is None:
        node_action = Node(game.board, game.is_won()*player,
                           action, node)
        node.add_child(node_action)
    node = node_action

    # ai player move
    explore(mcts, 1, node=node, state=game.board)
    node, action, scores = node.select_action()
    game.play(action)
    print('ai action: {}'.format(action))
    print('Scores', scores, '\n')
    valid_actions = game.valid_actions(game.board)

value2player = {-1: 2, 1: 1, 0: 0}
print('Board:\n', game.to_str())
print('Player {} won.'.format(value2player[game.is_won()]))
