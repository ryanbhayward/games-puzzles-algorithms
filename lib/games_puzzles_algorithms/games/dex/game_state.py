from games_puzzles_algorithms.union_find import UnionFind
from games_puzzles_algorithms.games.hex.win_detector import WinDetector
from games_puzzles_algorithms.games.hex.game_state \
    import GameState as HexGameState
from games_puzzles_algorithms.games.hex.game_state import Board as HexBoard
from games_puzzles_algorithms.multi_dimensional_array \
    import MultiDimensionalArray
from array import array
from games_puzzles_algorithms.debug import log
from games_puzzles_algorithms.games.hex.color import IllegalAction, COLORS, \
    ORIENTATION, COLOR_SYMBOLS, NUM_PLAYERS, color_to_player, next_player, \
    player_to_color, cell_str, cell_str_to_cell


class Board(HexBoard):
    _NUM_FLIP_FLOPS_PER_CELL = 2
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
        self._empty_cells = []
        self._my_cells = []
        for player in range(NUM_PLAYERS):
            self._empty_cells.append({})
            self._my_cells.append({})
            for a in range(num_rows * num_columns):
                self._empty_cells[player][a] = True

        # List of cells revealed to each player in the order
        # they were revealed
        self.revealed_cells = MultiDimensionalArray(
            (num_rows * num_columns, NUM_PLAYERS),
            initial_elem=self._SENTINAL_VALUE_FOR_REVEALED_CELLS,
            elem_type='i'
        )
        self.num_revealed_cells = array('I', [0]*NUM_PLAYERS)

    def raw(self):
        return (self.cells.raw(), self.revealed_cells.raw())

    def size(self):
        return (self.cells.indexer.dimensions[1],
                self.cells.indexer.dimensions[2])

    def is_color(self, player, row, column, color):
        ci = self.cell_index(row, column)
        if ci in self._empty_cells[player]:
            return color == COLORS['none']
        else:
            return bool(
                self.cells[color_to_player(color), row, column, player]
            )

    def color(self, player, row, column):
        ci = self.cell_index(row, column)
        if ci in self._empty_cells[player]:
            return COLORS['none']
        else:
            return int(not self.cells[0, row, column, player])

    def play(self, ci, player):
        ''' Returns the color of the cell after attempting to set it to the player's color '''
        color = player_to_color(player)

        opponent = next_player(player)
        num_revealed = self.num_revealed_cells[player]

        row, column = self.row(ci), self.column(ci)

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
            self._my_cells[player][ci] = True

        del self._empty_cells[player][ci]
        return color

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
        self._empty_cells[player][cell_index] = True
        if player == player_with_removed_stone:
            del self._my_cells[player][cell_index]

        return cell

    def to_s(self, player):
        """Print an ascii representation of the game board."""
        def color(row, column):
            return self.color(player, row, column)
        return self._to_s(color)

    def __str__(self):
        """Print an ascii representation of the game board."""
        def color(row, column):
            c1 = self.color(color_to_player(COLORS['white']), row, column)
            if c1 != COLORS['none']:
                return c1
            else:
                return self.color(color_to_player(COLORS['black']), row, column)

        return self._to_s(color)


class GameState(HexGameState):
    """Represents the current state of a game of dark hex (dex)."""
    # move value of -1 indicates the game has ended so no move is possible
    GAMEOVER = -1

    @classmethod
    def clean_board(self, *dimensions):
        return Board(*dimensions)

    def previous_action_was_a_collision(self, previous_player=None):
        if previous_player is None:
            previous_player = self._previous_acting_players[-1]
        return previous_player == self._acting_player

    def every_cell(self):
        for row, column in self.board.every_cell():
            yield row, column

    def every_empty_cell(self):
        for row, column in self.board.every_empty_cell(self._acting_player):
            yield row, column

    def every_legal_undominated_action(self):
        winning_moves = list(self.potentially_winning_moves())
        if winning_moves:
            for a in winning_moves:
                yield a
        else:
            for a in self.board.legal_actions(self._acting_player):
                yield a

    def num_undominated__empty_cells(self):
        winning_moves = list(self.potentially_winning_moves())
        return (
            len(winning_moves) if winning_moves else
            self.board.num_legal_actions(self._acting_player)
        )
