from .win_detector import WinDetector
from .color import IllegalAction, COLORS, ORIENTATION, COLOR_SYMBOLS, \
    NUM_PLAYERS, color_to_player, next_player, player_to_color, cell_str, \
    cell_str_to_cell
from array import array
from games_puzzles_algorithms.debug import log


def prod(*l):
    s = 1
    for e in l:
        s *= e
    return s


class Board(object):

    _NEIGHBOR_PATTERNS = (
        (-1, 0), # North
        (0, -1), # West
        (-1, 1), # Northeast
        (0, 1),  # East
        (1, 0),  # South
        (1, -1)  # Southwest
    )

    def __init__(self, *dimensions):
        self.dimensions = list(dimensions)
        if len(self.dimensions) < 1:
            self.dimensions.append(10)
        if len(self.dimensions) < 2:
            self.dimensions.append(self.dimensions[0])
        self._cells = array('I', [COLORS['none']] * len(self))

        self._actions = [[] for _ in range(NUM_PLAYERS)]
        self._empty_cells = []
        self._my_cells = []
        for player in range(NUM_PLAYERS):
            self._empty_cells.append({})
            self._my_cells.append({})
            for a in range(len(self)):
                self._empty_cells[player][a] = True

    def __len__(self):
        return prod(*self.dimensions)

    def __getitem__(self, i):
        return self._cells[i]

    def __setitem__(self, i, color):
        self._cells[i] = color

    def is_color(self, player, row, column, color):
        return self._cells[self.cell_index(row, column)] == color

    def size(self):
        return self.dimensions

    def num_rows(self):
        return self.dimensions[0]

    def num_columns(self):
        return self.dimensions[1]

    def cell_index(self, x, y):
        return x * self.num_rows() + y

    def column(self, index):
        return index // self.num_rows()

    def row(self, index):
        return index % self.num_rows()

    def empty_cells(self):
        for action in self._empty_cells.keys():
            yield self.row(action), self.column(action)

    def cells(self):
        for y in range(self.num_columns()):
            for x in range(self.num_rows()):
                yield y, x

    def with_action_applied(self, action, player):
        color = self.play(action, player)
        yield color
        self.undo(player)

    def undo(self, player):
        '''Undo `player`'s last action.'''
        action = self._actions[player].pop()
        self._cells[action] = COLORS['none']
        self._empty_cells[player][cell_index] = True
        del self._my_cells[player][cell_index]
        return action

    def play(self, action, player):
        '''Apply `action` on behalf of `player`.

        Returns the color of the cell after attempting to set it to the
        player's color.
        '''
        color = player_to_color(player)

        opponent = next_player(player)

        # Already the player's color
        if self._cells[action] == color:
            raise IllegalAction(
                "Attempted to place for {} but collided with {} stone already on cell {}".format(
                    color, color, (self.row(action), self.column(action))
                )
            )
        else: # Set to player's color
            self._cells[action] = color
            self._my_cells[player][action] = True
            self._actions[player].append(action)

        del self._empty_cells[player][action]
        return color

    def num_legal_actions(self, player):
        return len(self._empty_cells[player])

    def legal_actions(self, player):
        for action in self._empty_cells[player].keys():
            yield action

    def is_valid_cell(self, row, column):
        return (
            0 <= row and row < self.num_rows() and
            0 <= column and column < self.num_columns()
        )

    def every_neighbor(self, row, column):
        """Yields each neighbor of the given cell on the given board one by one."""
        for neighbor_row_offset, neighbor_column_offset in self._NEIGHBOR_PATTERNS:
            neighbor_row = row + neighbor_row_offset
            neighbor_column = column + neighbor_column_offset
            if self.is_valid_cell(neighbor_row, neighbor_column):
                yield (neighbor_row, neighbor_column)

    def _to_s(self, get_color_fn):
        """Return an ASCII representation."""
        ret = '\n'
        coord_size = len(str(self.num_rows()))
        offset = 1
        ret += ' ' * (offset + 1)
        for x in range(self.num_columns()):
            ret += chr(ord('A') + x) + ' ' * offset * 2
        ret = ret.rstrip() + '\n'
        for y in range(self.num_rows()):
            ret += str(y + 1) + ' ' * (offset * 2 +
                                       coord_size - len(str(y + 1)))
            for x in range(self.num_columns()):
                ret += COLOR_SYMBOLS[get_color_fn(y, x)]
                ret += ' ' * offset * 2
            ret += COLOR_SYMBOLS[COLORS['white']]
            ret = ret.rstrip() + "\n" + ' ' * offset * (y + 1)
        ret += (
            (' ' * (offset * 2 + 1)) +
            (COLOR_SYMBOLS[COLORS['black']] + ' ' * offset * 2) *
            self.num_columns()
        )

        return ret.rstrip()

    def __str__(self):
        """Return an ASCII representation."""
        return self._to_s(
            lambda row, column: self._cells[self.board.cell_index(row, column)]
        )


class GameState(object):
    """Represents the current state of a game of dark hex (dex)."""

    @classmethod
    def root(self, *dimensions):
        return self(dimensions[0] if len(dimensions) > 0 else 10)

    def __init__(self, *dimensions):
        """
        Initialize the game board and give Black the first turn.
        Also create our union find structures for win checking.
        """
        self.acting_player = COLORS["black"]
        self.board = Board(*dimensions)
        self.win_detector = WinDetector.root(NUM_PLAYERS)
        self.previous_acting_players = []

    def undo(self):
        cell = None
        if self.previous_acting_players:
            previous_player = self.previous_acting_players.pop()
            self.win_detector.undo(previous_player)
            self.acting_player = previous_player
            cell = self.board.undo(previous_player)
            self._potentially_winning_moves = None
        return cell

    def __getitem__(self, cell):
        return self.board.color(self.player_to_act(), *cell)

    def is_empty(self, cell):
        return self.board.is_empty(self.player_to_act(), *cell)

    def num_actions_taken(self, player):
        return len(self.win_detector.history_of_player_groups[player])

    def with_action_applied(self, action):
        '''Not meant to be used recursively.

        This is a faster version of #play that does less bookkeeping.
        Useful when one wants to examine the state after playing but
        does not need to do this recursively or check if the game has ended.
        '''
        for _ in self.board.with_action_applied(action, self.acting_player):
            yield

    def previous_action_was_a_collision(self, previous_player=None):
        if previous_player is None:
            previous_player = self.previous_acting_players[-1]
        return previous_player == self.acting_player

    def undo(self):
        action = None
        if self.previous_acting_players:
            previous_player = self.previous_acting_players.pop()
            if previous_player != self.acting_player:
                self.win_detector.undo(previous_player)
                self.acting_player = previous_player
            action = self.board.undo(previous_player)
            self._potentially_winning_moves = None
        return action

    def play(self, cell):
        self.place(cell, self.acting_player)

    def do_after_play(self, action):
        self.play(action)
        yield
        self.undo()

    def place(self, action, player):
        """Place a stone for the given player regardless of whose turn it is."""
        if self.is_terminal():
            raise IllegalAction(
                "Game has finished and {} is the winner".format(self.winner())
            )
        color_after_placing = self.board.play(action, player)
        self.previous_acting_players.append(player)
        self._update_state(action, player, color_after_placing)
        self._potentially_winning_moves = None

    def score(self, player):
        return int(player == self.winner())

    def winner(self):
        return self.win_detector.winner()

    def is_terminal(self):
        return self.win_detector.is_terminal()

    def player_to_act(self):
        return self.acting_player

    def set_player_to_act(self, player):
        self.acting_player = player

    def _update_state(self, action, viewing_player, color_of_cell_that_changed):
        color = player_to_color(viewing_player)
        self.win_detector.update(
            self.board,
            viewing_player,
            (self.board.row(action), self.board.column(action)),
            action
        )
        self.acting_player = next_player(viewing_player)

    def legal_actions(self):
        for a in self.board.legal_actions(self.acting_player):
            yield a

    def num_legal_actions(self):
        return self.board.num_legal_actions(self.acting_player)

    def to_s(self, player):
        """Print an ascii representation of the game board."""
        return self.board.to_s(player)

    def __str__(self):
        """Print an ascii representation of the game board."""
        return str(self.board)
