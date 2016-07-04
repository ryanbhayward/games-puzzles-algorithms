from array import array
from enum import IntEnum


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
            def __getitem__(self, indices):
                return self._data[self.index(*indices)]
            def __setitem__(self, indices, c):
                self._data[self.index(*indices)] = c
            def __len__(self):
                return self.num_rows() * self.num_columns()

        class BoardValues(IntEnum):
            X = 0
            O = 1
            Empty = 3

            def __str__(self):
                if self is self.Empty:
                    return ' '
                return self.name

        def __init__(self, size=3):
            self._spaces = self.TwoDimensionalTable(
                size,
                size,
                initial_elem=self.BoardValues.Empty,
                elem_type='b')
            self._actions = []

        def __str__(self):
            ret = "\n"
            coord_size = len(str(self._spaces.num_rows()))
            offset = 1
            ret += ' ' * (offset + 1)
            for x in range(self._spaces.num_columns()):
                ret += chr(ord('A') + x) + ' ' * offset
            ret = ret.rstrip() + '\n'
            for i in range(self._spaces.num_rows()):
                if i != 0:
                    ret += ("  "
                            + "|".join(['-']*self._spaces.num_columns())
                            + "\n")
                ret += (str(i + 1) + ' '
                                   * (offset + coord_size - len(str(i + 1))))
                for j in range(self._spaces.num_columns()):
                    if j > 0: ret += '|'
                    ret += chr(self._spaces[i, j])
                ret += "\n"
            return ret

        def cell_index(self, row, column):
            return self._spaces.index(row, column)
        def row(self, index): return self._spaces.row(index)
        def column(self, index): return self._spaces.column(index)

        def num_actions_played(self): return len(self._actions)

        def legal_actions(self):
            return [i for i in range(len(self._spaces))
                    if self._spaces._data[i] == self.BoardValues.Empty]

        def num_legal_actions(self):
            return len(self.legal_actions())

        def play(self, action, player):
            ''' Execute an action on the board '''
            row = self._spaces.row(action)
            column = self._spaces.column(action)
            if (self._spaces[row, column] == self.BoardValues.X
                or self._spaces[row, column] == self.BoardValues.O):
                raise IndexError(
                    "Cannot play in the same space as another player!")
            self._spaces[row, column] = player
            self._actions.append({'player': player, 'action': action})

        def undo(self):
            if len(self._actions) > 0:
                last_action = self._actions.pop()
                row = self._spaces.row(last_action['action'])
                column = self._spaces.column(last_action['action'])
                self._spaces[row, column] = self.BoardValues.Empty
                return last_action['player']

        def space_is_on_positive_diagonal(self, row, column):
            return row == column

        def space_is_on_negative_diagonal(self, row, column):
            return row == (self._spaces.num_columns() - (column + 1))

        def winner(self):
            '''
            Returns: None if the game is unfinished
                     GameState.Board.BoardValues.X if the x player has won
                     GameState.Board.BoardValues.O if the o player has won
                     GameState.Board.BoardValues.Empty if the game is a draw
            '''
            statuses = {
                'positive_diagonal': {'has_win': True, 'char': None},
                'negative_diagonal': {'has_win': True, 'char': None}
            }
            for row in range(self._spaces.num_rows()):
                statuses['row' + str(row)] = {'has_win': True, 'char': None}
            for column in range(self._spaces.num_columns()):
                statuses['column' + str(column)] = {
                    'has_win': True,
                    'char': None
                }
            for row in range(self._spaces.num_rows()):
                for column in range(self._spaces.num_columns()):
                    relevant_statuses = [
                        statuses['row' + str(row)],
                        statuses['column' + str(column)]]
                    if self.space_is_on_positive_diagonal(row, column):
                        relevant_statuses.append(statuses['positive_diagonal'])
                    if self.space_is_on_negative_diagonal(row, column):
                        relevant_statuses.append(statuses['negative_diagonal'])
                    space = self._spaces[row, column]
                    for s in relevant_statuses:
                        if s['has_win']:
                            if space == self.BoardValues.Empty:
                                s['has_win'] = False
                            elif s['char'] is None:
                                s['char'] = space
                            elif s['char'] != space:
                                s['has_win'] = False
            for label, status in statuses.items():
                if status['has_win']: return status['char']
            if self.num_legal_actions() < 1: return self.BoardValues.Empty
            else: return None

    def __init__(self, size=3):
        self._board = self.Board(size)
        self._next_to_act = 0

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
        self._next_to_act = int(not(self._next_to_act))
        return self

    def undo(self):
        self._next_to_act = self._board.undo()
        return self

    def set_player_to_act(self, p):
        self._next_to_act = p

    def player_to_act(self):
        return self._next_to_act

    def player_who_acted_last(self):
        return int(not(self._next_to_act)) \
            if self._board.num_actions_played() > 0 else None

    def is_terminal(self):
        return self._board.winner() is not None

    def score(self, player):
        winner = self._board.winner()
        if player == winner:
            return 1
        elif int(not(player)) == winner:
            return -1
        elif winner is None:
            return None
        else:
            return 0

    def __str__(self): return str(self._board)
