from games_puzzles_algorithms.union_find import UnionFind
from games_puzzles_algorithms.game.hex.win_detector import WinDetector
from .multi_dimensional_array import MultiDimensionalArray
from array import array
from games_puzzles_algorithms.debug import log
from games_puzzles_algorithms.game.hex.color import IllegalAction, COLORS, \
    ORIENTATION, COLOR_SYMBOLS, NUM_PLAYERS, color_to_player, next_player, \
    player_to_color, cell_str, cell_str_to_cell


class Board(object):
    """ """

    _NUM_FLIP_FLOPS_PER_CELL = 2
    _NEIGHBOR_PATTERNS = (
        (-1, 0), # North
        (0, -1), # West
        (-1, 1), # Northeast
        (0, 1),  # East
        (1, 0),  # South
        (1, -1)  # Southwest
    )
    _SENTINAL_VALUE_FOR_REVEALED_CELLS = -1

    def __init__(self, num_rows, num_columns):
        # Shows stones on the board from each player's perspective
        self.cells = MultiDimensionalArray(
            (
                self._NUM_FLIP_FLOPS_PER_CELL,
                num_rows,
                num_columns,
                NUM_PLAYERS
            ),
            initial_elem=0,
            elem_type='B'
        )
        self.empty_cells = []
        self.my_cells = []
        for player in range(NUM_PLAYERS):
            self.empty_cells.append({})
            self.my_cells.append({})
            for a in range(num_rows * num_columns):
                self.empty_cells[player][a] = True

        # List of cells revealed to each player in the order
        # they were revealed
        self.revealed_cells = MultiDimensionalArray(
            (num_rows * num_columns, NUM_PLAYERS),
            initial_elem=self._SENTINAL_VALUE_FOR_REVEALED_CELLS,
            elem_type='i'
        )
        self.num_revealed_cells = array('I', [0]*NUM_PLAYERS)

    def is_empty(self, player, row, column):
        return self.cell_at_index_is_empty(player, self.cell_index(row, column))

    def cell_at_index_is_empty(self, player, ci):
        return ci in self.empty_cells[player]

    def raw(self):
        return (self.cells, self.revealed_cells)

    def num_legal_actions(self, player):
        return len(self.empty_cells[player])

    def num_rows(self): return self.cells.indexer.dimensions[1]

    def num_columns(self): return self.cells.indexer.dimensions[2]

    def size(self): return (self.num_rows(), self.num_columns())

    def is_color(self, player, row, column, color):
        ci = self.cell_index(row, column)
        if ci in self.empty_cells[player]:
            return color == COLORS['none']
        else:
            return bool(
                self.cells[color_to_player(color), row, column, player]
            )

    def color(self, player, row, column):
        ci = self.cell_index(row, column)
        if ci in self.empty_cells[player]:
            return COLORS['none']
        else:
            return int(not self.cells[0, row, column, player])

    def place(self, player, row, column):
        ''' Returns the color of the cell after attempting to set it to the player's color '''
        color = player_to_color(player)

        opponent = next_player(player)
        num_revealed = self.num_revealed_cells[player]

        ci = self.cell_index(row, column)

        if self.cells[opponent, row, column, opponent]: # Collision
            if self.cells[opponent, row, column, player]: # Already revealed
                raise IllegalAction(
                    "Attempted to place for {} but collided with {} stone already on cell {}".format(
                        color, player_to_color(opponent), (row, column)
                    )
                )
            else: # Newly revealed
                self.cells[opponent, row, column, player] = 1
                self.revealed_cells[num_revealed, player] = ci
                self.num_revealed_cells[player] = num_revealed + 1
                color = player_to_color(opponent)

        # Already the player's color
        elif self.cells[player, row, column, player]:
            raise IllegalAction(
                    "Attempted to place for {} but collided with {} stone already on cell {}".format(
                        color, color, (row, column)
                    )
                )
        else: # Set to player's color
            self.cells[player, row, column, player] = 1
            self.revealed_cells[num_revealed, player] = ci
            self.num_revealed_cells[player] = num_revealed + 1
            self.my_cells[player][ci] = True

        del self.empty_cells[player][ci]
        return color

    def with_stone_on_cell(self, player, row, column):
        '''Not meant to be used recursively.
           This is a faster version of #play that does less bookkeeping.
           Useful when one wants to examine the board after playing but
           does not need to do this recursively or check if a winner was
           decided.
        '''
        color = self.place(player, row, column)
        yield color
        self.undo(player)

    def __len__(self): return self.num_rows() * self.num_columns()

    def undo(self, player):
        num_revealed = self.num_revealed_cells[player] - 1
        self.num_revealed_cells[player] = num_revealed
        cell_index = self.revealed_cells[num_revealed, player]
        self.revealed_cells[num_revealed, player] = -1
        cell = (self.row(cell_index), self.column(cell_index))
        color_of_stone_to_remove = self.color(
            player,
            cell[0],
            cell[1]
        )
        player_with_removed_stone = color_to_player(color_of_stone_to_remove)
        self.cells[
            player_with_removed_stone,
            cell[0],
            cell[1],
            player
        ] = 0
        self.empty_cells[player][cell_index] = True
        if player == player_with_removed_stone:
            del self.my_cells[player][cell_index]

        return cell

    def cell_index(self, row, column):
        return (column * self.num_rows()) + row

    def row(self, cell_index):
        return cell_index % self.num_rows()

    def column(self, cell_index):
        return cell_index // self.num_rows()

    def every_cell(self):
        for column in range(self.num_columns()):
            for row in range(self.num_rows()):
                yield row, column

    def every_empty_cell(self, player):
        for a in self.empty_cells[player].keys():
            yield self.row(a), self.column(a)

    def every_empty_cell_with_index(self, player):
        for a in self.empty_cells[player].keys():
            yield (self.row(a), self.column(a)), a

    def legal_actions(self, player):
        for a in self.empty_cells[player].keys():
            yield a

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

    def every_legal_neighbor(self, player, row, column):
        """Yields each neighbor of the given cell on the given board one by one."""
        for neighbor_row_offset, neighbor_column_offset in self._NEIGHBOR_PATTERNS:
            neighbor_row = row + neighbor_row_offset
            neighbor_column = column + neighbor_column_offset
            if (
                self.is_valid_cell(neighbor_row, neighbor_column) and
                self.cell_index(neighbor_row, neighbor_column) in self.empty_cells[player]
            ):
                yield (neighbor_row, neighbor_column)

    def is_on_goal_edge(self, player, *cell):
        length = self.size()[player]
        opponent = next_player(player)
        adjacent_length = self.size()[opponent]
        return cell[player] == 0 or cell[player] == adjacent_length - 1

    def every_goal_edge_action(self, player):
        length = self.size()[player]
        opponent = next_player(player)
        adjacent_length = self.size()[opponent]
        cell = [0]*2
        for side in [0, adjacent_length - 1]:
            cell[player] = side
            for i in range(length):
                cell[opponent] = i
                yield self.cell_index(*cell)

    def every_legal_goal_edge_action(self, player):
        length = self.size()[player]
        opponent = next_player(player)
        adjacent_length = self.size()[opponent]
        cell = [0]*2
        for side in [0, adjacent_length - 1]:
            cell[player] = side
            for i in range(length):
                cell[opponent] = i
                ci = self.cell_index(*cell)
                if ci in self.empty_cells:
                    yield ci

    def every_goal_edge_cell(self, player):
        length = self.size()[player]
        opponent = next_player(player)
        adjacent_length = self.size()[opponent]
        cell = [0]*2
        for side in [0, adjacent_length - 1]:
            cell[player] = side
            for i in range(length):
                cell[opponent] = i
                yield cell

    def every_legal_goal_edge_cell(self, player):
        ''' Also yields action (cell index)'''
        length = self.size()[player]
        opponent = next_player(player)
        adjacent_length = self.size()[opponent]
        cell = [0]*2
        for side in [0, adjacent_length - 1]:
            cell[player] = side
            for i in range(length):
                cell[opponent] = i
                ci = self.cell_index(*cell)
                if ci in self.empty_cells[player]:
                    yield cell, ci

    def every_legal_first_goal_edge_cell(self, player):
        ''' Also yields action (cell index)'''
        length = self.size()[player]
        opponent = next_player(player)
        adjacent_length = self.size()[opponent]
        cell = [0]*2
        for i in range(length):
            cell[opponent] = i
            ci = self.cell_index(*cell)
            if ci in self.empty_cells[player]:
                yield cell, ci

    def every_legal_second_goal_edge_cell(self, player):
        ''' Also yields action (cell index)'''
        length = self.size()[player]
        opponent = next_player(player)
        adjacent_length = self.size()[opponent]
        cell = [adjacent_length - 1]*2
        for i in range(length):
            cell[opponent] = i
            ci = self.cell_index(*cell)
            if ci in self.empty_cells[player]:
                yield cell, ci

    def to_s(self, player):
        """Print an ascii representation of the game board."""
        def color(row, column):
            return self.color(player, row, column)
        return self._to_s(color)

    def _to_s(self, get_color_fn):
        """Print an ascii representation of the game board."""
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
        """Print an ascii representation of the game board."""
        def color(row, column):
            c1 = self.color(color_to_player(COLORS['white']), row, column)
            if c1 != COLORS['none']:
                return c1
            else:
                return self.color(color_to_player(COLORS['black']), row, column)

        return self._to_s(color)


class GameState(object):
    """Stores information representing the current state of a game of hex,
    namely the board and the current turn.

    Also provides functions for playing the game and returning
    information about it.

    """
    # move value of -1 indicates the game has ended so no move is possible
    GAMEOVER = -1

    @classmethod
    def root(self, *dimensions):
        """Initialize the game board and give white first turn.

        Also create our union find structures for win checking.

        """
        if len(dimensions) < 1:
            num_rows = 6
        else:
            num_rows = dimensions[0]
        num_columns = num_rows if len(dimensions) < 2 else dimensions[1]
        return self(
            color_to_player(COLORS["white"]),
            Board(num_rows, num_columns),
            UnionFind(),
            UnionFind()
        )

    def __init__(self, actor, board, *groups):
        self.actor = actor
        self.previous_actors = []
        self.board = board
        self.win_detector = WinDetector(*groups)
        self._potentially_winning_moves = None

    def __getitem__(self, cell):
        return self.board.color(self.turn(), *cell)

    def is_empty(self, cell):
        return self.board.is_empty(self.turn(), *cell)

    def num_actions_taken(self, player):
        return len(self.win_detector.history_of_player_groups[player])

    def potentially_winning_moves(self):
        if self._potentially_winning_moves is None:
            self._potentially_winning_moves = {}
            if self.num_actions_taken(self.actor) >= (self.board.size()[self.actor] - 1):
                original_group = self.win_detector.current_groups[self.actor].copy_raw()
                color = player_to_color(self.actor)
                for my_cell_index in self.board.my_cells[self.actor].keys():
                    for cell in self.board.every_legal_neighbor(
                        self.actor,
                        self.board.row(my_cell_index),
                        self.board.column(my_cell_index)
                    ):
                        a = self.board.cell_index(*cell)
                        if a not in self._potentially_winning_moves:
                            self.win_detector.imagined_update(
                                self.board,
                                self.actor,
                                cell,
                                a
                            )
                            if self.win_detector.check_if_winner(self.actor):
                                self._potentially_winning_moves[a] = True
                            self.win_detector.current_groups[self.actor].copy_from_raw(original_group)
                self.win_detector._winner = COLORS['none']
        return list(self._potentially_winning_moves.keys())

    def with_stone_at_index(self, cell):
        '''Not meant to be used recursively.
           This is a faster version of #play that does less bookkeeping.
           Useful when one wants to examine the board after playing but
           does not need to do this recursively or check if a winner was
           decided.
        '''
        for _ in self.board.with_stone_on_cell(
            self.actor,
            self.board.row(cell),
            self.board.column(cell)
        ):
            yield

    def with_stone_at_cell(self, cell):
        '''Not meant to be used recursively.
           This is a faster version of #play that does less bookkeeping.
           Useful when one wants to examine the board after playing but
           does not need to do this recursively or check if a winner was
           decided.
        '''
        for _ in self.board.with_stone_on_cell(
            self.actor,
            *cell
        ):
            yield

    def previous_action_was_a_collision(self, previous_player=None):
        if previous_player is None:
            previous_player = self.previous_actors[-1]
        return previous_player == self.actor

    def undo(self):
        ''' Undoes the last action played '''
        cell = None
        if self.previous_actors:
            previous_player = self.previous_actors.pop()
            if previous_player != self.actor:
                self.win_detector.undo(previous_player)
                self.actor = previous_player
            cell = self.board.undo(previous_player)
            self._potentially_winning_moves = None
        return cell

    def play(self, cell):
        """Play a stone of the current turns color in the passed cell."""
        self.place(cell, player_to_color(self.actor))

    def play_at_index(self, cell):
        self.play((self.board.row(cell), self.board.column(cell)))

    def do_after_play_at_index(self, cell):
        self.play_at_index(cell)
        yield
        self.undo()

    def do_after_play(self, cell):
        self.play(cell)
        yield
        self.undo()

    def place(self, cell, player):
        """Place a stone for the given player regardless of whose turn it is."""
        if self.is_terminal():
            raise IllegalAction("Game has finished and {} is the winner".format(self.winner()))
        color_after_placing = self.board.place(player, *cell)
        self.previous_actors.append(player)
        self._update_state(player, cell, color_after_placing)
        self._potentially_winning_moves = None

    def winner(self):
        return self.win_detector.winner()

    def is_terminal(self):
        return self.win_detector.is_terminal()

    def turn(self):
        """Return the player with the next move."""
        return self.actor

    def set_turn(self, player):
        """Set the player to take the next move."""
        self.actor = player

    def _update_state(self, viewing_player, cell, color_of_cell_that_changed):
        color = player_to_color(viewing_player)
        if color_of_cell_that_changed == color:
            self.win_detector.update(
                self.board,
                viewing_player,
                cell,
                self.board.cell_index(*cell)
            )
            self.actor = next_player(viewing_player)

    def moves(self):
        """Get a list of all moves possible on the current board."""
        return list(self.board.empty_cells.keys())

    def every_cell(self):
        for row, column in self.board.every_cell():
            yield row, column

    def every_empty_cell(self):
        for row, column in self.board.every_empty_cell(self.actor):
            yield row, column

    def legal_actions(self):
        for a in self.board.legal_actions(self.actor):
            yield a

    def every_legal_undominated_action(self):
        winning_moves = self.potentially_winning_moves()
        if winning_moves:
            for a in winning_moves:
                yield a
        else:
            for a in self.board.legal_actions(self.actor):
                yield a

    def num_legal_actions(self):
        return self.board.num_legal_actions(self.actor)

    def num_undominated_empty_cells(self):
        winning_moves = self.potentially_winning_moves()
        return (
            len(winning_moves) if winning_moves else
            self.board.num_legal_actions(self.actor)
        )

    def to_s(self, player):
        """Print an ascii representation of the game board."""
        return self.board.to_s(player)

    def __str__(self):
        """Print an ascii representation of the game board."""
        return str(self.board)
