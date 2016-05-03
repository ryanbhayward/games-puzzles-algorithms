from games_puzzles_algorithms.game.dex.game_state import COLORS
from games_puzzles_algorithms.game.dex.game_state import player_to_color
from games_puzzles_algorithms.game.dex.game_state import color_to_player
from games_puzzles_algorithms.game.hex.game_state import GameState as HexGameState
from games_puzzles_algorithms.game.dex.game_state import IllegalAction
from games_puzzles_algorithms.choose import choose_from_distribution
from games_puzzles_algorithms.choose import choose_legal_action_uniformly_randomly
from games_puzzles_algorithms.player.mcts.mcts_agent import MctsAgent
import math


class CombinedPlayerRuleBasedAgent(object):
    """docstring for CombinedPlayerRuleBasedAgent"""
    def __init__(self, random_generator, only_corners=True, only_search=False):
        super(CombinedPlayerRuleBasedAgent, self).__init__()
        self.players = [
            RuleBasedAgent(random_generator, only_corners=only_corners, only_search=only_search),
            RuleBasedAgent(random_generator, only_corners=only_corners, only_search=only_search)
        ]

    def act(self, state, time_allowed_s=None):
        return self.players[state.turn()].act(
            state,
            time_allowed_s=time_allowed_s
        )

    def distribution(self, state, weight=1.0, time_allowed_s=None):
        return self.players[state.turn()].distribution(
            state,
            weight=weight,
            time_allowed_s=time_allowed_s
        )

    def reset(self):
        for p in self.players:
            p.reset()


class RuleBasedAgent(object):
    """docstring for RuleBasedAgent"""

    @staticmethod
    def empty_board_distribution(state, weight=1.0, only_corners=True):
        row = state.board.num_rows() - 1
        d = {}
        s = 0.0
        if only_corners:
            if state.board.color(state.turn(), row, 0) == COLORS['none']:
                action = state.board.cell_index(row, 0)
                d[action] = 1.0
                s += 1
            column = state.board.num_columns() - 1
            if state.board.color(state.turn(), 0, column) == COLORS['none']:
                action = state.board.cell_index(0, column)
                d[action] = 1.0
                s += 1
        else:
            middle_column = state.board.num_columns() // 2
            odd_sized_board = middle_column * 2 != state.board.num_columns()
            for column in range(middle_column):
                if state.board.color(state.turn(), row, column) == COLORS['none']:
                    action = state.board.cell_index(row, column)
                    d[action] = 1.0
                    s += 1
                row -= 1
            row = 0
            for column in range(
                state.board.num_columns() - 1,
                state.board.num_columns() - middle_column - 1,
                -1
            ):
                if state.board.color(state.turn(), row, column) == COLORS['none']:
                    action = state.board.cell_index(row, column)
                    d[action] = 1.0
                    s += 1
                row += 1
            if odd_sized_board:
                middle_row = middle_column
                if (
                    state.board.color(state.turn(), middle_row, middle_column) ==
                    COLORS['none']
                ):
                    d[state.board.cell_index(middle_row, middle_column)] = (
                        1.0
                    )
                    s += 1
        for k,v in d.items():
            d[k] /= s
        return d

    @staticmethod
    def empty_board_distribution_after_collision(state, row, column):
        d = {}
        s = 0
        if player_to_color(state.turn()) == COLORS['black']:
            if (
                column - 1 >= 0 and
                state.board.color(
                    state.turn(),
                    row,
                    column - 1
                ) == COLORS['none']
            ):
                d[state.board.cell_index(row, column - 1)] = 1
                s += 1
            if (
                column + 1 < state.board.num_columns() and
                state.board.color(
                    state.turn(),
                    row,
                    column + 1
                ) == COLORS['none']
            ):
                d[state.board.cell_index(row, column + 1)] = 1
                s += 1
        else:
            if (
                row - 1 >= 0 and
                state.board.color(
                    state.turn(),
                    row - 1,
                    column
                ) == COLORS['none']
            ):
                d[state.board.cell_index(row - 1, column)] = 1
                s += 1
            if (
                row + 1 < state.board.num_rows() and
                state.board.color(
                    state.turn(),
                    row + 1,
                    column
                ) == COLORS['none']
            ):
                d[state.board.cell_index(row + 1, column)] = 1
                s += 1
        for k,v in d.items():
            d[k] /= s
        return d

    @staticmethod
    def post_openining_distribution(state, row, column):
        d = {}
        s = 0.0
        if player_to_color(state.turn()) == COLORS['white']:
            # West
            west_row = row
            west_column = column - 1
            if (
                west_column >= 0 and
                state.board.color(
                    state.turn(),
                    west_row,
                    west_column
                ) == COLORS['none']
            ):
                d[state.board.cell_index(west_row, west_column)] = 1
                s += 1

            # East
            east_row = row
            east_column = column + 1
            if (
                east_column < state.board.num_columns() and
                state.board.color(
                    state.turn(),
                    east_row,
                    east_column
                ) == COLORS['none']
            ):
                d[state.board.cell_index(east_row, east_column)] = 1
                s += 1
        else:
            # North
            north_row = row - 1
            north_column = column
            if (
                north_row >= 0 and
                state.board.color(
                    state.turn(),
                    north_row,
                    north_column
                ) == COLORS['none']
            ):
                d[state.board.cell_index(north_row, north_column)] = 1
                s += 1

            # South
            south_row = row + 1
            south_column = column
            if (
                south_row < state.board.num_rows() and
                state.board.color(
                    state.turn(),
                    south_row,
                    south_column
                ) == COLORS['none']
            ):
                d[state.board.cell_index(south_row, south_column)] = 1
                s += 1

        # Southwest
        southwest_row = row + 1
        southwest_column = column - 1
        if (
            southwest_row < state.board.num_rows() and
            southwest_column >= 0 and
            state.board.color(
                state.turn(),
                southwest_row,
                southwest_column
            ) == COLORS['none']
        ):
            d[state.board.cell_index(southwest_row, southwest_column)] = 1
            s += 1

        # Northeast
        northeast_row = row - 1
        northeast_column = column + 1
        if (
            northeast_column < state.board.num_columns() and
            northeast_row >= 0 and
            state.board.color(
                state.turn(),
                northeast_row,
                northeast_column
            ) == COLORS['none']
        ):
            d[state.board.cell_index(northeast_row, northeast_column)] = 1
            s += 1

        for k,v in d.items():
            d[k] /= s
        return d

    OPENING_MODE = 'opening'
    POST_OPENINING_MODE = 'post-opening'
    MIDGAME_MODE = 'midgame'
    SEARCH_MODE = 'search'
    RANDOM_MODE = 'random'


    @staticmethod
    def cells_are_connected(c1, c2):
        if c1[0] == c2[0]:
            # West or East
            return math.abs(c1[1] - c2[1]) == 1
        elif c1[1] == c2[1]:
            # North or South
            return math.abs(c1[0] - c2[0]) == 1
        elif c2[0] - c1[0] == 1:
            # Southwest
            return c2[1] == (c1[1] - 1)
        elif c2[0] - c1[0] == -1:
            # Northeast
            return c2[1] == (c1[1] + 1)
        else:
            return False


    def __init__(self, random_generator, only_corners=True, only_search=False):
        super(RuleBasedAgent, self).__init__()
        self.random_generator = random_generator
        self.only_corners = only_corners
        self.only_search = only_search
        self.reset()

    def midgame_distribution(self, state):
        d = {}
        s = 0.0

        my_endpoint = self.endpoints[0]
        row = state.board.row(my_endpoint)
        column = state.board.column(my_endpoint)
        if player_to_color(state.turn()) == COLORS['white']:
            if column > 0:
                west_row = row
                west_column = column - 1
                if (
                    west_column >= 0 and
                    state.board.color(
                        state.turn(),
                        west_row,
                        west_column
                    ) == COLORS['none']
                ):
                    d[state.board.cell_index(west_row, west_column)] = 1
                    s += 1
                southwest_row = row + 1
                southwest_column = column - 1
                if (
                    southwest_column >= 0 and
                    southwest_row < state.board.num_rows() and
                    state.board.color(
                        state.turn(),
                        southwest_row,
                        southwest_column
                    ) == COLORS['none']
                ):
                    d[state.board.cell_index(
                        southwest_row,
                        southwest_column)] = 1
                    s += 1
        else:
            if row > 0:
                north_row = row - 1
                north_column = column
                if (
                    north_row >= 0 and
                    state.board.color(
                        state.turn(),
                        north_row,
                        north_column
                    ) == COLORS['none']
                ):
                    d[state.board.cell_index(north_row, north_column)] = 1
                    s += 1
                northeast_row = row - 1
                northeast_column = column + 1
                if (
                    northeast_row >= 0 and
                    northeast_column < state.board.num_columns() and
                    state.board.color(
                        state.turn(),
                        northeast_row,
                        northeast_column
                    ) == COLORS['none']
                ):
                    d[state.board.cell_index(
                        northeast_row,
                        northeast_column)] = 1
                    s += 1
        my_endpoint = self.endpoints[1]
        row = state.board.row(my_endpoint)
        column = state.board.column(my_endpoint)
        if player_to_color(state.turn()) == COLORS['white']:
            if column < state.board.num_columns() - 1:
                east_row = row
                east_column = column + 1
                if (
                    east_column < state.board.num_columns() and
                    state.board.color(
                        state.turn(),
                        east_row,
                        east_column
                    ) == COLORS['none']
                ):
                    d[state.board.cell_index(east_row, east_column)] = 1
                    s += 1
                northeast_row = row - 1
                northeast_column = column + 1
                if (
                    northeast_row >= 0 and
                    northeast_column < state.board.num_columns() and
                    state.board.color(
                        state.turn(),
                        northeast_row,
                        northeast_column
                    ) == COLORS['none']
                ):
                    d[state.board.cell_index(
                        northeast_row,
                        northeast_column)] = 1
                    s += 1
        else:
            if row < state.board.num_rows() - 1:
                south_row = row + 1
                south_column = column
                if (
                    south_row < state.board.num_rows() and
                    state.board.color(
                        state.turn(),
                        south_row,
                        south_column
                    ) == COLORS['none']
                ):
                    d[state.board.cell_index(south_row, south_column)] = 1
                    s += 1
                southwest_row = row + 1
                southwest_column = column - 1
                if (
                    southwest_row < state.board.num_rows() and
                    southwest_column >= 0 and
                    state.board.color(
                        state.turn(),
                        southwest_row,
                        southwest_column
                    ) == COLORS['none']
                ):
                    d[state.board.cell_index(
                        southwest_row,
                        southwest_column)] = 1
                    s += 1
        for k,v in d.items():
            d[k] /= s
        return d

    def search(self, state, time_allowed_s):
        if self.move_pending:
            return self.search_agent.distribution(exclude=self.last_move)
        else:
            self.search_agent.search(time_allowed_s)
            return self.search_agent.distribution()


    def act(self, state, time_allowed_s=None):
        if self.mode == self.RANDOM_MODE:
            self.last_move = choose_legal_action_uniformly_randomly(
                state,
                self.random_generator()
            )
        else:
            d = self.distribution(state, time_allowed_s=time_allowed_s)
            if len(d) == 0:
                self.mode = self.SEARCH_MODE
                d = self.search(state, time_allowed_s)
            self.last_move = choose_legal_action_uniformly_randomly(
                    state,
                    self.random_generator()
                ) if len(d) == 0 else choose_from_distribution(
                    d,
                    self.random_generator()
                )
        self.move_pending = True
        return (
            state.board.row(self.last_move),
            state.board.column(self.last_move)
        )

    def distribution(self, state, weight=1.0, time_allowed_s=None):
        if self.search_agent is None:
            fast_state = HexGameState.root(state.board.num_rows())
            fast_state.set_turn(state.turn())
            self.search_agent = MctsAgent(fast_state)
        if self.move_pending:
            row = state.board.row(self.last_move)
            column = state.board.column(self.last_move)
            try:
                self.search_agent.move((column, row), color_to_player(state[row, column]))
            except IllegalAction:
                # print("WARNING: Column {}, row {}, is an illegal action on the following board:".format(column, row))
                # print(str(self.search_agent.rootstate))
                # print("WARNING: The actual board is:")
                # print(str(state))
                if self.mode == self.SEARCH_MODE:
                    self.mode = self.RANDOM_MODE
            if state[row, column] != player_to_color(state.turn()):
                if self.mode == self.OPENING_MODE:
                    d = self.empty_board_distribution_after_collision(
                        state,
                        row,
                        column
                    )
                elif self.mode == self.POST_OPENINING_MODE:
                    row = state.board.row(self.endpoints[0])
                    column = state.board.column(self.endpoints[0])
                    d = self.post_openining_distribution(state, row, column)
                    if len(d) == 0:
                        self.mode = self.SEARCH_MODE
                        d = self.search(state, time_allowed_s)
                elif self.mode == self.MIDGAME_MODE:
                    d = self.midgame_distribution(state)
                    if len(d) == 0:
                        self.mode = self.SEARCH_MODE
                        d = self.search(state, time_allowed_s)
                else:
                    d = self.search(state, time_allowed_s)
            else:
                self.move_pending = False
                if self.mode == self.OPENING_MODE:
                    self.endpoints.append(self.last_move)
                    self.mode = self.POST_OPENINING_MODE
                elif self.mode == self.POST_OPENINING_MODE:
                    self.endpoints.append(self.last_move)
                    if player_to_color(state.turn()) == COLORS['white']:
                        if (
                            state.board.column(self.endpoints[1]) <
                            state.board.column(self.endpoints[0])
                        ):
                            self.endpoints.reverse()
                    elif (
                        state.board.row(self.endpoints[1]) <
                        state.board.row(self.endpoints[0])
                    ):
                        self.endpoints.reverse()
                    self.mode = self.MIDGAME_MODE
                elif self.mode == self.MIDGAME_MODE:
                    if player_to_color(state.turn()) == COLORS['white']:
                        if (
                            state.board.column(self.last_move) <
                            state.board.column(self.endpoints[0])
                        ):
                            self.endpoints[0] = self.last_move
                        elif (
                            state.board.column(self.last_move) >
                            state.board.column(self.endpoints[1])
                        ):
                            self.endpoints[1] = self.last_move
                    else:
                        if (
                            state.board.row(self.last_move) <
                            state.board.row(self.endpoints[0])
                        ):
                            self.endpoints[0] = self.last_move
                        elif (
                            state.board.row(self.last_move) >
                            state.board.row(self.endpoints[1])
                        ):
                            self.endpoints[1] = self.last_move
                d = self.distribution(
                    state,
                    weight=weight,
                    time_allowed_s=time_allowed_s
                )
        else:
            d = {}
            if self.mode == self.OPENING_MODE:
                d = self.empty_board_distribution(state, weight, only_corners=self.only_corners)
            elif self.mode == self.POST_OPENINING_MODE:
                row = state.board.row(self.last_move)
                column = state.board.column(self.last_move)
                d = self.post_openining_distribution(state, row, column)
            elif self.mode == self.MIDGAME_MODE:
                d = self.midgame_distribution(state)
            else:
                d = self.search(state, time_allowed_s)
        return d

    def reset(self):
        if self.only_search:
            self.mode = self.SEARCH_MODE
        else:
            self.mode = self.OPENING_MODE
        self.last_move = None
        self.endpoints = []
        self.move_pending = False
        self.last_distribution = {}
        self.search_agent = None
