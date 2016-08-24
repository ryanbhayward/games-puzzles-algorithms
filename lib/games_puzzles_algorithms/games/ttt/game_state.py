from array import array
from enum import IntEnum
from string import ascii_uppercase as alphabet


class BoardValues(IntEnum):
    X = 0
    O = 1
    Empty = 3

    def __str__(self):
        if self is BoardValues.Empty:
            return ' '
        return self.name

    def opponent(self):
        if self is BoardValues.Empty:
            raise ValueError("Empty piece has no opponent")
        return BoardValues.X if self is BoardValues.O else BoardValues.O


class UndoException(Exception):
    pass


class TwoDimensionalTable(object):

    def __init__(
        self,
        num_rows,
        num_columns,
        initial_elem=0,
        elem_type='b'
    ):
        self._dimensions = (num_rows, num_columns)
        self._data = array(
            elem_type,
            [initial_elem] * num_rows * num_columns)

    def size(self, index=None):
        if index is None:
            return self._dimensions
        return self._dimensions[index]

    def num_rows(self): return self.size(0)

    def num_columns(self): return self.size(1)

    def index(self, row, column):
        return (column * self.num_rows()) + row

    def row(self, index): return index % self.num_rows()

    def column(self, index): return index // self.num_rows()

    def get_index(self, index):
        return self._data[index]

    def set_index(self, index, val):
        self._data[index] = val

    def __getitem__(self, indices):
        return self._data[self.index(*indices)]

    def __setitem__(self, indices, c):
        self._data[self.index(*indices)] = c

    def __len__(self):
        return self.num_rows() * self.num_columns()

    def __iter__(self):
        return (i for i in self._data)


class WinDetector(object):
    """
    The WinDetector is used to track the win state of a game of tic-tac-toe.
    This is done by tracking run-lengths on the board for each direction. We
    perform this count from left to right and top to bottom along the board.
    The value in any given cell if the length of the run ending in that cell.
    """
    def __init__(self, rows, columns, spaces_to_win):
        self.rows = rows
        self.columns = columns
        self.spaces_to_win = spaces_to_win
        self._rows = TwoDimensionalTable(rows, columns)
        self._columns = TwoDimensionalTable(rows, columns)
        self._diagonals = TwoDimensionalTable(rows, columns)
        self._anti_diagonals = TwoDimensionalTable(rows, columns)

    def _iter_row(self, row, column):
        """Iterate along a row starting at the given coordinate."""
        for c in range(column, self.columns):
            yield (row, c)

    def _iter_column(self, row, column):
        """Iterate along a column starting at the given coordinate."""
        for r in range(row, self.rows):
            yield (r, column)

    def _iter_diagonal(self, row, column):
        """Iterate along a diagonal starting at the given coordinate."""
        row_difference = self.rows - row
        column_difference = self.columns - column

        for i in range(min(row_difference, column_difference)):
            yield(row + i, column + i)

    def _iter_anti_diagonal(self, row, column):
        """Iterate along an anti-diagonal starting at the given coordinate."""
        row_difference = self.rows - row
        for i in range(min(row_difference, column)):
            yield(row - i, column - i)

    def _cascade_state_update(self, state, row, column, iterator):
        """
        Starting from the given coordinate, increment the run-length along the
        direction defined by the iterator until we hit a blank spot on the
        board.
        """
        run_length = state[row, column]

        for r, c in iterator(row, column):
            # A zero run-length indicates no piece in this cell.
            if state[r, c] == 0:
                break

            state[r, c] = run_length
            run_length += 1

    def _row_length(self, row, column):
        """
        Calculate the existing run-length in this row ending at the given
        coordinate.
        """
        return 0 if column == 0 else self._rows[row, column - 1]

    def _column_length(self, row, column):
        """
        Calculate the existing run-length in this column ending at the given
        coordinate.
        """
        return 0 if row == 0 else self._columns[row - 1, column]

    def _diagonal_length(self, row, column):
        """
        Calculate the existing run-length in this diagonal ending at the given
        coordinate.
        """
        if row == 0 or column == 0:
            return 0
        else:
            return self._diagonals[row - 1, column - 1]

    def _anti_diagonal_length(self, row, column):
        """
        Calculate the existing run-length in this anti-diagonal ending at the
        given coordinate.
        """
        if row == 0 or column == self.columns - 1:
            return 0
        else:
            return self._anti_diagonals[row - 1, column + 1]

    def _update_triples(self):
        """
        A generator over the triples needed to update the WinDetector's
        states.
        """
        yield (self._rows, self._row_length, self._iter_row)
        yield (self._columns, self._column_length, self._iter_column)
        yield (self._diagonals, self._diagonal_length, self._iter_diagonal)
        yield (self._anti_diagonals, self._anti_diagonal_length,
               self._iter_anti_diagonal)

    def update(self, move, is_undo=False):
        """
        Update the WinDetector states to account for the given move. If the move
        was an undo, we set the run-length of the given cell to zero. Otherwise,
        we extend the existing run ending at this cell. Afterwards, we propagate
        the updated run to the cells below.
        """
        # All states are equally valid to query for the move coordinates.
        row = self._rows.row(move)
        column = self._rows.column(move)

        for (state, run_length, iterator) in self._update_triples():
            state[row, column] = 0 if is_undo else run_length(row, column) + 1
            self._cascade_state_update(state, row, column, iterator)

    def _states(self):
        """A generator of the WinDetector states."""
        yield self._rows
        yield self._columns
        yield self._diagonals
        yield self._anti_diagonals

    def win_detected(self):
        """Return whether any runs exist that meet the winning length."""
        for state in self._states():
            if any(run_length >= self.spaces_to_win for run_length in state):
                return True
        return False


class Board(object):

    def __init__(self, num_rows=3, num_columns=None, num_spaces_to_win=None):
        if num_columns is None:
            num_columns = num_rows
        if num_spaces_to_win is None:
            num_spaces_to_win = min(num_rows, num_columns)
        self._num_spaces_to_win = num_spaces_to_win
        self._spaces = TwoDimensionalTable(
            num_rows,
            num_columns,
            initial_elem=BoardValues.Empty,
            elem_type='b')

        self._actions = []
        self._win_detectors = {
            BoardValues.X: WinDetector(num_rows, num_columns,
                                       num_spaces_to_win),
            BoardValues.O: WinDetector(num_rows, num_columns, num_spaces_to_win)
        }

    def __str__(self):
        rows = self._spaces.num_rows()
        columns = self._spaces.num_columns()

        row_offset = ' ' * (len(str(rows)) + 1)
        row_edge = "\n{}{}\n".format(row_offset, "|".join(['-'] * columns))

        column_header = '\n{}{}\n'.format(row_offset,
                                          ' '.join(alphabet[:columns]))

        def row_repr(i):
            row_header = str(i + 1).ljust(len(row_offset))
            row = "|".join(str(BoardValues(self._spaces[i, j])) for j
                           in range(columns))
            return row_header + row

        board = row_edge.join(row_repr(i) for i in range(rows))
        return column_header + board + '\n'

    def cell_index(self, row, column):
        return self._spaces.index(row, column)

    def row(self, index): return self._spaces.row(index)

    def column(self, index): return self._spaces.column(index)

    def num_rows(self): return self._spaces.num_rows()

    def num_columns(self): return self._spaces.num_columns()

    def num_actions_played(self): return len(self._actions)

    def empty_spaces(self):
        return [i for (i, p) in enumerate(self._spaces)
                if p == BoardValues.Empty]

    def num_empty_spaces(self):
        return len(self.empty_spaces())

    def last_action(self):
        if len(self._actions) > 0:
            return self._actions[-1]['action']

    def play(self, action, player):
        """ Execute an action on the board """
        if (not self._spaces.get_index(action) == BoardValues.Empty):
            raise IndexError("Cannot play in the same space as another "
                             "player!")
        self._spaces.set_index(action, player)
        self._actions.append({'player': player, 'action': action})
        self._win_detectors[player].update(action)

    def undo(self):
        if len(self._actions) == 0:
            raise UndoException("Board is empty. Nothing to undo!")

        last_action = self._actions.pop()
        self._spaces.set_index(last_action['action'], BoardValues.Empty)
        self._win_detectors[last_action['player']].update(last_action['action'],
                                                          is_undo=True)
        return last_action['player']

    def _has_win(self, player):
        return self._win_detectors[player].win_detected()

    def num_spaces_to_win(self): return self._num_spaces_to_win

    def winner(self):
        """
        Returns: None if the game is unfinished
                 BoardValues.X if the x player has won
                 BoardValues.O if the o player has won
                 BoardValues.Empty if the game is a draw
        """
        if self._has_win(BoardValues.X):
            return BoardValues.X
        elif self._has_win(BoardValues.O):
            return BoardValues.O
        elif self.num_empty_spaces() == 0:
            return BoardValues.Empty
        else:
            return None

    def heuristic(self, player):
        """
        Return a heuristic value of the game state for player.

        Values are between -1 and 1, and values closer to 1 are better for
        player.
        """
        value = 0.0
        player = BoardValues(player)
        for row in range(self._spaces.num_rows()):
            if self._status[player.opponent()]['row' + str(row)] == 0:
                value += self._status[player]['row' + str(row)]
            if self._status[player]['row' + str(row)] == 0:
                value -= self._status[player.opponent()]['row' + str(row)]

        for column in range(self._spaces.num_columns()):
            str_col = 'column' + str(column)
            if self._status[player.opponent()][str_col] == 0:
                value += self._status[player][str_col]
            if self._status[player][str_col] == 0:
                value -= self._status[player.opponent()][str_col]

        if self._status[player.opponent()]['positive_diagonal'] == 0:
            value += self._status[player]['positive_diagonal']
        if self._status[player.opponent()]['negative_diagonal'] == 0:
            value += self._status[player]['negative_diagonal']
        if  self._status[player]['positive_diagonal'] == 0:
            value -= self._status[player.opponent()]['positive_diagonal']
        if self._status[player]['negative_diagonal'] == 0:
            value -= self._status[player.opponent()]['negative_diagonal']
        cols = self._spaces.num_columns()
        rows = self._spaces.num_rows()
        scale = cols * rows * 2 + max(cols, rows) * 2
        return value / scale


class GameState(Board):

    def __init__(self, num_rows=3, num_columns=None, num_spaces_to_win=None):
        if num_columns is None:
            num_columns = num_rows
        if num_spaces_to_win is None:
            num_spaces_to_win = min(num_rows, num_columns)
        super(GameState, self).__init__(num_rows,
                                        num_columns,
                                        num_spaces_to_win)
        self._next_to_act = BoardValues.X

    def __enter__(self):
        """Allows the following type of code:

        ```
        with state.play(action):
            # Do something with `state` after `action`
            # has been applied to `state`.
        # `action` has automatically be undone.
        """
        pass

    def __exit__(self,
                 exception_type,
                 exception_val,
                 exception_traceback):
        """Allows the following type of code:

        ```
        with state.play(action):
            # Do something with `state` after `action`
            # has been applied to `state`.
        # `action` has automatically be undone.
        """
        self.undo()

    def cell_index(self, row, column):
        return super().cell_index(row, column)

    def row(self, index): return self._board.row(index)

    def column(self, index): return self._board.column(index)

    def legal_actions(self):
        return [] if self.is_terminal() else super().empty_spaces()

    def num_legal_actions(self):
        return 0 if self.is_terminal() else super().num_empty_spaces()

    def play(self, action):
        super().play(action, self._next_to_act)
        self._next_to_act = self._next_to_act.opponent()
        return self

    def undo(self):
        try:
            self._next_to_act = super().undo()
        except UndoException:
            pass  # An UndoException signifies there's no change to make.

    def set_player_to_act(self, p):
        self._next_to_act = BoardValues(p)

    def player_to_act(self):
        return self._next_to_act

    def player_who_acted_last(self):
        if self.num_actions_played() > 0:
            return self._next_to_act.opponent()

    def is_terminal(self):
        return self.winner() is not None

    def score(self, player):
        winner = self.winner()
        player = BoardValues(player)

        if player == winner:
            return 1
        elif player.opponent() == winner:
            return -1
        elif winner is None:
            return None
        else:
            return 0

    def reset(self):
        super().__init__(super().num_rows())
        self._next_to_act = BoardValues.X
        return self
