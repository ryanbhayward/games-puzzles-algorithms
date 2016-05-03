from games_puzzles_algorithms.union_find import UnionFind
from .color import COLORS, NUM_PLAYERS, player_to_color


class WinDetector(object):
    """docstring for WinDetector"""

    # represent edges in the union find strucure for win detection
    _EDGES = [-1, -2]

    @classmethod
    def root(self, num_players=NUM_PLAYERS):
        return self(*[UnionFind() for _ in range(num_players)])

    def __init__(self, *groups):
        super(WinDetector, self).__init__()
        num_players = len(groups)
        self.history_of_player_groups = []
        self.current_groups = []
        self._winner = COLORS['none']
        for player in range(num_players):
            self.history_of_player_groups.append([])
            self.current_groups.append(groups[player])
            if self.check_if_winner(player):
                self._winner = player_to_color(player)

    def winner(self):
        return self._winner

    def is_terminal(self):
        return self.winner() != COLORS['none']

    def undo(self, acting_player):
        self.current_groups[acting_player].set_from_raw(
            self.history_of_player_groups[
                acting_player
            ].pop()
        )
        self._winner = COLORS['none']

    def update(self, board, acting_player, cell, cell_index):
        self.history_of_player_groups[acting_player].append(
            self.current_groups[acting_player].copy_raw()
        )
        self.imagined_update(board, acting_player, cell, cell_index)

    def connect_with_edge(self, acting_player, edge_index, cell_index):
        self.current_groups[acting_player].join(self._EDGES[edge_index], cell_index)

    def connect_with_edges_if_necessary(self, board, acting_player, cell, cell_index):
        if cell[acting_player] == 0:
            self.connect_with_edge(acting_player, 0, cell_index)
        elif cell[acting_player] == board.size()[acting_player] - 1:
            self.connect_with_edge(acting_player, 1, cell_index)

    def imagined_update(self, board, acting_player, cell, cell_index):
        self.connect_with_edges_if_necessary(board, acting_player, cell, cell_index)
        self.imagined_update_after_edges_checked(
            board,
            acting_player,
            cell,
            cell_index
        )
        if self.check_if_winner(acting_player):
            self._winner = player_to_color(acting_player)

    def imagined_update_after_edges_checked(
        self,
        board,
        acting_player,
        cell,
        cell_index
    ):
        color = player_to_color(acting_player)
        for row, column in board.every_neighbor(*cell):
            if board.is_color(acting_player, row, column, color):
                self.current_groups[acting_player].join(
                    board.cell_index(row, column),
                    cell_index
                )

    def check_if_winner(self, player):
        """Return the winning color or none if the game
           is not over.
        """
        return self.current_groups[player].connected(*self._EDGES)

    def is_connected_to_edge(self, player, edge_index, cell_index):
        return self.current_groups[player].connected(cell_index, self._EDGES[edge_index])
