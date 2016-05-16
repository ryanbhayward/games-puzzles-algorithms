from games_puzzles_algorithms.players.rule_based.rule_based_agent import RuleBasedAgent
from games_puzzles_algorithms.games.dex.game_state import GameState
from games_puzzles_algorithms.games.dex.game_state import COLORS
from games_puzzles_algorithms.games.dex.game_state import color_to_player
from games_puzzles_algorithms.games.dex.game_state import cell_str
from games_puzzles_algorithms.games.dex.game_state import cell_str_to_cell
import random


def test_error():
    random_generator = random.Random(290134)
    state = GameState.root(8)
    patient = RuleBasedAgent(lambda: random_generator.uniform(0, 1), only_corners=False)

    cells_to_play = [
      cell_str_to_cell('e4'),
      cell_str_to_cell('h1'),
      cell_str_to_cell('e3'),
      cell_str_to_cell('g1'),
      cell_str_to_cell('f2'),
      cell_str_to_cell('f1'),
      cell_str_to_cell('d5'),
      cell_str_to_cell('e1'),
      cell_str_to_cell('d6'),
      cell_str_to_cell('d2'),
      cell_str_to_cell('c7'),
      cell_str_to_cell('c3'),
      cell_str_to_cell('g1'),
      cell_str_to_cell('b4')
    ]
    for cell in cells_to_play:
      state.play(state.board.cell_index(*cell))


def test_midgame_black():
    random_generator = random.Random(290134)
    state = GameState.root(5)
    patient = RuleBasedAgent(lambda: random_generator.uniform(0, 1), only_corners=False)

    state.play(state.board.cell_index(0, 0))
    state.play(state.board.cell_index(2, 2))
    state.play(state.board.cell_index(1, 0))
    state.play(state.board.cell_index(3, 1))
    state.play(state.board.cell_index(0, 1))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  O  .  .  .  .  O
  3  .  .  @  .  .  O
   4  .  @  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.mode = RuleBasedAgent.POST_OPENINING_MODE
    patient.move_pending = True
    patient.endpoints.append(state.board.cell_index(2, 2))
    patient.last_move = state.board.cell_index(3, 1)
    d = patient.distribution(state)
    s = 0.0
    for k,v in d.items():
        s += v
    assert s > 1.0 - 1.e-10 and s < 1.0 + 1.e-10

    actions = sorted(d.keys())

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  O  .  .  @  .  O
  3  .  .  @  .  .  O
   4  .  @  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  O  .  @  .  .  O
  3  .  .  @  .  .  O
   4  .  @  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  O  .  .  .  .  O
  3  .  .  @  .  .  O
   4  .  @  .  .  .  O
    5  .  @  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  O  .  .  .  .  O
  3  .  .  @  .  .  O
   4  .  @  .  .  .  O
    5  @  .  .  .  .  O
        @  @  @  @  @'''
        )


def test_midgame_white():
    random_generator = random.Random(290134)
    state = GameState.root(5)
    patient = RuleBasedAgent(lambda: random_generator.uniform(0, 1), only_corners=False)

    state.play(state.board.cell_index(2, 2))
    state.play(state.board.cell_index(0, 0))
    state.play(state.board.cell_index(3, 1))
    state.play(state.board.cell_index(1, 0))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  @  .  .  .  .  O
  3  .  .  O  .  .  O
   4  .  O  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.mode = RuleBasedAgent.POST_OPENINING_MODE
    patient.move_pending = True
    patient.endpoints.append(state.board.cell_index(2, 2))
    patient.last_move = state.board.cell_index(3, 1)
    d = patient.distribution(state)
    s = 0.0
    for k,v in d.items():
        s += v
    assert s > 1.0 - 1.e-10 and s < 1.0 + 1.e-10

    actions = sorted(d.keys())

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  @  .  .  .  .  O
  3  .  .  O  O  .  O
   4  .  O  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  @  .  .  O  .  O
  3  .  .  O  .  .  O
   4  .  O  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  @  .  .  .  .  O
  3  .  .  O  .  .  O
   4  .  O  .  .  .  O
    5  O  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  @  .  .  .  .  O
  3  .  .  O  .  .  O
   4  O  O  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )


def test_post_opening_white():
    random_generator = random.Random(290134)
    state = GameState.root(5)
    patient = RuleBasedAgent(lambda: random_generator.uniform(0, 1), only_corners=False)

    state.play(state.board.cell_index(2, 2))
    state.play(state.board.cell_index(0, 0))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  O  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.mode = RuleBasedAgent.POST_OPENINING_MODE
    patient.last_move = state.board.cell_index(2, 2)
    d = patient.distribution(state)
    s = 0.0
    for k,v in d.items():
        s += v
    assert s > 1.0 - 1.e-10 and s < 1.0 + 1.e-10

    actions = sorted(d.keys())

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  O  O  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  O  .  O
  3  .  .  O  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  O  .  .  O
   4  .  O  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  @  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  O  O  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )


def test_post_opening_black():
    random_generator = random.Random(290134)
    state = GameState.root(5)
    patient = RuleBasedAgent(lambda: random_generator.uniform(0, 1), only_corners=False)

    state.play(state.board.cell_index(0, 0))
    state.play(state.board.cell_index(2, 2))
    state.play(state.board.cell_index(0, 1))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  @  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
    )

    patient.mode = RuleBasedAgent.POST_OPENINING_MODE
    patient.last_move = state.board.cell_index(2, 2)
    d = patient.distribution(state)
    s = 0.0
    for k,v in d.items():
        s += v
    assert s > 1.0 - 1.e-10 and s < 1.0 + 1.e-10

    actions = sorted(d.keys())

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  .  .  .  @  .  O
  3  .  .  @  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  @  .  .  O
   4  .  .  @  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  .  .  @  .  .  O
  3  .  .  @  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert str(state) == (
'''
  A  B  C  D  E
1  O  O  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  @  .  .  O
   4  .  @  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )


def test_collision_after_empty():
    random_generator = random.Random(290134)
    state = GameState.root(5)
    patient = RuleBasedAgent(lambda: random_generator.uniform(0, 1), only_corners=False)

    action = patient.act(state)
    state.play(state.board.cell_index(*action))
    state.play(state.board.cell_index(*action))
    state.set_player_to_act(COLORS['black'])
    d = patient.distribution(state)

    actions = sorted(d.keys())

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert state.to_s(color_to_player(COLORS['black'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  O  @  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )


def test_on_empty():
    random_generator = random.Random(290134)
    state = GameState.root(5)
    patient = RuleBasedAgent(lambda: random_generator.uniform(0, 1), only_corners=False)

    d = patient.distribution(state)
    s = 0.0
    for k,v in d.items():
        s += v
    assert s > 1.0 - 1.e-10 and s < 1.0 + 1.e-10

    actions = sorted(d.keys())

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert state.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  O  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert state.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  O  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert state.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  O  .  .  O
   4  .  .  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert state.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  O  .  .  .  O
    5  .  .  .  .  .  O
        @  @  @  @  @'''
        )

    state.undo()

    action = actions.pop()
    row = state.board.row(action)
    column = state.board.column(action)
    state.play(state.board.cell_index(row, column))

    assert state.to_s(color_to_player(COLORS['white'])) == (
'''
  A  B  C  D  E
1  .  .  .  .  .  O
 2  .  .  .  .  .  O
  3  .  .  .  .  .  O
   4  .  .  .  .  .  O
    5  O  .  .  .  .  O
        @  @  @  @  @'''
        )
