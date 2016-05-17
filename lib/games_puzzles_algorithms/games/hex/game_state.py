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
        (-1, 0),  # North
        (0, -1),  # West
        (-1, 1),  # Northeast
        (0, 1),   # East
        (1, 0),   # South
        (1, -1)   # Southwest
    )

    def __init__(self, *dimensions):
        self._dimensions = list(dimensions)
        if len(self._dimensions) < 1:
            self._dimensions.append(10)
        if len(self._dimensions) < 2:
            self._dimensions.append(self._dimensions[0])
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
        return prod(*self.size())

    def is_empty(self, player, *cell):
        return self.cell_index(*cell) in self._empty_cells[player]

    def color(self, row, column):
        return self._cells[self.cell_index(row, column)]

    def my_cells(self, player):
        return self._my_cells[player].keys()

    def is_color(self, player, row, column, color):
        return self._cells[self.cell_index(row, column)] == color

    def size(self):
        return self._dimensions

    def num_rows(self):
        return self.size()[0]

    def num_columns(self):
        return self.size()[1]

    def cell_index(self, row, column):
        return (column * self.num_rows()) + row

    def row(self, cell_index):
        return cell_index % self.num_rows()

    def column(self, cell_index):
        return cell_index // self.num_rows()

    def empty_cells(self):
        for action in self._empty_cells.keys():
            yield self.row(action), self.column(action)

    def cells(self):
        for row in range(self.num_columns()):
            for column in range(self.num_rows()):
                yield row, column

    def with_action_applied(self, action, player):
        color = self.play(action, player)
        yield color
        self.undo(player)

    def undo(self, player):
        '''Undo `player`'s last action.'''
        action = self._actions[player].pop()
        self._cells[action] = COLORS['none']
        self._empty_cells[player][action] = True
        del self._my_cells[player][action]
        return action

    def play(self, action, player):
        '''Apply `action` on behalf of `player`.

        Returns the color of the cell after attempting to set it to the
        player's color.
        '''
        color = player_to_color(player)

        opponent = next_player(player)

        # Already has a stone.
        if self._cells[action] != COLORS["none"]:
            raise IllegalAction(
                ("Attempted to place for {} but collided with {} stone already"
                 " on cell {}").format(
                    color, color, (self.row(action), self.column(action))
                )
            )
        else:  # Set to player's color
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
        """Generate neighbors of `cell`."""
        for (neighbor_row_offset,
             neighbor_column_offset) in self._NEIGHBOR_PATTERNS:
            neighbor_row = row + neighbor_row_offset
            neighbor_column = column + neighbor_column_offset
            if self.is_valid_cell(neighbor_row, neighbor_column):
                yield (neighbor_row, neighbor_column)

    def every_legal_neighbor(self, player, *cell):
        """Generate neighbors of `cell` that can be played on by `player`."""
        for neighbor in self.every_neighbor(*cell):
            if self.cell_index(*neighbor) in self._empty_cells[player]:
                yield neighbor

    def length_separating_goal_sides(self, player):
        return self.size()[player]

    def __str__(self):
        """Return an ASCII representation."""
        return self._to_s(self.color)

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


class GameState(object):
    """Represents the current state of a game of dark hex (dex)."""

    @classmethod
    def clean_board(self, *dimensions):
        return Board(*dimensions)

    @classmethod
    def root(self, *dimensions):
        """Initialize the game board and give White first turn."""
        if len(dimensions) < 1:
            num_rows = 6
        else:
            num_rows = dimensions[0]
        num_columns = num_rows if len(dimensions) < 2 else dimensions[1]
        return self(
            color_to_player(COLORS["white"]),
            self.clean_board(num_rows, num_columns),
            WinDetector.root(NUM_PLAYERS)
        )

    def __init__(self, acting_player, board, win_detector):
        self._acting_player = acting_player
        self._previous_acting_players = []
        self.board = board
        self.win_detector = win_detector
        self._potentially_winning_moves = None

    def __getitem__(self, cell):
        return self.board.color(self.player_to_act(), *cell)

    def could_terminate_in_one_action(self, player=None):
        '''
        Returns whether or not `player` can end the game in one
        action.

        `player`: Player index, {0, 1}. Defaults to `player_to_act`.
        '''
        return (self.num_actions_taken(self._acting_player)
                >= (self.board.length_separating_goal_sides(
                        self._acting_player) - 1))

    def potentially_winning_moves(self):
        if self._potentially_winning_moves is not None:
            for m in self._potentially_winning_moves.keys():
                yield m
        else:
            self._potentially_winning_moves = {}
            if self.could_terminate_in_one_action():
                original_group = (self.win_detector
                                  .current_groups[self._acting_player]
                                  .copy_raw())
                color = player_to_color(self._acting_player)
                for my_cell_index in self.board.my_cells(self._acting_player):
                    for cell in self.board.every_legal_neighbor(
                                    self._acting_player,
                                    self.board.row(my_cell_index),
                                    self.board.column(my_cell_index)):

                        a = self.board.cell_index(*cell)
                        if a not in self._potentially_winning_moves:
                            self.win_detector.imagined_update(
                                self.board, self._acting_player, cell, a)

                            if self.win_detector.check_if_winner(
                                    self._acting_player):

                                (self.win_detector
                                 .current_groups[self._acting_player]
                                 .copy_from_raw(original_group))
                                self.win_detector._winner = COLORS['none']
                                self._potentially_winning_moves[a] = True
                                yield a
                            else:
                                (self.win_detector
                                 .current_groups[self._acting_player]
                                 .copy_from_raw(original_group))

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
        for _ in self.board.with_action_applied(action, self._acting_player):
            yield

    def previous_action_was_a_collision(self, previous_player=None):
        if previous_player is None:
            previous_player = self._previous_acting_players[-1]
        return previous_player == self._acting_player

    def undo(self):
        action = None
        if self._previous_acting_players:
            previous_player = self._previous_acting_players.pop()
            if previous_player != self._acting_player:
                self.win_detector.undo(previous_player)
                self._acting_player = previous_player
            action = self.board.undo(previous_player)
            self._potentially_winning_moves = None
        return action

    def play(self, cell):
        self.place(cell, self._acting_player)

    def do_after_play(self, action):
        self.play(action)
        yield
        self.undo()

    def place(self, action, player):
        """
        Place a stone for the given player regardless of whose turn it is.
        """
        if self.is_terminal():
            raise IllegalAction(
                "Game has finished and {} is the winner".format(self.winner())
            )
        color_after_placing = self.board.play(action, player)
        self._previous_acting_players.append(player)
        self._update_state(action, player, color_after_placing)
        self._potentially_winning_moves = None

    def score(self, player):
        if self.is_terminal():
            return 1 if player == self.winner() else -1
        else:
            return None

    def winner(self):
        return self.win_detector.winner()

    def is_terminal(self):
        return self.win_detector.is_terminal()

    def player_to_act(self):
        return self._acting_player

    def set_player_to_act(self, player):
        self._acting_player = player

    def _update_state(
            self, action, viewing_player, color_of_cell_that_changed):
        color = player_to_color(viewing_player)
        if color_of_cell_that_changed == color:
            self.win_detector.update(
                self.board,
                viewing_player,
                (self.board.row(action), self.board.column(action)),
                action
            )
            self._acting_player = next_player(viewing_player)

    def legal_actions(self):
        for a in self.board.legal_actions(self._acting_player):
            yield a

    def num_legal_actions(self):
        return self.board.num_legal_actions(self._acting_player)

    def to_s(self, player):
        """Print an ascii representation of the game board."""
        return self.board.to_s(player)

    def __str__(self):
        """Print an ascii representation of the game board."""
        return str(self.board)
