import numpy as np

from .node import Node

class MCTS:
    def __init__(self, game_cls):
        self.game_cls = game_cls
        game = game_cls()
        self.root = Node(game.board, 0, None, None)

    def sim(self, relative_root=None, state=None):
        # instantiate one game per sim
        game = self.game_cls()
        player = 1
        node = self.root if relative_root is None else relative_root
        if state is not None:
            game.set_board(state)
            player = game.active_player(state)

        # exploration
        valid_actions = game.valid_actions(game.board)
        is_won = game.is_won()
        while is_won == 0 and len(valid_actions) > 0:

            # choose action
            children = [node.get_child_action(action) for action in valid_actions]
            if None in children:
                action = np.random.choice(valid_actions)
            else:
                scores = [child.get_ucb() for child in children]
                action = valid_actions[np.argmax(scores)]

            # update game state and action child node
            game.play(action)
            is_won = game.is_won()
            node_action = node.get_child_action(action)
            if node_action is None:
                node_action = Node(game.board.copy(), 0,
                                   action, node)
                node.add_child(node_action)
            node = node_action
            valid_actions = game.valid_actions(game.board)
            player *= -1


        # backprop
        player_last_move = -1*player
        node.winner = is_won != 0
        parent = node
        count = 0
        while parent is not None:
            count += 1
            parent.games += 1
            if game.active_player(parent.state) != is_won:
                parent.win += 1
            parent = parent.parent
