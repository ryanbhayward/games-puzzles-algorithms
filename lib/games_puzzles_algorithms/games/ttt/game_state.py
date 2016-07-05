from array import array
from enum import IntEnum
from string import ascii_uppercase as alphabet

class BoardValues(IntEnum):
    X = 0
    O = 1
    Empty = 3

    def __str__(self):
        if self is self.Empty:
            return ' '
        return self.name

    def opponent(self):
        if self is self.Empty:
            raise ValueError("Empty piece has no opponent")

        return BoardValues.X if self is BoardValues.O else BoardValues.O


class UndoException(Exception):
    pass


class GameState(object):
    class Board(object):
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
                return self._dimensions if index is None \
                    else self._dimensions[index]

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


        def __init__(self, size=3):
            self._size = size
            self._spaces = self.TwoDimensionalTable(
                size,
                size,
                initial_elem=BoardValues.Empty,
                elem_type='b')
            self._actions = []
            self.initialize_win_status()

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

        def num_actions_played(self): return len(self._actions)

        def legal_actions(self):
            return [i for (i, p) in enumerate(self._spaces)
                    if p == BoardValues.Empty]

        def num_legal_actions(self):
            return len(self.legal_actions())

        def play(self, action, player):
            ''' Execute an action on the board '''
            if (not self._spaces.get_index(action) == BoardValues.Empty):
                raise IndexError("Cannot play in the same space as another "
                                 "player!")
            self._spaces.set_index(action, player)
            self._actions.append({'player': player, 'action': action})
            self._update_win_status(action, player, increment=True)

        def undo(self):
            if len(self._actions) == 0:
                raise UndoException("Board is empty. Nothing to undo!")

            last_action = self._actions.pop()
            self._spaces.set_index(last_action['action'], BoardValues.Empty)
            self._update_win_status(last_action['action'],
                                    last_action['player'], increment=False)
            return last_action['player']

        def space_is_on_positive_diagonal(self, row, column):
            return row == column

        def space_is_on_negative_diagonal(self, row, column):
            return row == (self._spaces.num_columns() - (column + 1))

        def initialize_win_status(self):
            self._status = {}
            self._status[BoardValues.X] = {'positive_diagonal': 0,
                                           'negative_diagonal': 0 }

            for row in range(self._spaces.num_rows()):
                self._status[BoardValues.X]['row' + str(row)] = 0

            for column in range(self._spaces.num_columns()):
                self._status[BoardValues.X]['column' + str(column)] = 0

            self._status[BoardValues.O] = self._status[BoardValues.X].copy()

        def _update_win_status(self, action, player, increment=True):
            row = self._spaces.row(action)
            column = self._spaces.column(action)

            modifier = 1 if increment else -1

            self._status[player]['row' + str(row)] += modifier
            self._status[player]['column' + str(column)] += modifier

            if self.space_is_on_positive_diagonal(row, column):
                self._status[player]['positive_diagonal'] += modifier

            if self.space_is_on_negative_diagonal(row, column):
                self._status[player]['negative_diagonal'] += modifier

        def _has_win(self, player):
            player_status = self._status[player]
            return any(n == self._size for n in player_status.values())

        def winner(self):
            '''
            Returns: None if the game is unfinished
                     BoardValues.X if the x player has won
                     BoardValues.O if the o player has won
                     BoardValues.Empty if the game is a draw
            '''
            if self._has_win(BoardValues.X):
                return BoardValues.X
            elif self._has_win(BoardValues.O):
                return BoardValues.O
            elif self.num_legal_actions() == 0:
                return BoardValues.Empty
            else:
                return None


    def __init__(self, size=3):
        self._board = self.Board(size)
        self._next_to_act = BoardValues.X

    def __enter__(self):
        '''Allows the following type of code:

        ```
        with state.play(action):
            # Do something with `state` after `action`
            # has been applied to `state`.
        # `action` has automatically be undone.
        '''
        pass

    def __exit__(self,
                 exception_type,
                 exception_val,
                 exception_traceback):
        '''Allows the following type of code:

        ```
        with state.play(action):
            # Do something with `state` after `action`
            # has been applied to `state`.
        # `action` has automatically be undone.
        '''
        self.undo()

    def cell_index(self, row, column):
        return self._board.cell_index(row, column)

    def row(self, index): return self._board.row(index)
    def column(self, index): return self._board.column(index)

    def legal_actions(self):
        return [] if self.is_terminal() else self._board.legal_actions()

    def num_legal_actions(self):
        return self._board.num_legal_actions()

    def play(self, action):
        self._board.play(action, self._next_to_act)
        self._next_to_act = self._next_to_act.opponent()
        return self

    def undo(self):
        try:
            self._next_to_act = self._board.undo()
        except UndoException:
            pass # An UndoException signifies there's no change to make.

        return self

    def set_player_to_act(self, p):
        self._next_to_act = BoardValues(p)

    def player_to_act(self):
        return self._next_to_act

    def player_who_acted_last(self):
        if self._board.num_actions_played() > 0:
            return self._next_to_act.opponent()

        return None

    def is_terminal(self):
        return self._board.winner() is not None

    def score(self, player):
        winner = self._board.winner()
        player = BoardValues(player)

        if player == winner:
            return 1
        elif player.opponent() == winner:
            return -1
        elif winner is None:
            return None
        else:
            return 0

    def __str__(self): return str(self._board)
