import numpy as np
from scipy.signal import convolve2d as conv2d


class Connect4:
    def __init__(self, size=(6, 7), length_connect=4):
        self.size = size
        self.length_connect = length_connect
        self.reset()
        self.init_win_patterns()

    def reset(self):
        size = self.size
        self.board = np.zeros(size, dtype=int)
        self.level_col = np.zeros(size[1], dtype=int)
        self.filled_col = np.zeros(size[1], dtype=bool)
        self.player = 1

    def init_win_patterns(self):
        length_connect = self.length_connect
        row_pattern = np.ones((1, length_connect))
        col_pattern = np.ones((length_connect, 1))
        diag0_pattern = np.eye(length_connect)
        diag1_pattern = diag0_pattern[::-1]
        self.win_patterns = [row_pattern,
                             col_pattern,
                             diag0_pattern,
                             diag1_pattern]

    def allowed_actions(self):
        return [i for i in range(self.size[1]) if not(self.filled_col[i])]

    def play(self, col):
        assert not(self.filled_col[col])
        level_col = self.level_col[col]
        self.board[level_col, col] = self.player
        self.level_col[col] += 1
        self.filled_col = self.level_col == self.size[0]
        self.player *= -1

    def is_won(self):
        board = self.board
        length_connect = self.length_connect

        won = 0
        for pattern in self.win_patterns:
            res = conv2d(board, pattern, mode='same')
            idx_max = np.unravel_index(np.abs(res).argmax(), res.shape)
            if abs(res[idx_max]) == length_connect:
                won = 2*int(res[idx_max] > 0)-1

        return won
