from tqdm import tqdm

from .connect4 import Connect4
from .mcts import MCTS
from .ai import AI

game = Connect4()
mcts = MCTS(game)
num_self_play = 5*10**4
print('feza', num_self_play)

# explore game using MCTS
for _ in tqdm(range(num_self_play)):
    mcts.sim()
game.reset()

ai_player = AI(mcts, player=1)

while True:
    while game.is_won() == 0:
        print('Board:\n', game.board[::-1], '\n')
        action = -1
        while action not in game.allowed_actions():
            action = int(input('Action:'))
        game.play(action)
        ai_player.opponent_action(action)
        ai_action = ai_player.get_action(game.allowed_actions())
        game.play(ai_action)
        print('AI played action {}.\n'.format(ai_action))
    print('Game won by {}'.format(game.is_won()))
    game.reset()
